"""
Single-function module for filtering preset feeds by category.
"""
from typing import Dict, List
from .preset_data import PRESET_FEEDS
from .get_preset_feeds import get_preset_feeds


def get_presets_by_category(category: str) -> List[Dict[str, str]]:
    """Returns all preset feeds matching a category (case-insensitive)."""
    cat = (category or "").strip().lower()
    if not cat or cat == "all" or cat == "all categories":
        return get_preset_feeds()
    return [
        dict(feed)
        for feed in PRESET_FEEDS
        if (feed.get("category") or "").strip().lower() == cat
    ]
