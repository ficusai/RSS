"""Single-function module for fetching full page text from source web page."""
import re
import urllib.request
from .clean_html_simple import clean_html_simple

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def fetch_full_page_text(url: str, timeout: int = 5) -> str:
    """Extracts clean full text from an article webpage when RSS only provides a short summary snippet."""
    if not url or not url.startswith("http"):
        return ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html_bytes = resp.read()
            html_str = html_bytes.decode("utf-8", errors="ignore")

        main_match = re.search(r"<(main|article)[^>]*>(.*?)</\1>", html_str, re.DOTALL | re.IGNORECASE)
        target_html = main_match.group(2) if main_match else html_str

        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", target_html, re.DOTALL | re.IGNORECASE)
        clean_paragraphs = [clean_html_simple(p) for p in paragraphs if clean_html_simple(p)]

        valid_p = [
            p for p in clean_paragraphs
            if len(p) > 30
            and not any(
                w in p.lower()
                for w in ["official website", "subscribe", "cookie policy", "all rights reserved", "terms of use", "javascript", "browser"]
            )
        ]
        return "\n\n".join(valid_p)
    except Exception:
        return ""
