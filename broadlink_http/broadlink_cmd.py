#!/usr/bin/env python

import os.path
from os.path import abspath, dirname, join
import sys

import device

def main():
    if len(sys.argv) < 2:
        print "Error: Need a command!"
        sys.exit(1)
    args = sys.argv
    if args[1] == 'generate':
        device.generate_device()
    elif args[1] == 'learn':
        learn_command()
    elif args[1] == 'send':
        send_command(args[2], int(args[3]), int(args[4]))

if __name__ == "__main__":
    main(sys.argv)
