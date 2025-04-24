import curses
import json
import os
import subprocess
from tempfile import NamedTemporaryFile, gettempdir
from infradrone.config import BASE_DIR, load_config, save_config

def load_ssh_config():
    ssh_config_path = os.path.join(BASE_DIR, 'ssh.json')
    if os.path.exists(ssh_config_path):
        with open(ssh_config_path, 'r') as f:
            return json.load(f)
    else:
        return {'connections': {}}

def save_ssh_config(config):
    ssh_config_path = os.path.join(BASE_DIR, 'ssh.json')
    with open(ssh_config_path, 'w') as f:
        json.dump(config, f, indent=4)

def ssh_connections(stdscr):
    ssh_config = load_ssh_config()
    connections = list(ssh_config['connections'].keys())
    connections.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_connections(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = "SSH Connections"
        stdscr.addstr(1, 2, title)  # Align to the left side

        for idx, conn in enumerate(connections):
            x = 2  # Align to the left side
            y = 3 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, conn)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, conn)
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_connections(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(connections) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if connections[current_row] == "BACK TO PREVIOUS MENU":
                return
            else:
                open_ssh_connection(stdscr, ssh_config, connections[current_row])
                break
        elif key == curses.KEY_DC:  # Delete key
            if connections[current_row] != "BACK TO PREVIOUS MENU":
                confirm_deletion(stdscr, ssh_config, connections[current_row])
                connections = list(ssh_config['connections'].keys())
                connections.append("BACK TO PREVIOUS MENU")
        elif key == 27:  # ESC key
            return
        print_connections(stdscr, current_row)

def confirm_deletion(stdscr, ssh_config, connection_name):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    message = f"Are you sure you want to delete {connection_name}? (y/n)"
    stdscr.addstr(h//2, 2, message)  # Align to the left side
    stdscr.refresh()
    key = stdscr.getch()
    if key in [ord('y'), ord('Y')]:
        del ssh_config['connections'][connection_name]
        save_ssh_config(ssh_config)

def open_ssh_connection(stdscr, ssh_config, connection_name):
    # Construct the full path to config.json
    config_path = os.path.join(BASE_DIR, 'config.json')
    
    # Load config.json
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    connection = ssh_config['connections'][connection_name]
    ip = connection['ip']

    if config['SSH_PROVIDER'] != 'gcp':
        user = connection['user']
        private_key = connection['private_key']

    # Remove known hosts
    known_hosts_path = os.path.expanduser(config['KNOWN_HOSTS_DIR'])
    if os.path.exists(known_hosts_path):
        os.remove(known_hosts_path)

    # Determine the SSH key path based on the SSH_PROVIDER
    if config['SSH_PROVIDER'] == 'gcp':
        private_key_path = config['PROVIDERS']['gcp']['GCP_SSH_KEY']
        user = config['PROVIDERS']['gcp']['GCP_SSH_USER']
    else:
        # Write private key to a temporary file in the project tmp folder
        tmp_dir = os.path.join(gettempdir(), 'project_tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        private_key_path = os.path.join(tmp_dir, 'id_rsa')
        public_key_path = os.path.join(tmp_dir, 'id_rsa.pub')
        with open(private_key_path, 'w') as key_file:
            key_file.write(private_key)
        with open(public_key_path, 'w') as key_file:
            key_file.write(connection['public_key'])

    try:
        stdscr.clear()
        stdscr.refresh()

        # Output the password to the terminal
        if config['SSH_PROVIDER'] == 'gcp':
            password = config['PROVIDERS']['gcp']['GCP_SSH_KEY_PASS']
        else:
            password = connection['pass']

        # Output the password to the terminal using curses
        stdscr.addstr(0, 2, f"Use the following password to connect (please copy it and paste into the following prompt request): {password}")
        stdscr.addstr(2, 2, "Press any key to continue...")
        stdscr.refresh()

        # Wait for user confirmation
        stdscr.getch()

        stdscr.clear()
        stdscr.refresh()

        curses.endwin()

        # Ensure SSH agent is running
        ssh_agent_result = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True)
        if ssh_agent_result.returncode != 0:
            print(f"Failed to start SSH agent: {ssh_agent_result.stderr}")
            return
        print(f"SSH agent started: {ssh_agent_result.stdout}")

        
        result = subprocess.run(['ssh-add', private_key_path])

        if result.returncode != 0:
            print(f"Failed to add SSH key: {result.stderr}")
            return

        # Connect using SSH with -i parameter
        subprocess.run(['ssh', '-i', private_key_path, f'{user}@{ip}'])

    finally:
        if config['SSH_PROVIDER'] != 'gcp':
            os.remove(private_key_path)
            os.remove(public_key_path)

def get_input(stdscr, prompt):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 2, prompt)  # Align to the left side
    stdscr.refresh()
    input_str = stdscr.getstr(1, 2).decode('utf-8')  # Align to the left side
    curses.noecho()
    return input_str