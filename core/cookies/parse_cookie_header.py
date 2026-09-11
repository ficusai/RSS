"""Single-function module for parsing HTTP cookie headers into dicts."""
from typing import Any, Dict, List


def parse_cookie_header(cookie_str: str, domain: str) -> List[Dict[str, Any]]:
    """
    Constructs a list of Playwright cookie dicts from a Cookie-header-style string.
    """
    if not cookie_str:
        return []

    clean_domain = domain.lstrip(".")
    cookies = []
    for item in cookie_str.split("; "):
        if not item.strip():
            continue
        parts = item.split("=", 1)
        if len(parts) == 2:
            name, value = parts[0].strip(), parts[1].strip()
        else:
            name, value = "", parts[0].strip()

        cookies.append({
            "name": name,
            "value": value,
            "domain": clean_domain,
            "path": "/",
        })
    return cookies
