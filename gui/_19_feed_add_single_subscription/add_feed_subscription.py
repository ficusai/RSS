"""Add a single subscription from the drawer form."""
# WHAT: Reads window.in_name / window.in_url / window.in_cat / window.cb_freq,
#       validates, generates a feed ID, appends to window.feeds, saves, and refreshes.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: Category defaults to "General"; interval from cb_freq index.
# OUTPUT/EFFECT: window.feeds updated; tables refreshed; log message appended.
# ERRORS/EDGE CASES: Missing name or URL shows warning; duplicate URL/name logged.
# HOW TO TEST: add_feed(window) after filling the form fields
from PyQt6.QtWidgets import QMessageBox

from gui._09_feed_identifier_generate_from_name.generate_feed_id import generate_feed_id
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds
from gui._16_refresh_all_views_pipeline.refresh_all_views import refresh_window


def add_feed(window) -> None:
    """Add a feed from the drawer form fields."""
    name = window.in_name.text().strip()
    url = window.in_url.text().strip()
    cat = window.in_cat.text().strip() or "General"
    h = [1, 3, 6, 12, 24][window.cb_freq.currentIndex()]

    if not name or not url:
        QMessageBox.warning(window, "Missing Fields", "Both Feed Name and Feed URL are required.")
        return
    if not url.startswith("http"):
        url = "https://" + url

    for existing in window.feeds:
        if existing.get("url", "").rstrip("/") == url.rstrip("/"):
            append_log_message(window, f"Feed already subscribed: {name}")
            window.in_name.clear()
            window.in_url.clear()
            return

    fid = generate_feed_id(name, len(window.feeds))
    window.feeds.append({"id": fid, "name": name, "url": url, "category": cat, "fetch_interval_hours": h, "enabled": True})
    save_feeds(window)
    refresh_window(window)
    append_log_message(window, f"Successfully subscribed to feed: {name}")
    window.in_name.clear()
    window.in_url.clear()
