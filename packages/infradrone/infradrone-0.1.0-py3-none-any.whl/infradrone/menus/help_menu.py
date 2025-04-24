import curses

def help_menu(stdscr):
    help_text = [
        "InfraDrone Help Menu",
        "",
        "This script provides a menu-driven interface for managing infrastructure deployments.",
        "",
        "Main Menu Options:",
        "1. Deploy infra instance: Allows you to deploy a new infrastructure instance.",
        "2. Deploy docker: Allows you to deploy Docker on a selected instance.",
        "3. Set Default Parameter configuration: Allows you to set default parameters for deployments.",
        "4. SSH connections: Manage SSH connections to your instances.",
        "5. Help: Displays this help menu.",
        "6. EXIT: Exits the script.",
        "",
        "Navigation:",
        "Use the UP and DOWN arrow keys to navigate through the menu options.",
        "Press ENTER to select an option.",
        "Press ESC to go back to the previous menu or exit.",
        "",
        "Deploy infra instance:",
        "1. Choose the provider: Select the cloud provider for the instance.",
        "2. Choose the OS: Select the operating system for the instance.",
        "3. Choose the template: Select the template for the instance.",
        "4. Enter Instance Name: Provide a name for the instance.",
        "5. Enter Allowed Ports: Specify the ports to be allowed (comma-separated).",
        "",
        "Deploy docker:",
        "1. Choose the OS for Docker: Select the operating system for Docker.",
        "2. Choose the template for Docker: Select the Docker template.",
        "3. Enter parameter values: Provide values for the required parameters.",
        "4. Execute installation plan: Follow the steps to deploy Docker.",
        "",
        "Set Default Parameter configuration:",
        "1. Select a parameter to edit: Choose a parameter to modify.",
        "2. Save and return to main menu: Save the changes and go back to the main menu.",
        "",
        "SSH connections:",
        "1. Manage SSH connections: Add, edit, or delete SSH connections.",
        "2. Open SSH connection: Connect to an instance via SSH.",
        "",
        "Press any key to go back to the main menu."
    ]

    def print_help_page(stdscr, start_line):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for idx, line in enumerate(help_text[start_line:start_line + h - 1]):
            stdscr.addstr(idx, 2, line)  # Align to the left side
        stdscr.refresh()

    curses.curs_set(0)
    start_line = 0
    print_help_page(stdscr, start_line)

    while True:
        h, w = stdscr.getmaxyx()
        key = stdscr.getch()
        if key == curses.KEY_DOWN and start_line + h - 1 < len(help_text):
            start_line += 1
            print_help_page(stdscr, start_line)
        elif key == curses.KEY_UP and start_line > 0:
            start_line -= 1
            print_help_page(stdscr, start_line)
        elif key in [10, 13, 27]:  # Enter or ESC key
            break