"""Single-function module for saving deduplication state atomically."""
import json
from typing import Any, Dict
from .paths import get_dedup_file
from .ensure_dir import _ensure_dir


def _save_dedup_state(state: Dict[str, Any]) -> None:
    """Saves deduplication state atomically to dedup_state.json."""
    _ensure_dir()
    dedup_file = get_dedup_file()
    temp_file = dedup_file.with_suffix(".json.tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    temp_file.replace(dedup_file)
