"""Single-function module for reading storage statistics."""
import json
from typing import Any, Dict
from .paths import get_articles_file
from .ensure_dir import _ensure_dir
from .load_dedup_state import _load_dedup_state


def get_stats() -> Dict[str, Any]:
    """Returns stats such as total articles stored, total feeds, last scrape timestamp."""
    _ensure_dir()
    articles_file = get_articles_file()
    state = _load_dedup_state()

    total_articles = 0
    unique_feeds = set()

    if articles_file.exists():
        try:
            with open(articles_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        total_articles += 1
                        try:
                            item = json.loads(line)
                            feed_url = item.get("feed_url") or item.get("feed_name")
                            if feed_url:
                                unique_feeds.add(feed_url)
                        except Exception:
                            pass
        except Exception:
            pass

    return {
        "total_articles": total_articles,
        "dedup_count": len(state.get("seen_ids", {})),
        "total_feeds": len(unique_feeds),
        "last_scrape_timestamp": state.get("last_scrape_timestamp"),
        "storage_file_exists": articles_file.exists(),
        "storage_file_size_bytes": articles_file.stat().st_size if articles_file.exists() else 0,
    }
