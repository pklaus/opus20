#!/usr/bin/env python

import argparse
import logging
import pdb

from opus20 import Opus20FakeServer

logger = logging.getLogger('opus20_fakeserver')

def main():

    parser = argparse.ArgumentParser(description="Discovery of Lufft OPUS20 devices on the local network")
    parser.add_argument('bind_address', default="", nargs="?", help='The IP to bind to')
    parser.add_argument('--feed_logfile', help='A log file to feed the fake server with l2p frames')
    parser.add_argument('--loglevel', '-l', default="INFO", choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], help='log level')
    args = parser.parse_args()

    if args.loglevel:
        logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    fs = Opus20FakeServer(args.bind_address)
    if args.feed_logfile:
        logger.info("Feeding server with l2p example communication...".format(args.bind_address))
        fs.feed_with_communication_log(args.feed_logfile)
    logger.info("Starting fake OPUS20 server on interface {}...".format(args.bind_address))
    fs.bind_and_serve()
    logger.info("Fake OPUS20 server closed.")

if __name__ == "__main__": main()
