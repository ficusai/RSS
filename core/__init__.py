"""
Core package for RSS Feed Scraper system.
"""
# WHAT: Package initialization file for the 'core' directory.
# This file marks the 'core' folder as a Python package, allowing other scripts
# to import modules and helper functions from the core backend logic.
# OPTIONS/VALUES: N/A (Python package marker file).
# DEFAULTS: Exposes selected core utility functions at the package root level.
# OUTPUT/EFFECT: Enables clean imports such as 'from core import clean_html'.
# ERRORS/EDGE CASES: If missing functions are imported, an ImportError is raised.
# HOW TO TEST: Run 'python3 -c "import core; print(dir(core))"' in terminal.

from .cleaner import clean_html, parse_to_iso
from .storage import generate_article_id, is_duplicate, save_articles, get_stats
from .fetcher import fetch_feed, fetch_all_feeds
from .cache import CacheManager

__all__ = [
    "clean_html",
    "parse_to_iso",
    "generate_article_id",
    "is_duplicate",
    "save_articles",
    "get_stats",
    "fetch_feed",
    "fetch_all_feeds",
    "CacheManager",
]
