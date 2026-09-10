"""
Storage and deduplication engine for RSS feed articles.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

RESULTS_DIR = Path("/home/ficus-pro/Documents/RSS/SCRAPED-RESULTS")
ARTICLES_FILE = RESULTS_DIR / "scraped_articles.jsonl"
DEDUP_FILE = RESULTS_DIR / "dedup_state.json"


def _ensure_dir() -> None:
    """Ensures that the output storage directory exists."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_article_id(feed_url: str, item_link: str, item_title: str, item_guid: str) -> str:
    """
    Returns a SHA256 hex string based on link + title or guid.
    """
    guid_clean = (item_guid or "").strip()
    link_clean = (item_link or "").strip()
    title_clean = (item_title or "").strip()
    feed_clean = (feed_url or "").strip()

    if guid_clean:
        raw_key = f"{feed_clean}|{guid_clean}"
    elif link_clean or title_clean:
        raw_key = f"{feed_clean}|{link_clean}|{title_clean}"
    else:
        raw_key = f"{feed_clean}|{datetime.now(timezone.utc).isoformat()}"

    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def _load_dedup_state() -> Dict[str, Any]:
    """Loads deduplication state from dedup_state.json."""
    _ensure_dir()
    if not DEDUP_FILE.exists():
        return {"seen_ids": {}, "last_scrape_timestamp": None, "total_scraped": 0}
    try:
        with open(DEDUP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                seen_ids = data.get("seen_ids", {})
                if isinstance(seen_ids, list):
                    data["seen_ids"] = {i: None for i in seen_ids}
                elif not isinstance(seen_ids, dict):
                    data["seen_ids"] = {}
                return data
    except Exception:
        pass
    return {"seen_ids": {}, "last_scrape_timestamp": None, "total_scraped": 0}


def _save_dedup_state(state: Dict[str, Any]) -> None:
    """Saves deduplication state atomically to dedup_state.json."""
    _ensure_dir()
    temp_file = DEDUP_FILE.with_suffix(".json.tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    temp_file.replace(DEDUP_FILE)


def is_duplicate(article_id: str) -> bool:
    """
    Checks if article_id is in the deduplication state.
    """
    if not article_id:
        return False
    state = _load_dedup_state()
    return article_id in state.get("seen_ids", {})


def save_articles(articles: List[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Appends non-duplicate articles to JSONL file and updates dedup_state.json.
    Returns (new_articles_count, total_seen_count).
    """
    _ensure_dir()
    state = _load_dedup_state()
    seen_ids: Dict[str, Any] = state.get("seen_ids", {})

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_articles = []

    for art in articles:
        art_id = art.get("article_id")
        if not art_id:
            art_id = generate_article_id(
                art.get("feed_url", ""),
                art.get("url", ""),
                art.get("title", ""),
                art.get("article_id", "")
            )
            art["article_id"] = art_id

        if art_id not in seen_ids:
            seen_ids[art_id] = now_iso
            new_articles.append(art)

    if new_articles:
        with open(ARTICLES_FILE, "a", encoding="utf-8") as f:
            for art in new_articles:
                f.write(json.dumps(art, ensure_ascii=False) + "\n")

    state["seen_ids"] = seen_ids
    state["last_scrape_timestamp"] = now_iso
    state["total_scraped"] = state.get("total_scraped", 0) + len(new_articles)
    _save_dedup_state(state)

    total_seen = len(seen_ids)
    return len(new_articles), total_seen


def get_stats() -> Dict[str, Any]:
    """
    Returns stats such as total articles stored, total feeds, last scrape timestamp.
    """
    _ensure_dir()
    state = _load_dedup_state()

    total_articles = 0
    unique_feeds = set()

    if ARTICLES_FILE.exists():
        try:
            with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
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
        "storage_file_exists": ARTICLES_FILE.exists(),
        "storage_file_size_bytes": ARTICLES_FILE.stat().st_size if ARTICLES_FILE.exists() else 0,
    }
