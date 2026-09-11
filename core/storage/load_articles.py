"""Single-function module for reading and filtering stored articles."""
import json
from typing import Any, Dict, List
from .paths import get_articles_file
from .ensure_dir import _ensure_dir


def load_articles(
    limit: int = 200,
    offset: int = 0,
    category: str = "",
    feed_filter: str = "",
    search_query: str = "",
) -> List[Dict[str, Any]]:
    """Reads stored articles from scraped_articles.jsonl in reverse chronological order with filtering."""
    _ensure_dir()
    articles_file = get_articles_file()
    if not articles_file.exists():
        return []

    results = []
    query_lower = search_query.strip().lower()
    cat_lower = category.strip().lower()
    feed_lower = feed_filter.strip().lower()

    try:
        with open(articles_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in reversed(lines):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                item = json.loads(line_str)
            except Exception:
                continue

            if cat_lower and cat_lower != "all":
                item_cat = (item.get("category") or "General").lower()
                if cat_lower not in item_cat:
                    continue

            if feed_lower and feed_lower != "all":
                item_feed = (item.get("feed_name") or "").lower()
                if feed_lower not in item_feed:
                    continue

            if query_lower:
                title_match = query_lower in (item.get("title") or "").lower()
                text_match = query_lower in (item.get("text_clean") or "").lower()
                author_match = query_lower in (item.get("author") or "").lower()
                tags_str = " ".join(item.get("tags") or []).lower()
                tag_match = query_lower in tags_str
                if not (title_match or text_match or author_match or tag_match):
                    continue

            results.append(item)

    except Exception:
        pass

    start_idx = max(0, offset)
    end_idx = start_idx + limit
    return results[start_idx:end_idx]
