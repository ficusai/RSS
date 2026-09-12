"""Remove a subscription from window.feeds by its ID."""
# WHAT: Finds the feed with matching fid, removes it, saves, and refreshes all views.
# OPTIONS: window — MainWindow instance; fid — feed ID string.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: feed removed from window.feeds; tables/stats refreshed.
# ERRORS/EDGE CASES: None — silently skips if fid not found.
# HOW TO TEST: delete_feed(window, "some-fid")
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds


def delete_feed(window, fid: str) -> None:
    """Delete a feed subscription by ID."""
    for i, f in enumerate(window.feeds):
        if f.get("id") == fid:
            removed_name = f.get("name")
            window.feeds.pop(i)
            save_feeds(window)
            from gui._16_refresh_all_views_pipeline.refresh_all_views import refresh_window
            refresh_window(window)
            append_log_message(window, f"Unsubscribed feed: {removed_name}")
            return
