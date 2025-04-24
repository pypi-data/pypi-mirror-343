import json
import configparser
import os

# Load the base directory from config.ini
CONFIG_INI = 'config.ini'
config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_INI)

# Resolve BASE_DIR to an absolute path
BASE_DIR = os.path.abspath(os.path.expandvars(config_parser['Paths']['BaseDirectory']))

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)