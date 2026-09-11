"""Single-function module for applying cookie header string onto Playwright BrowserContext."""
from typing import Any
from .parse_cookie_header import parse_cookie_header


def set_playwright_cookies(context: Any, cookie_str: str, domain: str) -> None:
    """Synchronizes a raw cookie header string onto a Playwright BrowserContext."""
    cookie_list = parse_cookie_header(cookie_str, domain)
    if cookie_list and hasattr(context, "add_cookies"):
        context.add_cookies(cookie_list)
