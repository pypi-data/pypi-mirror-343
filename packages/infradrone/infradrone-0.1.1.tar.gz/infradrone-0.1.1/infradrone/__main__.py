import argparse
import curses
from infradrone.menus.main_menu import main_menu

def main():
    parser = argparse.ArgumentParser(description="InfraDrone")
    parser.add_argument("--param", type=str, help="Run with parameters")
    args = parser.parse_args()

    if args.param:
        # Placeholder for parameter handling
        print(f"Running with parameter: {args.param}")
    else:
        curses.wrapper(main_menu)

if __name__ == "__main__":
    main()