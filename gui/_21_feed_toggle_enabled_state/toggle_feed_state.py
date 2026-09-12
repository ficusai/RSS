"""Toggle a feed's enabled state by ID and persist."""
# WHAT: Sets feed["enabled"] = on, saves, and refreshes stats.
# OPTIONS: window — MainWindow instance; fid — feed ID; on — bool.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Feed toggled; stats badges updated.
# ERRORS/EDGE CASES: None — silently skips if fid not found.
# HOW TO TEST: toggle_feed(window, "fid", False)
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds
from gui._13_stats_badges_update_live.update_stats_badges import update_stats_badges


def toggle_feed(window, fid: str, on: bool) -> None:
    """Toggle enabled state of a feed and persist."""
    for f in window.feeds:
        if f.get("id") == fid:
            f["enabled"] = on
            save_feeds(window)
            update_stats_badges(window)
            return
