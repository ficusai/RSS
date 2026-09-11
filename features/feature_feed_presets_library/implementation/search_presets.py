"""
Single-function module for searching preset feeds by query text.
"""
from typing import Dict, List
from .preset_data import PRESET_FEEDS
from .get_preset_feeds import get_preset_feeds


def search_presets(query: str) -> List[Dict[str, str]]:
    """Returns preset feeds whose name/url/category match a text query."""
    q = (query or "").strip().lower()
    if not q:
        return get_preset_feeds()
    return [
        dict(feed)
        for feed in PRESET_FEEDS
        if q in (feed.get("name") or "").lower()
        or q in (feed.get("url") or "").lower()
        or q in (feed.get("category") or "").lower()
    ]
