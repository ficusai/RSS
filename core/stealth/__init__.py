"""Stealth package re-exporting single-function modules."""
from .get_client_hints_headers import get_client_hints_headers, USER_AGENTS
from .is_stealth_available import is_stealth_available, PLAYWRIGHT_AVAILABLE
from .fetch_with_stealth_browser import fetch_with_stealth_browser

__all__ = [
    "USER_AGENTS",
    "get_client_hints_headers",
    "PLAYWRIGHT_AVAILABLE",
    "is_stealth_available",
    "fetch_with_stealth_browser",
]
