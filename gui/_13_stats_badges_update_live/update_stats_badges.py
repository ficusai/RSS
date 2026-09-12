"""Update the article-count and feed-count badges in the header bar."""
# WHAT: Reads core.storage.get_stats() and updates window.lbl_articles_stat and window.lbl_feeds_stat.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: On exception, silently does nothing.
# OUTPUT/EFFECT: Header badge text updated.
# ERRORS/EDGE CASES: get_stats() may raise if storage is unavailable.
# HOW TO TEST: update_stats_badges(window); check lbl_articles_stat.text() contains "Articles"
from core.storage import get_stats


def update_stats_badges(window) -> None:
    """Update header stat badges from core.storage.get_stats()."""
    try:
        stats = get_stats()
        arts = stats.get("total_articles", 0)
        total = len(window.feeds)
        active = sum(1 for f in window.feeds if f.get("enabled", True))
        window.lbl_articles_stat.setText(f"📰 {arts} Articles")
        window.lbl_feeds_stat.setText(f"📡 {active}/{total} Feeds Active")
    except Exception:
        pass
