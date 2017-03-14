#!/usr/bin/env python

import sys

import config
import log
from server import Server
from request_handler import RequestHandler

def serve(config):
    address = (config['ip'], config['port'])
    logger = log.get_logger()
    log.add_file_handler(config['log_file'])
    logger.info('Starting httpd...')
    logger.info("Config: %s" % config)
    httpd = Server(address, RequestHandler, config, logger)
    httpd.serve_forever()

def main():
    if len(sys.argv) > 1:
        config_filename = sys.argv[1]
    else:
        config_filename = None

    try:
        serve(config.get_config(config_filename))
    except Exception, e:
        log.get_logger().critical(e)

if __name__ == "__main__":
    log.add_console_handler()
    main()
