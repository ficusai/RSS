"""
Storage and deduplication engine for RSS feed articles.
"""

# WHAT: Standard Python library for computing cryptographic hash fingerprints (SHA-256) of article text to assign unique IDs.
# OPTIONS/VALUES: hashlib.sha256().hexdigest().
# DEFAULTS: Standard library module.
# OUTPUT/EFFECT: Generates fixed 64-character hash strings for unique article identification.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "import hashlib; print(hashlib.sha256(b\"test\").hexdigest())"'.
import hashlib

# WHAT: Standard JSON library for converting Python dictionaries into formatted text files and back.
# OPTIONS/VALUES: json.dumps(), json.loads(), json.dump(), json.load().
# DEFAULTS: Handles UTF-8 encoding.
# OUTPUT/EFFECT: Reads/writes JSON files (dedup_state.json and scraped_articles.jsonl).
# ERRORS/EDGE CASES: Throws json.JSONDecodeError if JSON file is corrupted.
# HOW TO TEST: Run 'python3 -c "import json; print(json.dumps({\"a\": 1}))"'.
import json

# WHAT: Datetime utilities for tracking UTC scraping timestamps.
# OPTIONS/VALUES: datetime.now(timezone.utc).
# DEFAULTS: Uses Coordinated Universal Time (UTC).
# OUTPUT/EFFECT: Stores ISO timestamp strings in the database state.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat())"'.
from datetime import datetime, timezone

# WHAT: Path library for manipulating folder and file path strings cleanly across operating systems.
# OPTIONS/VALUES: PROJECT_ROOT / "SCRAPED-RESULTS".
# DEFAULTS: Uses absolute file system path.
# OUTPUT/EFFECT: Resolves data folder locations.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "from pathlib import Path; print(Path.home())"'.
from pathlib import Path

# WHAT: Type annotation hints to clarify function arguments and return types.
# OPTIONS/VALUES: Any, Dict, List, Optional, Tuple.
# DEFAULTS: Purely for static type checkers like mypy (does not change runtime execution).
# OUTPUT/EFFECT: Improves code readability and developer tooling.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Checked by static analysis tools.
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "SCRAPED-RESULTS"
ARTICLES_FILE = RESULTS_DIR / "scraped_articles.jsonl"
DEDUP_FILE = RESULTS_DIR / "dedup_state.json"


