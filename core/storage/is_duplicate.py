"""Single-function module for checking duplicate article IDs."""
from typing import Any, Dict, Optional
from .load_dedup_state import _load_dedup_state


def is_duplicate(article_id: str, state: Optional[Dict[str, Any]] = None) -> bool:
    """Checks if article_id is in the deduplication state."""
    if not article_id:
        return False
    st = state if state is not None else _load_dedup_state()
    return article_id in st.get("seen_ids", {})
