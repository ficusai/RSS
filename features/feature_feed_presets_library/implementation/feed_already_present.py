"""
Single-function module for checking duplicate feed existence.
"""
from typing import Any, Dict, List, Optional


def feed_already_present(preset: Dict[str, str], existing: Optional[List[Dict[str, Any]]] = None) -> bool:
    """Returns True if a preset URL/name already exists in the active feed list."""
    if existing is None:
        return False
    preset_url = (preset.get("url") or "").strip().rstrip("/")
    preset_name = (preset.get("name") or "").strip().lower()
    for feed in existing:
        feed_url = (feed.get("url") or "").strip().rstrip("/")
        feed_name = (feed.get("name") or "").strip().lower()
        if (preset_url and feed_url == preset_url) or (preset_name and feed_name == preset_name):
            return True
    return False
