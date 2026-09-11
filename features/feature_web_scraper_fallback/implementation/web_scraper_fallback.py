"""
Web Page Scraper Fallback Module (Git Branch: feature/web-scraper-fallback)
"""
from .clean_html_simple import clean_html_simple
from .fetch_full_page_text import fetch_full_page_text

__all__ = [
    "clean_html_simple",
    "fetch_full_page_text",
]
