#!/usr/bin/env python
# -*- coding: utf-8 -*-

# local deps
from opus20 import Opus20, OPUS20_CHANNEL_SPEC, PickleStore, Object

# std lib
import logging
import os
import time
from datetime import datetime

# external deps
from bottle import Bottle, request, response, view, static_file, TEMPLATE_PATH, jinja2_view as view

logger = logging.getLogger(__name__)

# Find out where our resource files are located:
try:
    from pkg_resources import resource_filename, Requirement
    PATH = resource_filename("opus20", "webapp")
except:
    PATH = './'

TEMPLATE_PATH.insert(0, os.path.join(PATH, 'views'))

clock = time.perf_counter

class PlotWebServer(Bottle):

    DPI = 72
    MIME_MAP = {
      'pdf': 'application/pdf',
      'png': 'image/png',
      'svg': 'image/svg+xml'
    }

    def __init__(self, host, log_file, **kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
            del kwargs['debug']
        else:
            self.debug = False
        self.o20 = Opus20(host, **kwargs)
        self.o20.disconnect()
        self.logfile = log_file
        self.ps = PickleStore(log_file)
        self._current_values_last_call = -1E13
        self._download_device_data_last_call = -1E13
        super(PlotWebServer, self).__init__()
        self.route('/connected/device', callback = self._connected_device)
        self.route('/list/devices', callback = self._list_devices)
        self.route('/download/<device_id>', callback = self._download_device_data)
        self.route('/plot/<device_id>_history.<fileformat>', callback = self._plot_history)
        self.route('/static/<filename:path>', callback = self._serve_static)
        if self.debug: self.route('/debug', callback = self._debug)
        self.route('/plot', callback = self._plot_page)
        self.route('/', callback = self._index)

    @view('index.jinja2')
    def _index(self):
        return {'current_values': self.current_values, 'active': 'home'}

    @view('plot.jinja2')
    def _plot_page(self):
        return {'device_id': self._connected_device(), 'active': 'plot'}

    @property
    def current_values(self):
        """ the current values """
        if  clock() - self._current_values_last_call < 2.0:
            return self._cached_current_values
        self._current_values_last_call = clock()
        cur = Object()
        values = self.o20.multi_channel_value( [0x0064, 0x006E, 0x00C8, 0x00CD, 0x2724] )
        cur.temperature =       values[0]
        cur.dewpoint =          values[1]
        cur.relative_humidity = values[2]
        cur.absolute_humidity = values[3]
        cur.battery_voltage =   values[4]
        cur.ts = datetime.now().replace(microsecond=0)
        self._cached_current_values = cur
        return cur

    def _serve_static(self, filename):
        return static_file(filename, root=os.path.join(PATH, 'static'))

    @view('debug.jinja2')
    def _debug(self):
        return {
          'active': 'debug',
          'debug_dict': {
            'self._current_values_last_call': self._current_values_last_call,
            'self._download_device_data_last_call': self._download_device_data_last_call,
          }
        }

    def _connected_device(self):
        return self.o20.device_id

    def _list_devices(self):
        return dict(devices=self.ps.get_device_ids())

    def _download_device_data(self, device_id):
        if  clock() - self._download_device_data_last_call < 10.0:
            return {'success': True, 'cached': True}
        self._download_device_data_last_call = clock()
        try:
            max_ts = self.ps.max_ts()[device_id]
        except KeyError:
            max_ts = None
        log_data = self.o20.download_logs(start_datetime=max_ts)
        self.o20.disconnect()
        self.ps.add_data(self.o20.device_id, log_data)
        self.ps.persist()
        return {'success': True}

    def _plot_history(self, device_id, fileformat):
        from io import BytesIO
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        df = pd.DataFrame(self.ps.get_data(device_id))

        df = df.set_index('ts', drop=True)
        df.columns = [OPUS20_CHANNEL_SPEC[col]['name'] for col in df.columns]

        # Handling of URL query variables
        q_range = request.query.range
        if q_range:
            if ',' in q_range:
                q_range = q_range.split(',')
                df = df[q_range[0]:q_range[1]]
            else:
                df = df[q_range]
        else:
            q_range = 'All Time'
        figsize = request.query.figsize or '10,6'
        figsize = (float(num) for num in figsize.split(','))
        dpi = request.query.dpi or self.DPI
        dpi = float(dpi)
        #resample = request.query.resample or '2min'
        measures = request.query.measures
        right = request.query.right
        if not measures:
            measures = ('temperature', 'relative humidity')
        else:
            measures = measures.split(',')
        if not right:
            right = ('relative humidity',)
        else:
            right = right.split(',')
        #selected_cols = df.columns
        selected_cols = set()
        for measure in measures:
            for col in df.columns:
                if measure in col:
                    selected_cols.add(col)
        selected_cols = list(selected_cols)
        right_cols = set()
        for col in selected_cols:
            for measure in right:
                if measure in col:
                    right_cols.add(col)
        right_cols = list(right_cols)
        # / End handling URL query variables

        fig = plt.figure(num=None, figsize=figsize, facecolor='w', edgecolor='k')
        ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])

        #ax = df.ix[:,selected_cols].plot(grid=True, secondary_y=right)
        ax = df.ix[:,selected_cols].plot(ax=ax, grid=True, secondary_y=right_cols, x_compat=False)
        ax.set_xlabel('')
        ax.set_ylabel('temperature [°C]')
        plt.ylabel('humidity [%]')
        #plt.title("OPUS20 device: " + device_id)
        ax.set_title("OPUS20 device: " + device_id)

        #ax = fig.add_subplot(111)
        #df.ix[:,measure.split(',')].resample(resample).plot(ax=ax)
        #start, end = ax.get_xlim()
        #ax.xaxis.set_ticks(np.arange(start, end, 1.0))
        ax.xaxis.grid(True, which="minor")
        #if type(q_range) == str:
        #    ax.set_xlabel(q_range)
        #else:
        #    ax.set_xlabel(' - '.join(q_range))
        #ax.set_ylabel('Power [Watt]')
        #ax.legend()

        io = BytesIO()
        fig.savefig(io, format=fileformat, dpi=dpi)
        plt.close()
        response.content_type = self.MIME_MAP[fileformat]
        return io.getvalue()

    def disconnect_opus20(self):
        self.o20.close()

