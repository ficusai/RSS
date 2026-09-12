"""Install and enable the systemd background timer, then refresh status."""
# WHAT: Calls install_systemd_timer(); shows success/failure dialog and logs result.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Timer installed (if successful); status badges refreshed; dialog shown.
# ERRORS/EDGE CASES: install_systemd_timer() may return False.
# HOW TO TEST: handle_install_systemd(window)
from PyQt6.QtWidgets import QMessageBox

from features.feature_systemd_scheduler.implementation.scheduler import install_systemd_timer
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import refresh_systemd_status


def handle_install_systemd(window) -> None:
    """Install the systemd timer and show result dialog."""
    ok = install_systemd_timer()
    if ok:
        append_log_message(window, "Successfully installed and launched systemd user timer (rss-scraper.timer).")
        QMessageBox.information(
            window,
            "Systemd Timer Installed",
            "Systemd background timer installed and started successfully!\n"
            "Feed scraper will execute automatically every 12 hours.",
        )
    else:
        append_log_message(window, "Failed to install systemd user timer.")
        QMessageBox.critical(
            window,
            "Installation Failed",
            "Unable to install systemd user units. Check system logs for details.",
        )
    refresh_systemd_status(window)
