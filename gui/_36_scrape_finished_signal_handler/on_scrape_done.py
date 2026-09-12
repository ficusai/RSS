"""Handle the completion signal from ScrapeThread."""
# WHAT: Re-enables the sync button, hides the progress bar, logs results,
#       updates stats, and refreshes the articles table.
# OPTIONS: window — MainWindow instance; new, total — article counts; errors — list of error dicts.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: UI returns to idle state; stats and articles refreshed.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: on_scrape_done(window, 5, 100, [])
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._13_stats_badges_update_live.update_stats_badges import update_stats_badges
from gui._18_articles_table_refresh_view.refresh_articles_table import refresh_articles_table


def on_scrape_done(window, new: int, total: int, errors: list) -> None:
    """Handle completion of the background scrape thread."""
    window.btn_sync.setEnabled(True)
    window.btn_sync.setText("🔄 Sync All Feeds")
    window.progress.setVisible(False)
    append_log_message(window, f"Scrape job complete: +{new} new article(s) added. Total database count: {total}.")
    if errors:
        append_log_message(window, f"Encountered {len(errors)} feed fetching issue(s).")
    update_stats_badges(window)
    refresh_articles_table(window)
