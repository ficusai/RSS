"""
GUI Reader Pro Components (Git Branch: feature/gui-reader-pro)

Provides category color badging definitions, article reading time estimation,
and clipboard integration handlers for PyQt6.
"""


def get_category_color(category_name: str) -> str:
    """Returns hex color code badge for a category."""
    cat = (category_name or "").lower()
    if "tech" in cat:
        return "#58a6ff"
    elif "finan" in cat or "econ" in cat or "bank" in cat:
        return "#3fb950"
    elif "news" in cat or "world" in cat:
        return "#d29922"
    return "#a371f7"


def calculate_reading_time_minutes(text: str, wpm: int = 200) -> int:
    """Estimates reading time in minutes based on word count."""
    if not text:
        return 1
    words = len(text.split())
    return max(1, round(words / wpm))
