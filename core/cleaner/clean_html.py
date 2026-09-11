"""Single-function module for HTML tag stripping and text cleaning."""
import html
import re


def clean_html(html_str: str) -> str:
    """
    Strips HTML tags, unescapes HTML entities, and normalizes spacing.
    """
    if not html_str or not isinstance(html_str, str):
        return ""

    text = html.unescape(html_str)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
