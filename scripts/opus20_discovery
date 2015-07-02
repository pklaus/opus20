#!/usr/bin/env python

import sys
import time
import argparse
import logging
import functools

from opus20 import Opus20, OPUS20_CHANNEL_SPEC, PickleStore, Opus20ConnectionException, discover_OPUS20_devices

clock = time.perf_counter
logger = logging.getLogger('opus20_discovery')

def main():

    parser = argparse.ArgumentParser(description="Discovery of Lufft OPUS20 devices on the local network")
    parser.add_argument('bind_address', default="", nargs="?", help='The IP to bind to')
    parser.add_argument('--loglevel', '-l', default="WARNING", choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], help='log level')
    args = parser.parse_args()

    if args.loglevel:
        logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    found_devices = []
    def full_callback(found_devices, answer):
        frm, host, answer_time = answer
        dev_props = frm.kind.func()
        dev_props['answer_time'] = answer_time
        found_devices.append(dev_props)
    callback = functools.partial(full_callback, found_devices)

    start = clock()

    print("\nTrying to find devices on interface {}...\n".format(args.bind_address))
    discover_OPUS20_devices(callback, bind_addr=args.bind_address)
    for device in found_devices:
        print("[{answer_time:.2f} ms] Device ID: {device_id}, IP: {ip}, Gateway: {gw}, Network: {net}".format(**device))
    print("\nFound a total number of {} devices.\n".format(len(found_devices)))

    end = clock()
    logger.info("script running time (net): {:.6f} seconds.".format(end-start))

    sys.exit(0 if found_devices else 1)

if __name__ == "__main__": main()
