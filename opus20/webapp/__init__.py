#!/usr/bin/env python

# local deps
from opus20 import Opus20, OPUS20_CHANNEL_SPEC, PickleStore

# std lib
import logging

# external deps
from bottle import Bottle, request, response

logger = logging.getLogger(__name__)

class PlotWebServer(Bottle):

    DPI = 72
    MIME_MAP = {
      'pdf': 'application/pdf',
      'png': 'image/png',
      'svg': 'image/svg+xml'
    }

    def __init__(self, host, log_file, **kwargs):
        self.o20 = Opus20(host, **kwargs)
        self.o20.disconnect()
        self.logfile = log_file
        self.ps = PickleStore(log_file)
        super(PlotWebServer, self).__init__()
        self.route('/connected/device', callback = self._connected_device)
        self.route('/list/devices', callback = self._list_devices)
        self.route('/download/<device_id>', callback = self._download_device_data)
        self.route('/plot/<device_id>_history.<fileformat>', callback = self._plot_history)

    def _connected_device(self):
        return self.o20.device_id

    def _list_devices(self):
        return dict(devices=self.ps.get_device_ids())

    def _download_device_data(self, device_id):
        try:
            max_ts = self.ps.max_ts()[device_id]
        except KeyError:
            max_ts = None
        log_data = self.o20.download_logs(start_datetime=max_ts)
        self.o20.disconnect()
        self.ps.add_data(self.o20.device_id, log_data)
        self.ps.persist()

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
        if not measures:
            measures = ('temperature', 'relative humidity')
            right = ('relative humidity')
        else:
            measures = measures.split(',')
        selected_cols = df.columns
        right = set()
        if measures:
            selected_cols = set()
            for measure in measures:
                for col in df.columns:
                    if measure in col:
                        selected_cols.add(col)
            for measure in right:
                for col in df.columns:
                    if measure in col:
                        right.add(col)
        # / End handling URL query variables

        fig = plt.figure(num=None, figsize=figsize, facecolor='w', edgecolor='k')
        ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])

        #ax = df.ix[:,selected_cols].plot(grid=True, secondary_y=right)
        df.ix[:,selected_cols].plot(ax=ax, grid=True, secondary_y=right)
        plt.xlabel('')
        plt.ylabel('temperature °C')
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

