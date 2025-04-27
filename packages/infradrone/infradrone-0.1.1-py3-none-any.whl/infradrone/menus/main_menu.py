import argparse
import curses
from infradrone.menus.deploy_infra_instance import deploy_infra_instance
from infradrone.menus.deploy_docker import deploy_docker
from infradrone.menus.ssh_connections import ssh_connections
from infradrone.menus.help_menu import help_menu

VERSION = "0.1.1"
CREATION_DATE = "April 2025"

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    menu = [
        "Deploy infra instance",
        "Deploy docker",
        "SSH connections",
        "Help",
        "EXIT"
    ]
    current_row = 0

    def print_menu(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = "InfraDrone"
        subtitle = f"Created in: {CREATION_DATE}"
        version = f"Version: {VERSION}"

        ascii_art = [
            ".___        _____              ________                              ",
            "|   | _____/ ____\\___________  \\______ \\_______  ____   ____   ____  ",
            "|   |/    \\   __\\\\_  __ \\__  \\ |    |  \\_  __ \\/  _ \\ /    \\_/ __ \\ ",
            "|   |   |  \\  |   |  | \\/ __ \\|    `   \\  | \\(  <_> )   |  \\  ___/ ",
            "|___|___|  /__|   |__|  (____  /_______  /__|   \\____/|___|  /\\___  >",
            "         \\/                  \\/        \\/                  \\/     \\/ "
        ]

        # Check if the terminal window is large enough
        if h < len(ascii_art) + len(menu) + 10 or w < max(len(line) for line in ascii_art):
            stdscr.clear()
            stdscr.addstr(0, 0, "Please resize the window to at least {}x{} and try again.".format(
                max(len(line) for line in ascii_art), len(ascii_art) + len(menu) + 10))
            stdscr.refresh()
            stdscr.getch()
            return

        for i, line in enumerate(ascii_art):
            stdscr.addstr(1 + i, w//2 - len(line)//2, line)

        stdscr.addstr(len(ascii_art) + 2, w//2 - len(title)//2, title)
        stdscr.addstr(len(ascii_art) + 3, w//2 - len(subtitle)//2, subtitle)
        stdscr.addstr(len(ascii_art) + 4, w//2 - len(version)//2, version)

        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        for idx, row in enumerate(menu):
            x = w//2 - len(row)//2
            y = len(ascii_art) + 8 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                deploy_infra_instance(stdscr)
            elif current_row == 1:
                deploy_docker(stdscr)
            elif current_row == 2:
                ssh_connections(stdscr)
            elif current_row == 3:
                help_menu(stdscr)
            elif current_row == 4:
                break
        print_menu(stdscr, current_row)