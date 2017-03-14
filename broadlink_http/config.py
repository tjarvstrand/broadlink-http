
import json
import os
import os.path
from os.path import abspath, dirname, isabs, isfile, isdir, join

def get_config(path = None):
    if path is None:
        path = os.path.join(os.getcwd(), ".broadlink/config.json")
    config = get_default_config(path)
    if isfile(path):
        with open(path, 'r') as f:
            config.update(json.load(f))
    else:
        with open(path, 'w') as f:
            json.dump(config, f, indent = 2)

    config = expand_paths(config, ['directory'], os.getcwd())
    config = expand_paths(config, ['log_file', 'pid_file'], config['directory'])
    return config

def expand_paths(config, keys, absprefix):
    for key in keys:
        if not isabs(config[key]):
            config[key] = join(absprefix, config[key])
    return config

def get_default_config(path):
    directory = dirname(path)
    if directory and not isdir(directory):
        os.makedirs(directory)
    config = {'directory': directory,
              'port': 8080,
              'log_file': 'broadlink-http.log',
              'pid_file': 'broadlink-http.pid'}
    return config
