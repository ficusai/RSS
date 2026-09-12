"""Validate enabled feeds and launch a full background scrape."""
# WHAT: Checks that at least one feed is enabled and a scrape is not already running,
#       then calls run_scrape(window, window.feeds).
# OPTIONS: window — MainWindow instance.
# DEFAULTS: No-op if scrape already running or no enabled feeds.
# OUTPUT/EFFECT: Background scrape launched; button text/progress bar updated.
# ERRORS/EDGE CASES: Shows QMessageBox if no enabled feeds.
# HOW TO TEST: start_scrape(window)
from PyQt6.QtWidgets import QMessageBox

from gui._35_scrape_run_background_orchestrator.run_scrape_background import run_scrape


def start_scrape(window) -> None:
    """Start a full background scrape of all enabled feeds."""
    if window.scrape_thread and window.scrape_thread.isRunning():
        return
    enabled = [f for f in window.feeds if f.get("enabled")]
    if not enabled:
        QMessageBox.information(window, "No Active Subscriptions", "Please enable at least one feed to sync.")
        return
    run_scrape(window, window.feeds)
