import curses
import json
import os
import paramiko
from tempfile import NamedTemporaryFile
from infradrone.utils import get_docker_os, get_docker_templates, load_config

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def load_env(file_path):
    env_vars = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    return env_vars

def save_env(params, file_path):
    env_vars = load_env(file_path)
    env_vars.update(params)
    with open(file_path, 'w', newline='\n') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

def run_ssh_command(ssh_client, command, log_file):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    log_file.write(stdout.read().decode('utf-8'))
    log_file.write(stderr.read().decode('utf-8'))

def upload_file(ssh_client, local_path, remote_path, log_file):
    sftp = ssh_client.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()
    log_file.write(f"Uploaded {local_path} to {remote_path}\n")

def deploy_docker(stdscr):
    os_list = get_docker_os()
    os_list.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_os(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = "Choose the OS for Docker"
        stdscr.addstr(1, 2, title)  # Align to the left side

        for idx, row in enumerate(os_list):
            x = 2  # Align to the left side
            y = 3 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_os(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(os_list) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if os_list[current_row] == "BACK TO PREVIOUS MENU":
                return
            else:
                choose_docker_template(stdscr, os_list[current_row])
            break
        elif key == 27:  # ESC key
            return
        print_os(stdscr, current_row)

def choose_docker_template(stdscr, os_name):
    templates = get_docker_templates(os_name)
    templates.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_templates(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = f"Choose the template for Docker on {os_name}"
        stdscr.addstr(1, 2, title)  # Align to the left side

        for idx, row in enumerate(templates):
            x = 2  # Align to the left side
            y = 3 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_templates(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(templates) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if templates[current_row] == "BACK TO PREVIOUS MENU":
                return
            else:
                execute_docker_template(stdscr, os_name, templates[current_row])
            break
        elif key == 27:  # ESC key
            return
        print_templates(stdscr, current_row)

def get_input(stdscr, prompt):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 2, prompt)  # Align to the left side
    stdscr.refresh()
    input_str = stdscr.getstr(1, 2).decode('utf-8')  # Align to the left side
    curses.noecho()
    return input_str

def execute_docker_template(stdscr, os_name, template_name):
    # Load package.json
    package_config = load_json(f'docker/{os_name}/{template_name}/package.json')
    params = package_config['params']
    installation_plan = package_config['installation_plan']

    # Load SSH connections
    ssh_config = load_json('ssh.json')
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
                ssh_connection = ssh_config['connections'][connections[current_row]]
                break
        elif key == 27:  # ESC key
            return
        print_connections(stdscr, current_row)

    config = load_config()

    if config['SSH_PROVIDER'] == 'gcp':
        private_key_path = config['PROVIDERS']['gcp']['GCP_SSH_KEY']
        user = config['PROVIDERS']['gcp']['GCP_SSH_USER']
        password = config['PROVIDERS']['gcp']['GCP_SSH_KEY_PASS']
    else:
        # Write private key to a temporary file
        with NamedTemporaryFile(delete=False) as key_file:
            key_file.write(ssh_connection['private_key'].encode())
            private_key_path = key_file.name
        user = ssh_connection['user']
        password = ssh_connection.get('pass', None)

    try:
        # Establish SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            ssh_connection['ip'],
            username=user,
            key_filename=private_key_path,
            passphrase=password
        )

        # Prompt user for parameter values
        env_params = {}
        for param in params:
            value = get_input(stdscr, f"Enter value for {param}: ")
            env_params[param] = value

        # Create the project directory and add it to the .env file
        project_dir = env_params.get('L_PROJECT_DIR')
        if project_dir:
            log_file_path = 'installation_log.txt'
            with open(log_file_path, 'w', encoding='utf-8') as log_file:
                run_ssh_command(ssh_client, f"mkdir -p {project_dir}", log_file)
                env_params['L_PROJECT_DIR'] = project_dir

        # Save parameters to .env file in the docker/{os}/{template} directory
        env_file_path = f'docker/{os_name}/{template_name}/.env'
        save_env(env_params, env_file_path)

        # Upload the .env file to the remote server
        remote_env_path = f"{project_dir}/.env"

        # Execute installation plan
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            for step in installation_plan:
                for key, value in step.items():
                    stdscr.clear()
                    stdscr.addstr(0, 2, f"Starting step: {key} - {value}")  # Align to the left side
                    stdscr.refresh()
                    if key == 'init':
                        project_dir = env_params.get(value)
                        if project_dir:
                            # Step 1: Create a directory with the name (parametrized)
                            run_ssh_command(ssh_client, f"mkdir -p {project_dir}", log_file)
                            # Step 3: Save L_PROJECT_DIR - a directory name
                            env_params['L_PROJECT_DIR'] = project_dir
                            # Step 4: Get current path from the directory
                            stdin, stdout, stderr = ssh_client.exec_command(f"pwd")
                            absolute_path = stdout.read().decode().strip()+f"/{project_dir}"
                            # Step 5: Save absolute path to the directory as G_HOME_DIR into the .env file
                            env_params['G_HOME_DIR'] = absolute_path
                            save_env(env_params, env_file_path)
                            # Step 6: Upload .env file into this directory
                            upload_file(ssh_client, env_file_path, remote_env_path, log_file)
                            # Step 7: Remember the absolute path within the script
                            g_home_dir = absolute_path
                            # Step 8: Set up the $G_HOME_DIR environment variable, so that it will be available in all scripts
                            run_ssh_command(ssh_client, f"export G_HOME_DIR={g_home_dir}", log_file)
                    elif key == 'sh/install':
                        script_path = f"sh/install/{os_name}/{value}.sh"
                        remote_path = f"{project_dir}/{os.path.basename(script_path)}"
                        upload_file(ssh_client, script_path, remote_path, log_file)
                        run_ssh_command(ssh_client, f"sudo G_HOME_DIR={g_home_dir} sh {remote_path}", log_file)
                    elif key == 'sh/helpers':
                        script_path = f"sh/helpers/{os_name}/{value}.sh"
                        remote_path = f"{project_dir}/{os.path.basename(script_path)}"
                        upload_file(ssh_client, script_path, remote_path, log_file)
                        run_ssh_command(ssh_client, f"sudo G_HOME_DIR={g_home_dir} sh {remote_path}", log_file)
                    elif key == 'sh/local':
                        script_path = f"docker/{os_name}/{template_name}/local_sh/{value}.sh"
                        remote_path = f"{project_dir}/{os.path.basename(script_path)}"
                        upload_file(ssh_client, script_path, remote_path, log_file)
                        run_ssh_command(ssh_client, f"sudo G_HOME_DIR={g_home_dir} sh {remote_path}", log_file)
                    elif key == 'file':
                        local_file_path = f"docker/{os_name}/{template_name}/{value}"
                        remote_path = f"{project_dir}/{os.path.basename(local_file_path)}"
                        upload_file(ssh_client, local_file_path, remote_path, log_file)
                    stdscr.addstr(1, 2, f"Finished step: {key} - {value}")  # Align to the left side
                    stdscr.refresh()

        ssh_client.close()
    finally:
        if config['SSH_PROVIDER'] != 'gcp':
            os.remove(private_key_path)

    stdscr.clear()
    stdscr.addstr(0, 2, f"Installation completed. Logs saved to {log_file_path}")  # Align to the left side
    stdscr.refresh()
    stdscr.getch()