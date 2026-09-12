#!/usr/bin/env python3
# WHAT: This is the "main door" script for the RSS Feed Manager & Scraper.
#       When someone runs "python3 main.py", the computer starts executing here.
#       It decides whether to open the graphical window (the screen with buttons
#       and tables) or to run quietly in the background (no window, just downloads).
# OPTIONS: You can pass text commands when you run it:
#   - "--headless" : Run the download process without opening any window (for cron jobs or servers).
#   - "--scrape"   : Immediately download all feeds once and then quit (also no window).
#   - (nothing)    : Try to open the graphical window. If there is no screen
#                    available, fall back to headless mode automatically.
# DEFAULTS: If both --headless and --scrape are given, the app behaves the
#           same as just --headless (both trigger the same quiet download mode).
# OUTPUT: Either a window on the screen (GUI mode) or text messages in the
#         terminal (headless mode) describing what was downloaded.
# ERRORS/EDGE CASES: If there is no graphical display on the computer
#   (common on servers), it prints a warning and switches to headless mode.
#   If the script is told to exit, the "sys.exit" line closes the program.
# HOW TO TEST:
#   - Run "python3 main.py --scrape" to test the background download mode.
#   - Run "python3 main.py" on a computer with a screen to test the window.
"""
Main entrypoint for RSS Feed Manager & Scraper.
Supports GUI mode (PyQt6) and CLI/headless mode (--headless, --scrape).
"""

# argparse: a helper that reads text commands typed by the user (like --headless)
#           and turns them into something the program can understand.
import argparse
# os: a helper for talking to the operating system (here, to check environment settings).
import os
# sys: lets the program control how it exits and find its own file location.
import sys
# Path: a tool for working with file and folder locations in a way that works on any OS.
from pathlib import Path

# PROJECT_ROOT: figure out the folder where this file (main.py) lives.
#   .resolve() follows any shortcuts to get the real absolute path.
#   .parent means "the folder containing this file."
PROJECT_ROOT = Path(__file__).resolve().parent
# If the project folder is not already in the list of places Python looks,
# add it so that the program can find its helper files (in the core/ folder).
# str(...) converts the folder path into plain text so it can be stored in the list.
if str(PROJECT_ROOT) not in sys.path:
    # sys.path is a list of folders Python searches when you say "import something".
    # insert(0, ...) puts our folder at the very front of that list.
    sys.path.insert(0, str(PROJECT_ROOT))

# Now import the function that does the quiet/background download.
# "run_headless_scrape" lives in the core/ folder and does the actual work
# of contacting every feed URL and saving new articles.
from core.run_headless_scrape import run_headless_scrape


def main() -> None:
    # "def main" defines a named block of instructions called "main".
    # The "() -> None" means this block takes no inputs and produces no output file.
    # argparse.ArgumentParser: creates a "command parser" that understands the
    # text commands you type after "python3 main.py".
    # description=...: this text shows up when someone runs "python3 main.py --help".
    parser = argparse.ArgumentParser(description="RSS Feed Manager & Scraper")
    # Add a switch for "--headless". action="store_true" means:
    #   if the user types --headless, set a box to True; otherwise it is False.
    # help=...: the hint text shown next to --headless in the --help output.
    parser.add_argument("--headless", action="store_true", help="Run feed scraper in headless CLI mode")
    # Add a switch for "--scrape". Same idea: True if typed, False otherwise.
    parser.add_argument("--scrape", action="store_true", help="Run immediate feed scrape in CLI mode and exit")
    # parse_args(): look at what the user typed and fill in the results.
    # "args" is now a small container with two yes/no boxes: args.headless and args.scrape.
    args = parser.parse_args()

    # If the user asked for headless OR scrape mode, run the quiet download.
    if args.headless or args.scrape:
        # Call the headless download function (defined in core/run_headless_scrape.py).
        run_headless_scrape()
        # return: stop the main() block here; the program will end.
        return

    # Ask the operating system: is there a graphical display (a screen with windows)?
    # os.environ.get("DISPLAY"): looks for the DISPLAY environment variable.
    #   On Linux, this tells us if a graphical screen is connected.
    # os.environ.get("WAYLAND_DISPLAY"): same idea but for newer Wayland display servers.
    # If DISPLAY is not set, try WAYLAND_DISPLAY. If both are empty (""), it is falsy.
    display = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    # If there is no display at all (falsy means empty or None)...
    if not display:
        # Tell the user (in plain text) what is happening.
        print("[WARNING] No GUI display detected ($DISPLAY or $WAYLAND_DISPLAY not set).")
        print("[RSS Scraper] Falling back to headless CLI scrape mode.")
        # Switch to the quiet download mode instead.
        run_headless_scrape()
        # End the program.
        return

    # Only when a graphical screen exists, launch through the GUI package.
    from gui._38_bootstrap_launch_window.bootstrap_launch_window import launch_gui_window
    launch_gui_window()


# This special "if" checks: is this file being run directly (not imported)?
# When you type "python3 main.py", this is True and main() runs.
# When another script says "import main", this is False and main() does not run automatically.
if __name__ == "__main__":
    # Call the main() block defined above to start everything.
    main()
