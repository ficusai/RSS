"""
Web Page Scraper Fallback Module (Git Branch: feature/web-scraper-fallback)

Extracts clean full-text article content from source web pages when RSS feeds only provide
short preview summaries.
"""

import urllib.request
import re
from typing import Optional

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def clean_html_simple(html_str: str) -> str:
    """Strips HTML tags and normalizes whitespace."""
    if not html_str or not isinstance(html_str, str):
        return ""
    import html
    text = html.unescape(html_str)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


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
