"""
Pre-Configured Feed Presets Library (Git Branch: feature/feed-presets-library)

475 curated RSS/Atom feed subscriptions across 22 industry
categories, re-exporting dedicated single-function modules.
"""

from .preset_data import PRESET_CATEGORIES, PRESET_FEEDS
from .get_preset_feeds import get_preset_feeds
from .get_preset_categories import get_preset_categories
from .get_presets_by_category import get_presets_by_category
from .search_presets import search_presets
from .feed_already_present import feed_already_present

__all__ = [
    "PRESET_CATEGORIES",
    "PRESET_FEEDS",
    "get_preset_feeds",
    "get_preset_categories",
    "get_presets_by_category",
    "search_presets",
    "feed_already_present",
]
