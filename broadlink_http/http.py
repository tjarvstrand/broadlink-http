#!/usr/bin/env python

import sys
import os

from request_handler import RequestHandler
from BaseHTTPServer import HTTPServer

class Server(HTTPServer):
    def __init__(self, address, handler, config):
        self.config = config
        HTTPServer.__init__(self, address, handler)

def get_config():
    config = {'directory': os.getcwd(),
              'ip': '0.0.0.0',
              'port': 8088}

    for key in config.keys():
        env_var = "BROADLINK_" + key.upper()
        if env_var in os.environ.keys():
            config[key] = os.environ[env_var]

    return config

def serve(config):
    address = (config.get('ip', ''), config['port'])
    print 'Starting broadlink-http server...'
    for (k, v) in config.iteritems():
        print "%s: %s" % (k, v)
    server = Server(address, RequestHandler, config)
    server.serve_forever()

def main():
    try:
        serve(get_config())
    except Exception, e:
        print e
        sys.exit(1)

if __name__ == "__main__":
    main()
