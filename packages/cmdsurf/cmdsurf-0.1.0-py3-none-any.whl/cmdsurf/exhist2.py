import os
import curses
import subprocess
import signal
import sys

HISTFILE = os.getenv("HISTFILE", os.path.expanduser("~/.bash_history"))


def load_history():
    if not os.path.exists(HISTFILE):
        return []
    with open(HISTFILE, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def save_history(commands):
    with open(HISTFILE, "w", encoding="utf-8") as f:
        f.write("\n".join(commands) + "\n")


def run_cli(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(0)
    stdscr.keypad(True)

    history = load_history()
    pos = 0
    offset = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        if not history:
            stdscr.addstr(0, 0, "No history found.", curses.A_BOLD)
        else:
            visible = history[offset : offset + h - 1]
            for idx, cmd in enumerate(visible):
                marker = ">" if offset + idx == pos else " "
                stdscr.addstr(idx, 0, f"{marker} {cmd}")

        stdscr.refresh()
        key = stdscr.getch()

        if key in [curses.KEY_UP, ord("k")]:
            if pos > 0:
                pos -= 1
            if pos < offset:
                offset -= 1

        elif key in [curses.KEY_DOWN, ord("j")]:
            if pos < len(history) - 1:
                pos += 1
            if pos >= offset + h - 1:
                offset += 1

        elif key in [10, 13]:  # Enter
            if history:
                curses.endwin()
                subprocess.run(history[pos], shell=True)
                return

        elif key in [127, curses.KEY_DC]:  # Delete
            if history:
                del history[pos]
                if pos >= len(history):
                    pos = max(0, len(history) - 1)
                save_history(history)
                offset = max(0, min(offset, len(history) - h + 1))

        elif key in [ord("q"), 3]:  # q or Ctrl+C
            return


def main():
    try:
        curses.wrapper(run_cli)
    except KeyboardInterrupt:
        print("\nExited.")


if __name__ == "__main__":
    main()
