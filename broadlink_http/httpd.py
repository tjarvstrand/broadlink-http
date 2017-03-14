#!/usr/bin/env python

# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import os
import os.path
import time
import sys

#third party libs
from daemon import runner

import broadlink_http

class BroadlinkHttpd():

    def __init__(self, config_filename):
        self.config = broadlink_http.get_config(config_filename)
        self.stdin_path = '/dev/pts/37'
        self.stdout_path = '/dev/pts/37'
        self.stderr_path = '/dev/pts/37'
        self.pidfile_path =  self.config['pid_file']
        self.pidfile_timeout = 5

    def run(self):
        broadlink_http.serve(self.config)

def main():
    if len(sys.argv) > 2:
        config_filename = sys.argv[2]
    else:
        config_filename = os.path.join(os.getcwd(), ".broadlink/config.json")

    daemon_runner = runner.DaemonRunner(BroadlinkHttpd(config_filename))
    daemon_runner.do_action()

if __name__ == "__main__":
    main()
