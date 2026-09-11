"""Single-function module for fetching and extracting clean article text from URL."""
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


UNWANTED_SELECTORS = [
    "nav", "header", "footer", "aside", "script", "style", "iframe", "noscript",
    ".ad", ".ads", ".advertisement", ".social-share", ".comments", ".comment-list",
    "#comments", "#sidebar", ".sidebar", ".related-posts", ".cookie-banner",
    ".navigation", ".nav-menu", ".header-wrapper", ".footer-wrapper"
]


def extract_article_text(html: str, url: str = "") -> dict:
    """
    Extracts clean article text from HTML using BeautifulSoup-based readability.
    Returns dict with 'clean_text', 'clean_html', 'word_count', 'title'.
    """
    if not html or not isinstance(html, str):
        return {"clean_text": "", "clean_html": "", "word_count": 0, "title": ""}

    if not BS4_AVAILABLE:
        logger.warning("BeautifulSoup not available, skipping readability extraction")
        return {"clean_text": "", "clean_html": "", "word_count": 0, "title": ""}

    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title_elem = soup.find("title") or soup.find("h1")
    extracted_title = title_elem.get_text().strip() if title_elem else ""

    # Remove unwanted elements
    for selector in UNWANTED_SELECTORS:
        for element in soup.select(selector):
            element.decompose()

    # Find main content element
    main_elem = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", class_=re.compile(r"(content|article|post|body|entry-content)", re.I))
        or soup.find("section", class_=re.compile(r"(content|article|post|body)", re.I))
        or soup.find("div", id=re.compile(r"(content|article|post|main)", re.I))
        or soup.body
        or soup
    )

    clean_text = main_elem.get_text(separator="\n", strip=True) if main_elem else ""
    clean_html = str(main_elem) if main_elem else ""

    # Clean up text
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)
    clean_text = re.sub(r"[ \t]+", " ", clean_text)
    words = clean_text.split()

    return {
        "clean_text": clean_text,
        "clean_html": clean_html,
        "word_count": len(words),
        "title": extracted_title
    }
