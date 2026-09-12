"""Configure and start a ScrapeThread, wiring signals to GUI slots."""
# WHAT: Creates ScrapeThread(feeds), connects log_signal → append_log_message,
#       finished_signal → on_scrape_done, disables the sync button, shows progress bar.
# OPTIONS: window — MainWindow instance; feeds — list of feed dicts.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Background thread started; UI updated to reflect running state.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: run_scrape(window, [...])
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._36_scrape_finished_signal_handler.on_scrape_done import on_scrape_done
from gui._02_background_scrape_thread_worker.scrape_thread_worker import ScrapeThread


def run_scrape(window, feeds) -> None:
    """Start the background scrape thread and wire signals."""
    window.btn_sync.setEnabled(False)
    window.btn_sync.setText("⏳ Syncing...")
    window.progress.setVisible(True)
    window.progress.setRange(0, 0)
    window.scrape_thread = ScrapeThread(feeds)
    window.scrape_thread.log_signal.connect(lambda msg: append_log_message(window, msg))
    window.scrape_thread.finished_signal.connect(lambda new, total, errors: on_scrape_done(window, new, total, errors))
    window.scrape_thread.start()
