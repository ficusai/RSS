"""Fetcher package re-exporting single-function modules."""
from .get_browser_headers import get_browser_headers, DEFAULT_USER_AGENT
from .parse_local_tag import parse_local_tag
from .parse_item_element import parse_item_element
from .fetch_url_bytes import fetch_url_bytes
from .parse_xml_bytes import parse_xml_bytes
from .fetch_feed import fetch_feed
from .fetch_all_feeds import fetch_all_feeds

# Aliases for backward compatibility in tests
_local_tag = parse_local_tag
_parse_item_element = parse_item_element

__all__ = [
    "DEFAULT_USER_AGENT",
    "get_browser_headers",
    "parse_local_tag",
    "parse_item_element",
    "_local_tag",
    "_parse_item_element",
    "fetch_url_bytes",
    "parse_xml_bytes",
    "fetch_feed",
    "fetch_all_feeds",
]
