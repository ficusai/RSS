"""Single-function module for basic HTML entity unescaping and tag stripping."""
import html
import re


def clean_html_simple(html_str: str) -> str:
    """Strips HTML tags and normalizes whitespace."""
    if not html_str or not isinstance(html_str, str):
        return ""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_str, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()
