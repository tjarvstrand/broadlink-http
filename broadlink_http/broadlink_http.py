#!/usr/bin/env python

import json
import logging
import logging.handlers
import os
import os.path
from os.path import abspath, dirname, isfile, isdir, join
import sys

from server import Server
from request_handler import RequestHandler

def serve(config):
    logger = logging.getLogger('broadlink-http')
    logger.setLevel(logging.INFO)
    log_file = config['log_file']
    if not os.path.isabs(log_file):
        log_file = os.path.join(os.getcwd(), log_file)
    handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    httpd = Server((config['ip'], config['port']), RequestHandler, config, logger)
    logger.info('Starting httpd...')
    httpd.serve_forever()

def create_default_config(path):
    directory = dirname(path)
    if directory and not isdir(directory):
        os.makedirs(directory)
    config = {'directory': directory,
              'ip': '',
              'port': 8080,
              'log_file': 'broadlink-http.log'}
    with open(path, 'w') as f:
        json.dump(config, f, indent = 2)
    return config

def get_config(path):
    if not isfile(path):
        return create_default_config(path)
    with open(path, 'r') as f:
        return json.load(f)

def main():
    if len(sys.argv) > 1:
        config_filename = sys.argv[1]
    else:
        config_filename = os.path.join(os.getcwd(), ".broadlink/config.json")

    logger = logging.getLogger('broadlink-http')
    logger.addHandler(logging.StreamHandler())
    try:
        serve(get_config(config_filename))
    except Exception, e:
        logger.critical(e)

if __name__ == "__main__":
    main()
