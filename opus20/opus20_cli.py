#!/usr/bin/env python

import pdb
import sys
import time
import argparse
import logging

from opus20 import Opus20, OPUS20_CHANNEL_SPEC, PickleStore, Opus20ConnectionException

clock = time.perf_counter
logger = logging.getLogger('opus20_cli')

def extended_int(string):
    if string.startswith('0x'):
        return int(string, 16)
    else:
        return int(string)

def main():

    parser = argparse.ArgumentParser(description="CLI for the Lufft OPUS20. Note that the subcommands provide their own --help!")
    parser.add_argument('host', help='hostname of the device')
    parser.add_argument('--port', '-p', type=int, help='TCP port of the OPUS20')
    parser.add_argument('--timeout', '-t', type=float, help='Timeout of the TCP connection in seconds')
    parser.add_argument('--loglevel', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], help='Sets the verbosity of this script')
    subparsers = parser.add_subparsers(title='commands', help='', dest='cmd')
    parser_list = subparsers.add_parser('list', help='list all possible measurement channels')
    parser_get = subparsers.add_parser('get', help='get the value(s) of specific channel(s)')
    parser_get.add_argument('channel', type=extended_int, nargs='+', help='The selected channel(s)')
    parser_download = subparsers.add_parser('download', help='download the logs and store them locally')
    parser_download.add_argument('persistance_file', help='file to store the logs in')
    parser_logging = subparsers.add_parser('logging', help='change or query global logging settings (start, stop, clear)')
    subsubparsers = parser_logging.add_subparsers(help='Action to perform w/ respect to logging', dest='action')
    parser_logging_action_status = subsubparsers.add_parser('status', help='Query the current logging status of the device')
    parser_logging_action_start  = subsubparsers.add_parser('start', help='Start logging altogether on the device')
    parser_logging_action_stop   = subsubparsers.add_parser('stop', help='Stop logging altogether on the device')
    parser_logging_action_clear  = subsubparsers.add_parser('clear', help='Clear the log history on the device')
    parser_enable = subparsers.add_parser('enable', help='enable logging for a specific channel')
    parser_enable.add_argument('channel', type=extended_int, nargs='+', help='The selected channel(s)')
    parser_disable = subparsers.add_parser('disable', help='disable logging for a specific channel')
    parser_disable.add_argument('channel', type=extended_int, nargs='+', help='The selected channel(s)')
    args = parser.parse_args()

    if not args.cmd: parser.error('please select a command')
    if args.cmd == 'logging' and not args.action: parser.error('please select a logging action')

    if args.loglevel:
        logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    start = clock()
    o20 = None
    try:
        kwargs = {}
        if args.port: kwargs['port'] = args.port
        if args.timeout: kwargs['timeout'] = args.timeout
        o20 = Opus20(args.host, **kwargs)

        if args.cmd == 'list':
            for channel in o20.available_channels:
                log_enabled = o20.get_channel_logging_state(channel)
                log_enabled = 'yes' if log_enabled else 'no'
                fmt = "Channel {:5d} (0x{:04X}): {name:22s}  unit: {unit:4s}  offset: {offset:5s}  logging: {log_enabled}"
                print(fmt.format(channel, channel, log_enabled=log_enabled, **OPUS20_CHANNEL_SPEC[channel]))
        if args.cmd == 'get':
            if len(args.channel) > 1:
                for channel in o20.multi_channel_value(args.channel):
                    print("{:.3f}".format(channel))
            else:
                print("{:.3f}".format(o20.channel_value(args.channel[0])))
        if args.cmd == 'download':
            ps = PickleStore(args.persistance_file)
            try:
                max_ts = ps.max_ts()[o20.device_id]
            except KeyError:
                max_ts = None
            log_data = o20.download_logs(start_datetime=max_ts)
            ps.add_data(o20.device_id, log_data)
            ps.persist()
        if args.cmd == 'logging':
            def logging_in_words(): return 'enabled' if o20.get_logging_state() else 'disabled'
            if args.action == 'status':
                print("Logging is currently " + logging_in_words() + ".")
            elif args.action in ('start', 'stop'):
                o20.set_logging_state(args.action == 'start')
                logger.info("Logging is now " + logging_in_words() + ".")
            elif args.action == 'clear':
                o20.clear_log()
                print('Clearing the log now. This will take a couple of minutes.')
                print('You cannot make requests to the device during that time.')
                o20.disconnect()
        if args.cmd in ('enable', 'disable'):
            enable = args.cmd == 'enable'
            for channel in args.channel:
                o20.set_channel_logging_state(enable)

    except Opus20ConnectionException as e:
        parser.error(str(e))

    finally:
        try:
            o20.disconnect()
            o20 = None
        except:
            pass
    end = clock()
    logger.info("script running time (net): {:.6f} seconds.".format(end-start))


if __name__ == "__main__": main()
