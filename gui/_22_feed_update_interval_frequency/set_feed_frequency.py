"""Update a feed's fetch interval in hours and persist."""
# WHAT: Sets feed["fetch_interval_hours"] = hours for the matching fid, then saves.
# OPTIONS: window — MainWindow instance; fid — feed ID; hours — int (1/3/6/12/24).
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Interval updated in window.feeds and on disk.
# ERRORS/EDGE CASES: None — silently skips if fid not found.
# HOW TO TEST: set_feed_frequency(window, "fid", 6)
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds


def set_feed_frequency(window, fid: str, hours) -> None:
    """Update the fetch interval for a feed by ID."""
    for f in window.feeds:
        if f.get("id") == fid:
            f["fetch_interval_hours"] = hours
            save_feeds(window)
            return
