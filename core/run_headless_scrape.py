"""Single-function module for executing headless CLI feed scraping."""
import json
import sys
from pathlib import Path
from core.fetcher import fetch_all_feeds
from core.storage import save_articles

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "feeds.json"


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

    articles, errors = fetch_all_feeds(enabled_feeds, extract_full_text=True)
    new_count, total_count = save_articles(articles)

    print(f"[SUMMARY] Scrape complete! {new_count} new article(s) added. Total stored articles: {total_count}.")

    if errors:
        print(f"[SUMMARY] Encountered {len(errors)} feed error(s):")
        for err in errors:
            print(f"  - {err.get('feed_name', 'Unknown')}: {err.get('error')}")

    sys.exit(0)
