"""Single-function module for executing dual-tier feed fetching."""
import urllib.error
from typing import Any, Dict, List
from core.stealth import fetch_with_stealth_browser, is_stealth_available
from .fetch_url_bytes import fetch_url_bytes
from .parse_xml_bytes import parse_xml_bytes


def fetch_feed(feed_config: Dict[str, Any], extract_full_text: bool = False, timeout: int = 10) -> List[Dict[str, Any]]:
    """Fetches and parses a single RSS or Atom feed using dual-engine approach."""
    url = feed_config.get("url")
    if not url:
        return []

    raw_data = None
    last_error = None

    try:
        raw_data = fetch_url_bytes(url, timeout=timeout)
    except urllib.error.HTTPError as e:
        last_error = e
        if e.code in (403, 412, 503) and is_stealth_available():
            try:
                raw_data = fetch_with_stealth_browser(url, timeout=timeout * 2)
            except Exception as stealth_err:
                last_error = stealth_err
    except Exception as e:
        last_error = e
        if is_stealth_available():
            try:
                raw_data = fetch_with_stealth_browser(url, timeout=timeout * 2)
            except Exception as stealth_err:
                last_error = stealth_err

    if raw_data is None:
        raise last_error or RuntimeError(f"Failed to fetch feed: {url}")

    return parse_xml_bytes(raw_data, feed_config, extract_full_text=extract_full_text)
