"""Single-function module for Playwright stealth browser fetching."""
import logging
import time
from urllib.parse import urlparse
from typing import Optional

logger = logging.getLogger(__name__)

PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from .get_client_hints_headers import get_client_hints_headers
from core.cookies.set_playwright_cookies import set_playwright_cookies


def fetch_with_stealth_browser(
    url: str,
    timeout: int = 30,
    allow_interactive_fallback: bool = True,
    force_headless: Optional[bool] = None,
    cookie_str: Optional[str] = None,
    proxy_uri: Optional[str] = None,
) -> bytes:
    """
    Fetches raw content from url using a stealth-configured Chromium browser instance.
    """
    if not PLAYWRIGHT_AVAILABLE:
        raise RuntimeError(
            "Playwright is not installed. Run 'pip install playwright && python3 -m playwright install chromium' to enable stealth anti-bot scraping."
        )

    headers = get_client_hints_headers()
    user_agent = headers["User-Agent"]
    parsed_domain = urlparse(url).netloc

    def _attempt_fetch(headless: bool) -> bytes:
        with sync_playwright() as p:
            launch_kwargs = {
                "headless": headless,
                "args": [
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,800",
                ],
            }
            if proxy_uri:
                launch_kwargs["proxy"] = {"server": proxy_uri}

            browser = p.chromium.launch(**launch_kwargs)
            try:
                context = browser.new_context(
                    user_agent=user_agent,
                    viewport={"width": 1280, "height": 800},
                    extra_http_headers=headers,
                )

                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    window.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                """)

                if cookie_str and parsed_domain:
                    set_playwright_cookies(context, cookie_str, parsed_domain)

                page = context.new_page()
                intercepted_data = {}

                def handle_response(response):
                    if response.url == url or response.url.rstrip("/") == url.rstrip("/"):
                        try:
                            intercepted_data["bytes"] = response.body()
                            intercepted_data["status"] = response.status()
                        except Exception as e:
                            logger.debug(f"Failed to read response body: {e}")

                page.on("response", handle_response)

                logger.info(f"Stealth browser navigating to: {url} (headless={headless})")
                page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                time.sleep(2)

                content_str = page.content()
                lower_content = content_str.lower()

                is_challenge = any(
                    marker in lower_content
                    for marker in [
                        "just a moment...",
                        "cf-browser-verification",
                        "checking your browser",
                        "enable javascript and cookies",
                        "turnstile",
                        "access denied",
                    ]
                )

                if is_challenge and headless and allow_interactive_fallback:
                    raise PermissionError("Cloudflare interactive challenge detected in headless mode")

                if is_challenge and not headless:
                    logger.warning("Cloudflare challenge active. Waiting up to 20 seconds for user interaction...")
                    start_wait = time.time()
                    while time.time() - start_wait < 20:
                        time.sleep(1)
                        curr_content = page.content().lower()
                        if not any(m in curr_content for m in ["just a moment...", "cf-browser-verification"]):
                            break

                if intercepted_data.get("bytes"):
                    return intercepted_data["bytes"]

                return page.content().encode("utf-8")

            finally:
                browser.close()

    headless_setting = True if force_headless is None else force_headless

    try:
        return _attempt_fetch(headless=headless_setting)
    except PermissionError:
        if allow_interactive_fallback and headless_setting:
            logger.warning("Cloudflare challenge detected! Re-launching browser with headless=False for human interaction...")
            return _attempt_fetch(headless=False)
        raise
