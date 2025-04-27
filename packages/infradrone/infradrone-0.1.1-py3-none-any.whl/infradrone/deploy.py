import curses
from infradrone.utils import get_providers, get_os, get_templates, get_docker_os, get_docker_templates

def deploy_infra_instance(stdscr):
    providers = get_providers()
    providers.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_providers(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = "Choose the provider"
        stdscr.addstr(1, w//2 - len(title)//2, title)

        for idx, row in enumerate(providers):
            x = w//2 - len(row)//2
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
        stdscr.addstr(1, w//2 - len(title)//2, title)

        for idx, row in enumerate(os_list):
            x = w//2 - len(row)//2
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
        stdscr.addstr(1, w//2 - len(title)//2, title)

        for idx, row in enumerate(templates):
            x = w//2 - len(row)//2
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
                stdscr.addstr(0, 0, f"You selected '{templates[current_row]}' for {os_name} on {provider}")
                stdscr.refresh()
                stdscr.getch()
            break
        elif key == 27:  # ESC key
            return
        print_templates(stdscr, current_row)

def deploy_docker(stdscr):
    os_list = get_docker_os()
    os_list.append("BACK TO PREVIOUS MENU")
    current_row = 0

    def print_os(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = "Choose the OS for Docker"
        stdscr.addstr(1, w//2 - len(title)//2, title)

        for idx, row in enumerate(os_list):
            x = w//2 - len(row)//2
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
        stdscr.addstr(1, w//2 - len(title)//2, title)

        for idx, row in enumerate(templates):
            x = w//2 - len(row)//2
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
                stdscr.addstr(0, 0, f"You selected '{templates[current_row]}' for Docker on {os_name}")
                stdscr.refresh()
                stdscr.getch()
            break
        elif key == 27:  # ESC key
            return
        print_templates(stdscr, current_row)