"""Ping a single feed endpoint immediately (single-feed scrape)."""
# WHAT: Runs _run_scrape on a list containing only the target feed.
# OPTIONS: window — MainWindow instance; fid — feed ID.
# DEFAULTS: Silently returns if feed not found or scrape already running.
# OUTPUT/EFFECT: Background thread started for single feed; log messages emitted.
# ERRORS/EDGE CASES: Skips if scrape_thread is already running.
# HOW TO TEST: ping_feed(window, "some-fid")
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._35_scrape_run_background_orchestrator.run_scrape_background import run_scrape


def ping_feed(window, fid: str) -> None:
    """Start a single-feed scrape for the feed matching fid."""
    target = next((f for f in window.feeds if f.get("id") == fid), None)
    if not target:
        return
    if window.scrape_thread and window.scrape_thread.isRunning():
        return
    append_log_message(window, f"Pinging RSS feed endpoint: {target['name']} ({target['url']})")
    run_scrape(window, [target])
