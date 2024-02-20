import curses

def main(stdscr):
    # Turn off cursor blinking
    curses.curs_set(0)

    # Colors for the interface
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    highlight = curses.color_pair(1)

    # Clear screen
    stdscr.clear()
    stdscr.refresh()

    # Add a button
    stdscr.addstr(5, 10, "Press q to quit", highlight)
    stdscr.addstr(5, 10, "Press b to start", highlight)

    # Wait for user input
    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break

curses.wrapper(main)