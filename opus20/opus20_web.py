#!/usr/bin/env python

# local deps
from opus20.webapp import PlotWebServer

# std lib
import argparse
import logging

logger = logging.getLogger('opus20_web')


def main():

    parser = argparse.ArgumentParser(description="Web interface for the Lufft OPUS20")
    parser.add_argument('host', help='hostname of the device')
    parser.add_argument('--port', '-p', type=int, help='port of the device for TCP connections')
    parser.add_argument('--timeout', '-t', type=float, help='timeout for the TCP connection')
    parser.add_argument('--loglevel', '-l', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], help='log level')
    parser.add_argument('--debug', '-d', action='store_true', help='enable debugging')
    args = parser.parse_args()

    if args.loglevel:
        logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    plot_server = None
    try:
        kwargs = {}
        if args.port: kwargs['port'] = args.port
        if args.timeout: kwargs['timeout'] = args.timeout
        kwargs['debug'] = args.debug
        plot_server = PlotWebServer(args.host, '/tmp/opus20-plot-server.pickle', **kwargs)
        plot_server.run(host='0.0.0.0', port=45067, debug=args.debug)

    except ConnectionRefusedError as e:
        parser.error("Could not connect to host {}: {}".format(args.host, e))

    finally:
        try:
            plot_server.disconnect_opus20()
        except:
            pass


if __name__ == "__main__": main()
