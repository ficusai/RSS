"""Single-function module for standardizing RFC-822 and ISO-8601 timestamps to ISO UTC format."""
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


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

    # 1. Try RFC-822
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

    # 2. Try ISO-8601
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
