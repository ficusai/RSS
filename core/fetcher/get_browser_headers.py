"""Single-function module for building browser headers with Client Hints."""
from typing import Dict, Optional
from core.stealth import get_client_hints_headers, USER_AGENTS

DEFAULT_USER_AGENT = USER_AGENTS[0]


def get_browser_headers(ua: Optional[str] = None) -> Dict[str, str]:
    """Generates modern browser request headers including Client Hints to bypass bot blocks."""
    return get_client_hints_headers(ua=ua)
