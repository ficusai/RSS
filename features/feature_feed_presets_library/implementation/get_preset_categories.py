"""
Single-function module for retrieving preset categories.
"""
from typing import List
from .preset_data import PRESET_CATEGORIES


def get_preset_categories() -> List[str]:
    """Returns an ordered copy of all preset categories."""
    return list(PRESET_CATEGORIES)
