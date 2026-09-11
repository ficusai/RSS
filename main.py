#!/usr/bin/env python3
"""
Main entrypoint for RSS Feed Manager & Scraper.
Supports GUI mode (PyQt6) and CLI/headless mode (--headless, --scrape).
"""

# WHAT: Command-line flag parsing library for accepting terminal arguments like '--headless' or '--scrape'.
# OPTIONS/VALUES: argparse.ArgumentParser(), add_argument(), parse_args().
# DEFAULTS: Standard library module.
# OUTPUT/EFFECT: Allows running the application in background mode or GUI mode.
# ERRORS/EDGE CASES: Displays help screen if invalid flags are passed.
# HOW TO TEST: Run 'python3 main.py --help'.
import argparse

# WHAT: JSON encoder and decoder library for reading configuration files (config/feeds.json).
# OPTIONS/VALUES: json.load().
# DEFAULTS: Standard library module.
# OUTPUT/EFFECT: Loads feed list from disk.
# ERRORS/EDGE CASES: Throws JSONDecodeError if config JSON file syntax is invalid.
# HOW TO TEST: Run 'python3 -c "import json; json.load(open(\"config/feeds.json\"))"'.
import json

# WHAT: Operating system environment library for checking display servers ($DISPLAY or $WAYLAND_DISPLAY).
# OPTIONS/VALUES: os.environ.get("DISPLAY").
# DEFAULTS: Standard library module.
# OUTPUT/EFFECT: Detects whether a desktop GUI monitor is connected.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "import os; print(os.environ.get(\"DISPLAY\"))"'.
import os

# WHAT: System parameters module providing command line arguments (sys.argv) and exit codes (sys.exit).
# OPTIONS/VALUES: sys.argv, sys.exit(0), sys.path.
# DEFAULTS: Standard library module.
# OUTPUT/EFFECT: Controls program exit status codes.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "import sys; print(sys.argv)"'.
import sys

# WHAT: Object-oriented filesystem path library.
# OPTIONS/VALUES: Path(__file__).resolve().parent.
# DEFAULTS: Sets absolute root directory path.
# OUTPUT/EFFECT: Guarantees module import paths work regardless of working directory.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "from pathlib import Path; print(Path(__file__).resolve())"'.
from pathlib import Path

# WHAT: Calculates project absolute root directory and inserts it into sys.path.
# OPTIONS/VALUES: Dynamic project root directory.
# DEFAULTS: Project root folder.
# OUTPUT/EFFECT: Allows relative module imports ('from core.fetcher import ...').
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Print sys.path in Python shell.
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# WHAT: Import core scraper and storage functions.
from core.fetcher import fetch_all_feeds
from core.storage import save_articles

# WHAT: Path constant for feed catalog configuration file.
CONFIG_PATH = PROJECT_ROOT / "config" / "feeds.json"


# WHAT: Runs automated headless RSS feed scraping without opening a graphical window (used by systemd timer).
# OPTIONS/VALUES: Reads config/feeds.json, fetches all enabled feeds, appends output to scraped_articles.jsonl, and exits cleanly.
# DEFAULTS: Exits with code 0 upon completion.
# OUTPUT/EFFECT: Prints progress and summary metrics to standard output.
# ERRORS/EDGE CASES: Prints error logs and exits safely if feeds file is missing or corrupt.
# HOW TO TEST: Run 'python3 main.py --headless' from terminal.
def run_headless_scrape() -> None:
    """Executes a headless CLI RSS feed scrape operation."""
    print("[RSS Scraper] Running in headless CLI mode...")

    if not CONFIG_PATH.exists():
        print(f"[ERROR] Configuration file not found at: {CONFIG_PATH}")
        sys.exit(0)

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            feeds = data.get("feeds", []) if isinstance(data, dict) else data
    except Exception as e:
        print(f"[ERROR] Failed to load feeds from {CONFIG_PATH}: {e}")
        sys.exit(1)

    enabled_feeds = [f for f in feeds if isinstance(f, dict) and f.get("enabled", True)]
    print(f"[RSS Scraper] Found {len(enabled_feeds)} enabled feed(s) out of {len(feeds)} total.")

    if not enabled_feeds:
        print("[RSS Scraper] No enabled feeds to scrape.")
        sys.exit(0)

    articles, errors = fetch_all_feeds(enabled_feeds)
    new_count, total_count = save_articles(articles)

    print(f"[SUMMARY] Scrape complete! {new_count} new article(s) added. Total stored articles: {total_count}.")

    if errors:
        print(f"[SUMMARY] Encountered {len(errors)} feed error(s):")
        for err in errors:
            print(f"  - {err.get('feed_name', 'Unknown')}: {err.get('error')}")

    sys.exit(0)


# WHAT: Main program entrypoint function that parses terminal flags and launches either CLI headless scrape mode or the PyQt6 GUI dashboard.
# OPTIONS/VALUES: Flags: '--headless', '--scrape', or no flags (GUI mode).
# DEFAULTS: Opens PyQt6 GUI window if desktop environment is detected; falls back to CLI scrape if headless.
# OUTPUT/EFFECT: Displays desktop app or executes background scrape.
# ERRORS/EDGE CASES: Auto-installs 12-hour systemd timer if inactive.
# HOW TO TEST: Run 'python3 main.py' or './RSS'.
def main() -> None:
    parser = argparse.ArgumentParser(description="RSS Feed Manager & Scraper")
    parser.add_argument("--headless", action="store_true", help="Run feed scraper in headless CLI mode")
    parser.add_argument("--scrape", action="store_true", help="Run immediate feed scrape in CLI mode and exit")
    args = parser.parse_args()

    if args.headless or args.scrape:
        run_headless_scrape()
        return

    # Check GUI environment
    display = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    if not display:
        print("[WARNING] No GUI display detected ($DISPLAY or $WAYLAND_DISPLAY not set).")
        print("[RSS Scraper] Falling back to headless CLI scrape mode.")
        run_headless_scrape()
        return

    # Launch PyQt6 GUI Application
    from PyQt6.QtWidgets import QApplication
    from gui.window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
