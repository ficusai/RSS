"""Extractors package re-exporting single-function modules."""
from .extract_readability import extract_readability
from .extract_next_data import extract_next_data
from .extract_nuxt_data import extract_nuxt_data
from .extract_window_state import extract_window_state

__all__ = [
    "extract_readability",
    "extract_next_data",
    "extract_nuxt_data",
    "extract_window_state",
]
