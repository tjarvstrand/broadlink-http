from BaseHTTPServer import BaseHTTPRequestHandler
import json
import traceback

import device
from exception import NotFoundException, TimeoutException

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            self.handle_post()
            self.send_response(200)
        except NotFoundException, e:
            self.send_response(404)
        except TimeoutException, e:
            self.send_response(504)
        except Exception, e:
            self.send_response(500, message = traceback.format_exc())

    def handle_post(self):
        (command, args) = self.parse_path_and_args()
        print "Received POST request: %s with args %s" % (command, args)
        if command == "generate_device":
            device.generate_device(self.server.config['directory'],
                                   self.server.config.get('ip', None))
        elif command == "learn_command":
            device.learn_command(self.server.config['directory'], args)
        elif command == "send_commands":
            device.send_commands(self.server.config['directory'], args)
        else:
            print "unknown command: %s" % command
            raise NotFoundException()

    def do_GET(self):
        try:
            body = self.handle_get()
            self.send_response(200, message = json.dumps(body))
        except NotFoundException, e:
            self.send_response(404)
        except TimeoutException, e:
            self.send_response(504)
        except Exception, e:
            self.send_response(500, message = traceback.format_exc())

    def handle_get(self):
        (command, args) = self.parse_path_and_args()
        print "Received GET request: %s with args %s" % (command, args)
        if command == "list_commands":
            commands = device.list_commands(self.server.config['directory'], args)
            print "Command successful: %s" % command
            return commands
        else:
            print "Unknown command: %s" % command
            raise NotFoundException()


    def parse_path_and_args(self):
        s = self.path.split('?')
        if len(s) > 1:
            args = dict([arg.split('=') for arg in s[-1].split('&')])
        else:
            args = {}
        args['commands'] = args.get('commands', '').split(',')
        args['command_repeat'] = int(args.get('command_repeat', '1'))
        args['command_repeat_interval'] = float(args.get('command_repeat_interval', '0.1'))
        args['iterations'] = int(args.get('iterations', '1'))
        args['iteration_interval'] = float(args.get('iteration_interval', '1.0'))
        args['timeout'] = float(args.get('timeout', '30.0'))
        return (s[0][1:], args)
