"""Single-function module for estimating reading time."""

def calculate_reading_time_minutes(text: str, wpm: int = 200) -> int:
    """Estimates reading time in minutes based on word count."""
    if not text:
        return 1
    words = len(text.split())
    return max(1, round(words / wpm))
