"""Single-function module for loading deduplication state."""
import json
from typing import Any, Dict
from .paths import get_dedup_file
from .ensure_dir import _ensure_dir


def _load_dedup_state() -> Dict[str, Any]:
    """Loads deduplication state from dedup_state.json."""
    _ensure_dir()
    dedup_file = get_dedup_file()
    if not dedup_file.exists():
        return {"seen_ids": {}, "last_scrape_timestamp": None, "total_scraped": 0}
    try:
        with open(dedup_file, "r", encoding="utf-8") as f:
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
