"""Add a single preset feed to the subscriptions list."""
# WHAT: Checks for duplicates, generates a feed ID, appends to window.feeds, saves, and refreshes.
# OPTIONS: window — MainWindow instance; preset — dict with name/url/category keys.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Preset added to window.feeds; tables refreshed.
# ERRORS/EDGE CASES: Skips silently if preset already subscribed.
# HOW TO TEST: add_preset_feed(window, {"name": "...", "url": "...", "category": "..."})
from features.feature_feed_presets_library.implementation.feeds_presets import feed_already_present
from gui._09_feed_identifier_generate_from_name.generate_feed_id import generate_feed_id
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds


def add_preset_feed(window, preset) -> None:
    """Add a single preset feed to subscriptions."""
    if feed_already_present(preset, window.feeds):
        append_log_message(window, f"Preset already subscribed: {preset.get('name')}")
        return
    name = (preset.get("name") or "").strip()
    url = (preset.get("url") or "").strip()
    cat = (preset.get("category") or "General").strip()
    if not name or not url:
        return
    fid = generate_feed_id(name, len(window.feeds))
    window.feeds.append(
        {"id": fid, "name": name, "url": url, "category": cat, "fetch_interval_hours": 12, "enabled": True}
    )
    save_feeds(window)
    from gui._16_refresh_all_views_pipeline.refresh_all_views import refresh_window
    from gui._31_presets_table_refresh_view.refresh_presets_table import refresh_presets_table
    refresh_window(window)
    refresh_presets_table(window)
    append_log_message(window, f"Subscribed preset feed: {name}")
