"""Single-function module for generating SHA-256 article IDs."""
import hashlib
from datetime import datetime, timezone


def generate_article_id(feed_url: str, item_link: str, item_title: str, item_guid: str) -> str:
    """Returns a SHA256 hex string based on link + title or guid."""
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
