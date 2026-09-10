#!/usr/bin/env python3
"""
Main entrypoint for RSS Feed Manager & Scraper.
Supports GUI mode (PyQt6) and CLI/headless mode (--headless, --scrape).
"""

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.fetcher import fetch_all_feeds
from core.scheduler import get_timer_status, install_systemd_timer
from core.storage import save_articles

CONFIG_PATH = Path("/home/ficus-pro/Documents/RSS/config/feeds.json")


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

    # Auto-install background 12-hour timer if not active
    try:
        timer_status = get_timer_status()
        if not timer_status.get("active"):
            print("[RSS Scraper] Systemd timer is inactive. Automatically setting up 12-hour background timer...")
            install_systemd_timer()
    except Exception as e:
        print(f"[WARNING] Could not check or install systemd timer: {e}")

    # Launch PyQt6 GUI Application
    from PyQt6.QtWidgets import QApplication
    from gui.window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