# WHAT: Internal helper function that creates the output folder if it does not already exist.
# OPTIONS/VALUES: None.
# DEFAULTS: Creates parents and ignores existing folder error (exist_ok=True).
# OUTPUT/EFFECT: Ensures SCRAPED-RESULTS directory exists within project root.
# ERRORS/EDGE CASES: Raises PermissionError if write permission is denied.
# HOW TO TEST: Call _ensure_dir() and verify folder existence with os.path.exists().
def _ensure_dir() -> None:
    """Ensures that the output storage directory exists."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# WHAT: Generates a unique 64-character SHA-256 hex string ID for an article based on feed URL, link, title, or GUID.
# OPTIONS/VALUES: Input strings: feed_url, item_link, item_title, item_guid.
# DEFAULTS: Falls back to feed_url + current ISO timestamp if title and link are empty.
# OUTPUT/EFFECT: Returns 64-character SHA-256 hexadecimal string.
# ERRORS/EDGE CASES: Handles empty or None parameters gracefully by stripping and formatting fallback keys.
# HOW TO TEST: Run 'python3 -c "from core.storage import generate_article_id; print(generate_article_id(\"http://test.com\", \"http://test.com/1\", \"Title\", \"guid123\"))"'.
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


# WHAT: Internal helper function that reads dedup_state.json from disk into a Python dictionary.
# OPTIONS/VALUES: Returns dict with keys: 'seen_ids', 'last_scrape_timestamp', 'total_scraped'.
# DEFAULTS: Returns empty state dict if file does not exist or fails to parse.
# OUTPUT/EFFECT: Loads deduplication history into memory.
# ERRORS/EDGE CASES: Catches file missing, corrupted JSON syntax, or invalid data types safely.
# HOW TO TEST: Call _load_dedup_state() in Python shell.
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


# WHAT: Internal helper function that atomically writes the updated deduplication dictionary to dedup_state.json.
# OPTIONS/VALUES: Takes state dictionary.
# DEFAULTS: Writes formatted JSON with indent=2.
# OUTPUT/EFFECT: Updates dedup_state.json on disk safely using a temporary file replacement.
# ERRORS/EDGE CASES: Uses temporary file atomic rename to prevent file corruption if app crashes mid-write.
# HOW TO TEST: Pass test dictionary to _save_dedup_state() and verify file updates.
def _save_dedup_state(state: Dict[str, Any]) -> None:
    """Saves deduplication state atomically to dedup_state.json."""
    _ensure_dir()
    temp_file = DEDUP_FILE.with_suffix(".json.tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    temp_file.replace(DEDUP_FILE)


# WHAT: Checks whether a specific article ID hash has already been saved previously.
# OPTIONS/VALUES: Input article_id string, optional preloaded state dict.
# DEFAULTS: Returns False if article_id is empty or missing.
# OUTPUT/EFFECT: Returns True if article was already scraped, False if new.
# ERRORS/EDGE CASES: Returns False for empty strings.
# HOW TO TEST: Run 'python3 -c "from core.storage import is_duplicate; print(is_duplicate(\"non_existent_hash\"))"'.
def is_duplicate(article_id: str, state: Optional[Dict[str, Any]] = None) -> bool:
    """
    Checks if article_id is in the deduplication state. Accepts optional preloaded state dict.
    """
    if not article_id:
        return False
    st = state if state is not None else _load_dedup_state()
    return article_id in st.get("seen_ids", {})


# WHAT: Main storage function that filters out duplicate articles, appends new ones to scraped_articles.jsonl, and updates dedup_state.json.
# OPTIONS/VALUES: Input list of article dictionaries.
# DEFAULTS: Appends single line JSON string per new article.
# OUTPUT/EFFECT: Returns tuple (new_articles_count, total_seen_count).
# ERRORS/EDGE CASES: Creates files automatically if missing; skips duplicate articles cleanly.
# HOW TO TEST: Call save_articles([sample_article_dict]) and check return counts.
def save_articles(articles: List[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Appends non-duplicate articles to JSONL file and updates dedup_state.json.
    Updates existing records if incoming article has complete text content missing in stored record.
    Returns (new_articles_count, total_seen_count).
    """
    _ensure_dir()
    state = _load_dedup_state()
    seen_ids: Dict[str, Any] = state.get("seen_ids", {})

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_articles = []
    update_map = {}

    # Load existing articles if file exists to check for incomplete records
    existing_records = {}
    if ARTICLES_FILE.exists():
        try:
            with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
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
                art.get("article_id", "")
            )
            art["article_id"] = art_id

        if art_id not in seen_ids:
            seen_ids[art_id] = now_iso
            new_articles.append(art)
            existing_records[art_id] = art
        elif art_id in existing_records:
            # Check if incoming art has richer content or new preview/full_text_clean fields
            old_art = existing_records[art_id]
            old_len = len(old_art.get("text_clean") or "")
            new_len = len(art.get("text_clean") or "")
            missing_preview = not old_art.get("preview") and art.get("preview")

            if new_len > old_len or missing_preview:
                existing_records[art_id] = art
                update_map[art_id] = art

    if update_map:
        # Rewrite file atomically with updated records and new articles
        temp_file = ARTICLES_FILE.with_suffix(".jsonl.tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            for aid, record in existing_records.items():
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        temp_file.replace(ARTICLES_FILE)
    elif new_articles:
        with open(ARTICLES_FILE, "a", encoding="utf-8") as f:
            for art in new_articles:
                f.write(json.dumps(art, ensure_ascii=False) + "\n")

    state["seen_ids"] = seen_ids
    state["last_scrape_timestamp"] = now_iso
    state["total_scraped"] = len(seen_ids)
    _save_dedup_state(state)

    total_seen = len(seen_ids)
    return len(new_articles) + len(update_map), total_seen


# WHAT: Reads storage metrics and returns a summary dictionary for the GUI dashboard.
# OPTIONS/VALUES: Returns dict with keys: total_articles, dedup_count, total_feeds, last_scrape_timestamp, storage_file_exists, storage_file_size_bytes.
# DEFAULTS: Returns 0 for counts if files do not exist.
# OUTPUT/EFFECT: Supplies statistical counters to the PyQt6 user interface.
# ERRORS/EDGE CASES: Gracefully handles missing output files without throwing errors.
# HOW TO TEST: Run 'python3 -c "from core.storage import get_stats; print(get_stats())"'.
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


# WHAT: Loads stored articles from JSONL database file with support for filtering, searching, and pagination.
# OPTIONS/VALUES: Arguments: limit, offset, category filter, feed filter, keyword search string.
# DEFAULTS: Limit 200 items, reverse chronological order (newest first).
# OUTPUT/EFFECT: Returns list of matching article dictionaries.
# ERRORS/EDGE CASES: Returns empty list if storage file does not exist or fails to parse.
# HOW TO TEST: Run 'python3 -c "from core.storage import load_articles; print(len(load_articles()))"'.
def load_articles(
    limit: int = 200,
    offset: int = 0,
    category: str = "",
    feed_filter: str = "",
    search_query: str = "",
) -> List[Dict[str, Any]]:
    """
    Reads stored articles from scraped_articles.jsonl in reverse chronological order with filtering.
    """
    _ensure_dir()
    if not ARTICLES_FILE.exists():
        return []

    results = []
    query_lower = search_query.strip().lower()
    cat_lower = category.strip().lower()
    feed_lower = feed_filter.strip().lower()

    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Reverse so newest articles come first
        for line in reversed(lines):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                item = json.loads(line_str)
            except Exception:
                continue

            # Category filter
            if cat_lower and cat_lower != "all":
                item_cat = (item.get("category") or "General").lower()
                if cat_lower not in item_cat:
                    continue

            # Feed filter
            if feed_lower and feed_lower != "all":
                item_feed = (item.get("feed_name") or "").lower()
                if feed_lower not in item_feed:
                    continue

            # Search query (matches title, text_clean, author, or tags)
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

    # Pagination slice
    start_idx = max(0, offset)
    end_idx = start_idx + limit
    return results[start_idx:end_idx]
