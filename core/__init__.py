"""
Core package for RSS Feed Scraper system.
"""

from .cleaner import clean_html, parse_to_iso
from .storage import generate_article_id, is_duplicate, save_articles, get_stats
from .fetcher import fetch_feed, fetch_all_feeds
from .scheduler import install_systemd_timer, get_timer_status

__all__ = [
    "clean_html",
    "parse_to_iso",
    "generate_article_id",
    "is_duplicate",
    "save_articles",
    "get_stats",
    "fetch_feed",
    "fetch_all_feeds",
    "install_systemd_timer",
    "get_timer_status",
]
