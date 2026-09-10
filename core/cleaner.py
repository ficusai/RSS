"""
HTML cleaning and Date parsing utilities for RSS feed processing.
"""

import html
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def clean_html(html_str: str) -> str:
    """
    Strips HTML tags, unescapes HTML entities, and normalizes spacing.
    """
    if not html_str or not isinstance(html_str, str):
        return ""

    # Unescape HTML entities
    text = html.unescape(html_str)

    # Strip script and style blocks content
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace (replace multiple spaces/newlines with a single space)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def parse_to_iso(date_str: str) -> str:
    """
    Parses RFC-822 (RSS) or ISO-8601 (Atom) date strings into clean ISO 8601 UTC string (YYYY-MM-DDTHH:MM:SSZ).
    Falls back to current UTC time if parsing fails.
    """
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not date_str or not isinstance(date_str, str):
        return now_utc

    date_str = date_str.strip()
    if not date_str:
        return now_utc

    # 1. Try RFC-822 (RSS format, e.g. Mon, 02 Jan 2006 15:04:05 GMT)
    try:
        dt = parsedate_to_datetime(date_str)
        if dt is not None:
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc)
            else:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        pass

    # 2. Try ISO-8601 (Atom format, e.g. 2006-01-02T15:04:05Z or 2006-01-02T15:04:05+00:00)
    iso_candidate = date_str
    if iso_candidate.endswith("Z"):
        iso_candidate = iso_candidate[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(iso_candidate)
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        pass

    # 3. Fallback common date formats
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d %b %Y %H:%M:%S"):
        try:
            dt = datetime.strptime(date_str, fmt)
            dt = dt.replace(tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            continue

    return now_utc
