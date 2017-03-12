import base64
import broadlink
import json
import os
import os.path
import time

from exception import TimeoutException

def get_device_filename(directory):
    return os.path.join(directory, "device.json")

def get_command_filename(directory, command):
    return os.path.join(directory, "commands", command + ".json")

def get_device(directory):
    device_filename = get_device_filename(directory)

    if not os.path.isfile(device_filename):
        generate_device(device_filename)
    with open(device_filename) as f:
        details = json.load(f)

        device = broadlink.rm((details['host'], details['port']),
                               base64.b64decode(details['mac']))
        device.id = base64.b64decode(details['id'])
        device.key = base64.b64decode(details['key'])
        return device

def generate_device(directory):
    device_filename = get_device_filename(directory)

    devices = broadlink.discover(timeout=5)
    if len(devices) == 0:
        raise Exception("No devices found")

    device = devices[0]
    device.auth()
    details = {'id': base64.b64encode(device.id),
               'host': device.host[0],
               'port': device.host[1],
               'key': base64.b64encode(device.key),
               'mac': base64.b64encode(device.mac)}
    with open(device_filename, "w") as f:
        json.dump(details, f)

def send_commands(directory, args):
    args['commands'] = args['commands'] * (args['iterations'])

    device = get_device(directory)
    while len(args['commands']) > 0:
        _send_command(device, directory, args)
        args['commands'] = args['commands'][1:]
        if len(args['commands']) > 0:
            time.sleep(args['iteration_interval'])

def _send_command(device, directory, args):
    command = args['commands'][0]
    command_filename = get_command_filename(directory, command)
    if not os.path.isfile(command_filename):
        raise Exception("Command not found: %s" % command)
    print "Executing command: %s" % command
    with open(command_filename, 'r+b') as f:
        command = f.read()
        device.send_data(base64.b64decode(command))
        for _ in range(args['command_repeat'] - 1):
            time.sleep(args['command_repeat_interval'])
            device.send_data(base64.b64decode(command))

def learn_command(directory, command, timeout):
    command_filename = get_command_filename(directory, command)
    command_directory = os.path.dirname(command_filename)
    if not os.path.isdir(command_directory):
        os.makedirs(command_directory)

    device = get_device(directory)
    device.enter_learning()
    start_time = time.time()
    data = None
    while data is None:
        if time.time() - start_time > timeout:
            raise TimeoutException
        time.sleep(1)
        data = device.check_data()

    with open(command_filename, 'w+b') as f:
        f.write(base64.b64encode(data))

