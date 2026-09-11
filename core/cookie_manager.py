"""
Cookie Management & Playwright Context Synchronization Utility.
Converts between standard HTTP Cookie header strings and Playwright/Browser cookie objects.
Inspired by RSSHub's lib/utils/playwright-utils.ts.
"""

from typing import List, Dict, Any, Optional


def parse_cookie_header(cookie_str: str, domain: str) -> List[Dict[str, Any]]:
    """
    Constructs a list of Playwright cookie dicts from a Cookie-header-style string.
    
    Args:
        cookie_str: Raw cookie header string (e.g. "foo=bar; baz=qux").
        domain: Target domain name (e.g. "example.com").

    Returns:
        List of dicts formatted for Playwright context.add_cookies().
    """
    if not cookie_str:
        return []

    # Clean domain (remove leading dot if present)
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


def format_cookie_header(cookies: List[Dict[str, Any]], domain_filter: Optional[str] = None) -> str:
    """
    Formats a list of Playwright cookie dicts into a standard Cookie header string.
    
    Args:
        cookies: List of cookie dictionaries.
        domain_filter: Optional domain string to filter cookies.

    Returns:
        Formatted cookie header string (e.g. "foo=bar; baz=qux").
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


def set_playwright_cookies(context: Any, cookie_str: str, domain: str) -> None:
    """Synchronizes a raw cookie header string onto a Playwright BrowserContext."""
    cookie_list = parse_cookie_header(cookie_str, domain)
    if cookie_list and hasattr(context, "add_cookies"):
        context.add_cookies(cookie_list)


def get_playwright_cookies(context: Any, domain_filter: Optional[str] = None) -> str:
    """Extracts cookies from a Playwright BrowserContext as an HTTP Cookie header string."""
    if hasattr(context, "cookies"):
        cookie_list = context.cookies()
        return format_cookie_header(cookie_list, domain_filter=domain_filter)
    return ""
