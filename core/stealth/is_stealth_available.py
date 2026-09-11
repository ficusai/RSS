"""Single-function module checking Playwright stealth availability."""
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def is_stealth_available() -> bool:
    """Returns True if Playwright browser automation is installed and ready."""
    return PLAYWRIGHT_AVAILABLE
