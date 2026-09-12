"""Bulk-import all preset feeds that are not yet subscribed."""
# WHAT: Iterates get_preset_feeds(), skips duplicates, appends new ones, saves, and refreshes.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: New presets added to window.feeds; tables refreshed; info dialog shown.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: add_all_presets(window)
from PyQt6.QtWidgets import QMessageBox

from features.feature_feed_presets_library.implementation.feeds_presets import get_preset_feeds, feed_already_present
from gui._09_feed_identifier_generate_from_name.generate_feed_id import generate_feed_id
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds
from gui._16_refresh_all_views_pipeline.refresh_all_views import refresh_window
from gui._31_presets_table_refresh_view.refresh_presets_table import refresh_presets_table


def add_all_presets(window) -> None:
    """Bulk-import all unsubscribed preset feeds."""
    added = 0
    for preset in get_preset_feeds():
        if feed_already_present(preset, window.feeds):
            continue
        name = (preset.get("name") or "").strip()
        url = (preset.get("url") or "").strip()
        cat = (preset.get("category") or "General").strip()
        if not name or not url:
            continue
        fid = generate_feed_id(name, len(window.feeds))
        window.feeds.append(
            {"id": fid, "name": name, "url": url, "category": cat, "fetch_interval_hours": 12, "enabled": True}
        )
        added += 1
    if added:
        save_feeds(window)
        refresh_window(window)
        refresh_presets_table(window)
    append_log_message(window, f"Preset import complete: {added} new feed(s) added.")
    QMessageBox.information(window, "Presets Imported", f"Added {added} preset feed(s) to your subscriptions.")
