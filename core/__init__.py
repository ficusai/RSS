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

# WHAT: Imports HTML cleaning and date standardizing functions from the local cleaner module.
# OPTIONS/VALUES: Imports 'clean_html' (strips HTML tags) and 'parse_to_iso' (converts dates to ISO UTC format).
# DEFAULTS: Functions are imported into the core package scope.
# OUTPUT/EFFECT: Makes 'clean_html' and 'parse_to_iso' directly accessible from 'core'.
# ERRORS/EDGE CASES: ImportError if cleaner.py is missing or contains syntax errors.
# HOW TO TEST: Run 'python3 -c "from core import clean_html, parse_to_iso"'.
from .cleaner import clean_html, parse_to_iso

# WHAT: Imports article storage and management functions from the local storage module.
# OPTIONS/VALUES: Imports 'generate_article_id' (creates unique hashes), 'is_duplicate' (checks existing articles),
# 'save_articles' (writes data to database), and 'get_stats' (retrieves database summary metrics).
# DEFAULTS: Exposes database operations at the core package level.
# OUTPUT/EFFECT: Provides access to database reading and writing capabilities.
# ERRORS/EDGE CASES: ImportError if storage.py is missing or database helper functions fail to load.
# HOW TO TEST: Run 'python3 -c "from core import save_articles, get_stats"'.
from .storage import generate_article_id, is_duplicate, save_articles, get_stats

# WHAT: Imports RSS network downloader functions from the local fetcher module.
# OPTIONS/VALUES: Imports 'fetch_feed' (downloads a single RSS feed URL) and 'fetch_all_feeds' (downloads all saved feeds).
# DEFAULTS: Network fetching utilities exposed at core package root.
# OUTPUT/EFFECT: Allows downloading of web feed contents.
# ERRORS/EDGE CASES: ImportError if fetcher.py is missing.
# HOW TO TEST: Run 'python3 -c "from core import fetch_feed, fetch_all_feeds"'.
from .fetcher import fetch_feed, fetch_all_feeds

# WHAT: Imports Linux background task scheduler functions from the local scheduler module.
# OPTIONS/VALUES: Imports 'install_systemd_timer' (sets up periodic background background downloads)
# and 'get_timer_status' (checks if systemd timer is active or inactive).
# DEFAULTS: Scheduler utilities exposed at core package level.
# OUTPUT/EFFECT: Controls automatic background feed updating via systemd.
# ERRORS/EDGE CASES: ImportError if scheduler.py is missing.
# HOW TO TEST: Run 'python3 -c "from core import install_systemd_timer, get_timer_status"'.
from .scheduler import install_systemd_timer, get_timer_status

# WHAT: Defines '__all__', the explicit public list of function names exposed when executing 'from core import *'.
# OPTIONS/VALUES: A list of strings containing function names: "clean_html", "parse_to_iso", "generate_article_id",
# "is_duplicate", "save_articles", "get_stats", "fetch_feed", "fetch_all_feeds", "install_systemd_timer", "get_timer_status".
# DEFAULTS: Explicitly controls exported symbols during wildcard imports.
# OUTPUT/EFFECT: Restricts public exports to only the listed 10 function names.
# ERRORS/EDGE CASES: Typos in function names cause AttributeError during wildcard imports.
# HOW TO TEST: Run 'python3 -c "import core; print(core.__all__)"'.
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
