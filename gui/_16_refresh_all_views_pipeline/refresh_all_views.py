"""Orchestrate a full view refresh: subscriptions table, articles table, stats badges."""
# WHAT: Calls the three refresh functions in sequence.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: All three views updated.
# ERRORS/EDGE CASES: None — each sub-function handles its own errors.
# HOW TO TEST: refresh_window(window)
from gui._13_stats_badges_update_live.update_stats_badges import update_stats_badges
from gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table import refresh_subscriptions_table
from gui._18_articles_table_refresh_view.refresh_articles_table import refresh_articles_table


def refresh_window(window) -> None:
    """Refresh all display views: subscriptions, articles, and stats."""
    refresh_subscriptions_table(window)
    refresh_articles_table(window)
    update_stats_badges(window)
