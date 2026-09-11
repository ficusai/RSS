"""
Single-function module for retrieving full preset feed catalog.
"""
from typing import Dict, List
from .preset_data import PRESET_FEEDS


def get_preset_feeds() -> List[Dict[str, str]]:
    """Returns a copy of the full preset feed catalog."""
    return [dict(feed) for feed in PRESET_FEEDS]
