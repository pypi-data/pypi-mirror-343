import os
import json
import subprocess
import curses
import configparser

# Load the base directory from config.ini
CONFIG_INI = 'config.ini'
config_parser = configparser.ConfigParser()
config_parser.read(CONFIG_INI)
BASE_DIR = os.path.abspath(os.path.expandvars(config_parser['Paths']['BaseDirectory']))

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

def get_providers():
    return [d for d in os.listdir('./tf') if os.path.isdir(os.path.join('./tf', d))]

def get_os(provider):
    return [d for d in os.listdir(f'./tf/{provider}') if os.path.isdir(os.path.join(f'./tf/{provider}', d))]

def get_templates(provider, os_name):
    return [d for d in os.listdir(f'./tf/{provider}/{os_name}') if os.path.isdir(os.path.join(f'./tf/{provider}/{os_name}', d))]

def get_docker_os():
    return [d for d in os.listdir('./docker') if os.path.isdir(os.path.join('./docker', d))]

def get_docker_templates(os_name):
    return [d for d in os.listdir(f'./docker/{os_name}') if os.path.isdir(os.path.join(f'./docker/{os_name}', d))]

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def generate_ssh_keys(instance_dir, ssh_key_name, password):
    ssh_key_path = os.path.join(instance_dir, ssh_key_name)
    subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', ssh_key_path, '-N', password])
    return ssh_key_path

def edit_parameter(stdscr, config, key):
    curses.echo()
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = f"Edit parameter: {key}"
    stdscr.addstr(1, 2, title)  # Align to the left side
    stdscr.addstr(3, 2, "Current value:")  # Align to the left side
    stdscr.addstr(4, 2, str(config[key]))  # Align to the left side
    stdscr.addstr(5, 2, "Enter new value:")  # Align to the left side
    stdscr.refresh()
    new_value = stdscr.getstr(6, 2, 40).decode('utf-8')  # Align to the left side
    config[key] = new_value
    save_config(config)
    curses.noecho()