"""Single-function module for extracting cookies from Playwright BrowserContext."""
from typing import Any, Optional
from .format_cookie_header import format_cookie_header


def get_playwright_cookies(context: Any, domain_filter: Optional[str] = None) -> str:
    """Extracts cookies from a Playwright BrowserContext as an HTTP Cookie header string."""
    if hasattr(context, "cookies"):
        cookie_list = context.cookies()
        return format_cookie_header(cookie_list, domain_filter=domain_filter)
    return ""
