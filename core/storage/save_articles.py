"""Single-function module for appending non-duplicate articles to JSONL storage."""
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple
from .paths import get_articles_file
from .ensure_dir import _ensure_dir
from .load_dedup_state import _load_dedup_state
from .save_dedup_state import _save_dedup_state
from .generate_article_id import generate_article_id


def save_articles(articles: List[Dict[str, Any]]) -> Tuple[int, int]:
    """Appends non-duplicate articles to JSONL file and updates dedup_state.json."""
    _ensure_dir()
    articles_file = get_articles_file()
    state = _load_dedup_state()
    seen_ids: Dict[str, Any] = state.get("seen_ids", {})

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_articles = []
    update_map = {}

    existing_records = {}
    if articles_file.exists():
        try:
            with open(articles_file, "r", encoding="utf-8") as f:
                for line in f:
                    line_str = line.strip()
                    if line_str:
                        try:
                            item = json.loads(line_str)
                            aid = item.get("article_id")
                            if aid:
                                existing_records[aid] = item
                        except Exception:
                            pass
        except Exception:
            pass

    for art in articles:
        art_id = art.get("article_id")
        if not art_id:
            art_id = generate_article_id(
                art.get("feed_url", ""),
                art.get("url", ""),
                art.get("title", ""),
                art.get("guid", "")
            )
            art["article_id"] = art_id

        if art_id not in seen_ids:
            seen_ids[art_id] = now_iso
            new_articles.append(art)
            existing_records[art_id] = art
        elif art_id in existing_records:
            old_art = existing_records[art_id]
            old_len = len(old_art.get("text_clean") or "")
            new_len = len(art.get("text_clean") or "")
            missing_preview = not old_art.get("preview") and art.get("preview")

            if new_len > old_len or missing_preview:
                existing_records[art_id] = art
                update_map[art_id] = art

    if update_map:
        temp_file = articles_file.with_suffix(".jsonl.tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            for aid, record in existing_records.items():
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        temp_file.replace(articles_file)
    elif new_articles:
        with open(articles_file, "a", encoding="utf-8") as f:
            for art in new_articles:
                f.write(json.dumps(art, ensure_ascii=False) + "\n")

    state["seen_ids"] = seen_ids
    state["last_scrape_timestamp"] = now_iso
    state["total_scraped"] = len(seen_ids)
    _save_dedup_state(state)

    total_seen = len(seen_ids)
    return len(new_articles) + len(update_map), total_seen
