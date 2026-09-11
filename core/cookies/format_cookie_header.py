"""Single-function module for formatting cookie dicts into HTTP Cookie header strings."""
from typing import Any, Dict, List, Optional


def format_cookie_header(cookies: List[Dict[str, Any]], domain_filter: Optional[str] = None) -> str:
    """
    Formats a list of Playwright cookie dicts into a standard Cookie header string.
    """
    if not cookies:
        return ""

    filtered = cookies
    if domain_filter:
        target_domain = domain_filter.lstrip(".")
        filtered = [
            c for c in cookies
            if c.get("domain", "").lstrip(".") == target_domain
            or c.get("domain", "").endswith("." + target_domain)
        ]

    cookie_parts = []
    for c in filtered:
        name = c.get("name", "")
        value = c.get("value", "")
        if name:
            cookie_parts.append(f"{name}={value}")
        elif value:
            cookie_parts.append(value)

    return "; ".join(cookie_parts)
