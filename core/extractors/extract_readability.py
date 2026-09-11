"""Single-function module for DOM-based readability article extraction."""
import re
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup, Tag

UNWANTED_SELECTORS: List[str] = [
    "nav", "header", "footer", "aside", "script", "style", "iframe", "noscript",
    ".ad", ".ads", ".advertisement", ".social-share", ".comments", ".comment-list",
    "#comments", "#sidebar", ".sidebar", ".related-posts", ".cookie-banner",
    ".navigation", ".nav-menu", ".header-wrapper", ".footer-wrapper"
]


def extract_readability(html_content: str, url: str = "") -> Dict[str, Any]:
    """
    Parses raw HTML and isolates primary content container, plain text, and word count.
    """
    if not html_content or not isinstance(html_content, str):
        return {
            "clean_text": "",
            "clean_html": "",
            "word_count": 0,
            "url": url,
            "title": ""
        }

    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title before decomposing elements
    title_elem = soup.find("title") or soup.find("h1")
    extracted_title = title_elem.get_text().strip() if title_elem else ""

    # Decompose unwanted noise elements
    for selector in UNWANTED_SELECTORS:
        for element in soup.select(selector):
            element.decompose()

    # Identify candidate main article element
    main_elem: Optional[Tag] = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", class_=re.compile(r"(content|article|post|body|entry-content)", re.I))
        or soup.find("section", class_=re.compile(r"(content|article|post|body)", re.I))
        or soup.body
        or soup
    )

    clean_text = main_elem.get_text(separator="\n", strip=True) if main_elem else ""
    clean_html = str(main_elem) if main_elem else ""

    # Normalize whitespace in clean_text
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)
    words = clean_text.split()

    return {
        "clean_text": clean_text,
        "clean_html": clean_html,
        "word_count": len(words),
        "url": url,
        "title": extracted_title
    }
