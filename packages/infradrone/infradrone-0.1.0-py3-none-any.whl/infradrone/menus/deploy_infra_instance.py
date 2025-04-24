import curses
from infradrone.utils import get_providers, get_os, get_templates
from infradrone.infra_operations import deploy_instance

def deploy_infra_instance(stdscr):
    providers = get_providers()
    providers.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_providers(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = "Choose the provider"
        stdscr.addstr(1, 2, title)  # Align to the left side

        for idx, row in enumerate(providers):
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
    print_providers(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(providers) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if providers[current_row] == "BACK TO PREVIOUS MENU":
                return
            else:
                choose_os(stdscr, providers[current_row])
            break
        elif key == 27:  # ESC key
            return
        print_providers(stdscr, current_row)

def choose_os(stdscr, provider):
    os_list = get_os(provider)
    os_list.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_os(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = f"Choose the OS for {provider}"
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
                choose_template(stdscr, provider, os_list[current_row])
            break
        elif key == 27:  # ESC key
            return
        print_os(stdscr, current_row)

def choose_template(stdscr, provider, os_name):
    templates = get_templates(provider, os_name)
    templates.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_templates(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = f"Choose the template for {os_name} on {provider}"
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
                ask_parameters(stdscr, provider, os_name, templates[current_row])
            break
        elif key == 27:  # ESC key
            return
        print_templates(stdscr, current_row)

def ask_parameters(stdscr, provider, os_name, template):
    curses.echo()
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1, 2, "Enter Instance Name: ")  # Align to the left side
    instance_name = stdscr.getstr(2, 2, 20).decode('utf-8')

    default_ports = "22, 80, 443, 8443, 8080"
    stdscr.addstr(4, 2, f"Enter Allowed Ports (comma-separated) [default: {default_ports}]: ")  # Align to the left side
    stdscr.addstr(5, 2, default_ports)
    stdscr.move(5, 2 + len(default_ports))  # Set cursor at the end of default ports
    stdscr.refresh()
    allowed_ports_input = stdscr.getstr(5, 2 + len(default_ports), 40).decode('utf-8').strip()
    if allowed_ports_input == "":
        allowed_ports_input = default_ports
    else:
        allowed_ports_input = default_ports + "," + allowed_ports_input
    allowed_ports = [int(port.strip()) for port in allowed_ports_input.split(',') if port.strip()]

    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(1, 2, "Starting the deployment...")  # Align to the left side

    success, message = deploy_instance(provider, os_name, template, instance_name, allowed_ports)

    if not success:
        stdscr.addstr(10, 2, message)  # Align to the left side
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.addstr(13, 2, f"Instance {instance_name} created successfully with IP {message}")  # Align to the left side
    stdscr.refresh()
    stdscr.getch()