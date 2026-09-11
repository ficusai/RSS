"""
Pre-Configured Feed Presets Library (Git Branch: feature/feed-presets-library)

Provides curated preset RSS/Atom feed subscriptions across multiple industry categories.
"""

from typing import Any, Dict, List

PRESET_FEEDS: List[Dict[str, str]] = [
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"},
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss", "category": "Tech News"},
    {"name": "Federal Reserve", "url": "https://www.federalreserve.gov/feeds/press_all.xml", "category": "Central Banks"},
    {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/rss.xml", "category": "World News"},
    {"name": "Ars Technica", "url": "http://feeds.arstechnica.com/arstechnica/index", "category": "Technology"},
    {"name": "Financial Times", "url": "https://www.ft.com/rss/home", "category": "Finance"},
    {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "category": "Crypto"},
]


def get_preset_feeds() -> List[Dict[str, str]]:
    """Returns copy of predefined feed list."""
    return list(PRESET_FEEDS)
