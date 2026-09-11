#!/usr/bin/env python3
"""
Main entrypoint for RSS Feed Manager & Scraper.
Supports GUI mode (PyQt6) and CLI/headless mode (--headless, --scrape).
"""

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.run_headless_scrape import run_headless_scrape


def main() -> None:
    parser = argparse.ArgumentParser(description="RSS Feed Manager & Scraper")
    parser.add_argument("--headless", action="store_true", help="Run feed scraper in headless CLI mode")
    parser.add_argument("--scrape", action="store_true", help="Run immediate feed scrape in CLI mode and exit")
    args = parser.parse_args()

    if args.headless or args.scrape:
        run_headless_scrape()
        return

    display = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    if not display:
        print("[WARNING] No GUI display detected ($DISPLAY or $WAYLAND_DISPLAY not set).")
        print("[RSS Scraper] Falling back to headless CLI scrape mode.")
        run_headless_scrape()
        return

    from PyQt6.QtWidgets import QApplication
    from gui.window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
