#!/usr/bin/env python

import json
import os
import os.path
from os.path import abspath, dirname, isfile, isdir, join
import sys

from server import Server
from request_handler import RequestHandler

def serve(config):
    httpd = Server((config['ip'], config['port']), RequestHandler, config)
    print 'Starting httpd...'
    httpd.serve_forever()

def create_default_config(path):
    directory = dirname(path)
    if not isdir(directory):
        os.makedirs(directory)
    config = {'directory': directory,
              'ip': '',
              'port': 8080}
    with open(path, 'w') as f:
        json.dump(config, f, indent = 2)

def get_config(path):
    if not isfile(path):
        return create_default_config(path)
    with open(path, 'r') as f:
        return json.load(f)

def main():
    if len(sys.argv) > 1:
        config = get_config(argv[2])
    else:
        config = get_config(os.path.join(os.getcwd(), ".broadlink/config.json"))
    serve(config)

if __name__ == "__main__":
    main()
