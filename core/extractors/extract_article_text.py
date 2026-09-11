"""Single-function module for readability-style article text extraction.

Extracts the main article body of a published HTML page and returns clean,
paragraph-separated plain text. It is deliberately conservative:

* block-aware text joining (inline <a>/<code>/<span> never break lines),
* text-density main container selection,
* aggressive boilerplate block pruning (nav promos, "Most Popular", by-lines,
  cookie/subscribe/read-more artefacts, trailers).
"""

import logging
import re
from typing import Dict, Iterable, List

from bs4 import BeautifulSoup, NavigableString, Tag

from core.boilerplate_terms import BOILERPLATE_TERMS

logger = logging.getLogger(__name__)

BS4_AVAILABLE = True  # bs4 is a hard dependency in this project

UNWANTED_SELECTORS: List[str] = [
    "nav", "header", "footer", "aside", "form", "button", "iframe", "noscript",
    "script", "style", "svg", "canvas",
    ".ad", ".ads", ".advertisement", ".advert", ".sponsored", ".promo",
    ".social-share", ".share-tools", ".sharing",
    ".comments", ".comment-list", "#comments", ".comment-form",
    "#sidebar", ".sidebar", ".related-posts", ".related", ".also-read",
    ".cookie-banner", ".cookie-consent", ".cookie-notice",
    ".navigation", ".nav-menu", ".nav-bar", ".header-wrapper", ".header-nav",
    ".footer-wrapper", ".site-footer", "#footer",
    ".newsletter", ".subscribe-cta", ".signup-box", ".email-capture",
    ".breadcrumbs", ".pagination", ".pager", ".skip-link", ".sr-only",
]

INLINE_TAGS = {
    "a", "abbr", "acronym", "b", "bdi", "bdo", "big", "cite", "code", "del",
    "dfn", "em", "font", "i", "ins", "kbd", "label", "mark", "q", "s", "samp",
    "small", "span", "strike", "strong", "sub", "sup", "time", "tt", "u",
    "var", "wbr", "rb", "rp", "rt",
}

BLOCK_CANDIDATE_TAGS = ("article", "main", "section", "div")

PARAGRAPH_TAGS = ("p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre", "li", "dt", "dd", "figcaption")

HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

PUNCT_TRIM_RE = re.compile(r"\s+([,.;:!?)\]»%])")
WHITESPACE_RE = re.compile(r"\s+")
BYLINE_RE = re.compile(r"^\s*(by|written by|byline|from)\s+[^\n]{1,60}\s*$", re.IGNORECASE)


def _clean_inline(text: str) -> str:
    """Collapses whitespace and fixes spaces before punctuation inside a block."""
    out = WHITESPACE_RE.sub(" ", text or "")
    out = PUNCT_TRIM_RE.sub(r"\1", out)
    return out.strip()


def _normalized(text: str) -> str:
    return (text or "").replace("’", "'").replace("‘", "'").lower()


def _count_boilerplate(text: str) -> int:
    low = _normalized(text)
    return sum(1 for term in BOILERPLATE_TERMS if term in low)


def _link_density(block: Tag) -> float:
    """Fraction of a block's characters that live inside <a> tags."""
    total = len(block.get_text(" "))
    if total < 1:
        return 0.0
    link_text = sum(len(a.get_text(" ")) for a in block.find_all("a"))
    return link_text / total


def _is_link_block(block: Tag, text: str) -> bool:
    """True when a block is essentially a list of links (nav/headlines box)."""
    return not block.name in HEADING_TAGS and len(text) < 260 and _link_density(block) > 0.65


def _is_boilerplate(text: str, min_len: int = 45, is_heading: bool = False) -> bool:
    """True if a paragraph looks like nav/promo/junk rather than article text."""
    if not text:
        return True
    low = _normalized(text)
    if is_heading:
        # Headings are allowed to be short, but still reject obvious nav labels.
        return any(term in low for term in ("most popular", "related", "recommended", "subscribe", "newsletter"))
    if BYLINE_RE.match(text):
        return True
    if _count_boilerplate(text) >= 1:
        return True
    if len(text) < min_len:
        return True
    # Gallery/by-line style blocks: "Name by author" repeated rows.
    if re.match(r"^.{1,60}\s+by\s+.{1,40}$", text, re.IGNORECASE):
        return True
    return False


def _gather_paragraph_blocks(main_elem: Tag) -> List[Tag]:
    """Collects paragraph-level blocks; falls back to dense <div> blocks."""
    blocks = main_elem.find_all(PARAGRAPH_TAGS)
    filled = [b for b in blocks if len(_clean_inline(b.get_text(" "))) >= 45]
    total_text = sum(len(_clean_inline(b.get_text(" "))) for b in filled)

    if total_text < 200 or len(filled) < 3:
        # Some sites (plain markdown-style blogs, code dumps) use <div> per
        # paragraph with no <p>. Pull direct-text divs as fallback blocks.
        for div in main_elem.find_all("div"):
            if any(isinstance(c, Tag) and c.name in ("div", "p", "ul", "table") for c in div.children):
                continue
            txt = _clean_inline(div.get_text(" "))
            if len(txt) >= 60:
                blocks.append(div)
    return blocks


def _score_container(el: Tag) -> tuple:
    """Readability-lite density score: text volume and paragraph count."""
    text_len = len(_clean_inline(el.get_text(" ")))
    p_count = len(el.find_all(["p", "blockquote", "pre"]))
    return (text_len, p_count)


def _select_main(soup: BeautifulSoup) -> Tag:
    """Selects the primary article container by density, preferencing semantics."""
    candidates: List[Tag] = []
    for tag in BLOCK_CANDIDATE_TAGS:
        for el in soup.find_all(tag):
            # Only consider reasonably-placed containers to avoid duplicating nests.
            candidates.append(el)

    body = soup.body or soup
    if not candidates:
        return body

    scored = [(c, _score_container(c)) for c in candidates]
    best, best_score = max(scored, key=lambda x: x[1])

    if best_score[0] < 200:
        return body
    return best


def _extract_title(soup: BeautifulSoup) -> str:
    title_elem = soup.find("title") or soup.find("h1")
    return title_elem.get_text(" ", strip=True) if title_elem else ""


def extract_article_text(html: str, url: str = "") -> Dict[str, str]:
    """
    Extracts a clean article body from raw HTML.

    Returns: {clean_text, clean_html, word_count, url, title}
    """
    empty = {"clean_text": "", "clean_html": "", "word_count": 0, "url": url, "title": ""}
    if not html or not isinstance(html, str):
        return empty

    soup = BeautifulSoup(html, "html.parser")
    title = _extract_title(soup)

    for selector in UNWANTED_SELECTORS:
        for element in soup.select(selector):
            element.decompose()

    main_elem = _select_main(soup)
    blocks = _gather_paragraph_blocks(main_elem)

    paragraphs: List[str] = []
    first_heading_kept = False
    for block in blocks:
        is_heading = block.name in HEADING_TAGS
        text = _clean_inline(block.get_text(" "))
        is_first_heading = is_heading and not first_heading_kept
        if _link_density(block) > 0.8 and len(text) < 220 and not is_first_heading:
            # Pure-link blocks are nav/headline boxes; only the first heading
            # (the article headline) is exempt so it survives as a lead-in.
            continue
        if is_heading:
            first_heading_kept = True
        if _is_link_block(block, text):
            continue
        if _is_boilerplate(text, is_heading=is_heading):
            continue
        if not paragraphs or paragraphs[-1] != text:
            paragraphs.append(text)

    # Trim nav/junk from the start (e.g. "Previous", "Next", site intros).
    while paragraphs and _is_boilerplate(paragraphs[0], min_len=30, is_heading=False):
        paragraphs.pop(0)
    # Trim promo/junk trailers from the end aggressively.
    while paragraphs and (
        _is_boilerplate(paragraphs[-1], min_len=30, is_heading=False)
        or (len(paragraphs[-1]) < 60 and not re.search(r"[.!?…]\"?$", paragraphs[-1]))
    ):
        paragraphs.pop()
    # Trim residual UI fragments (e.g. ".com", "Select", stray bullets).
    while paragraphs and len(paragraphs[-1]) < 26 and not re.search(r"[A-Za-z]{6,}", paragraphs[-1]):
        paragraphs.pop()

    clean_text = "\n\n".join(paragraphs)
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)
    clean_text = re.sub(r"\s*\bContinue reading\.\.\.\s*$", "", clean_text)
    clean_text = re.sub(r"\s*\bContinue reading\s*$", "", clean_text)
    # Drop stray trailing comment/byline lines ending in a bullet (e.g. gist "Name commented ... •").
    clean_text = re.sub(r"\n*\s*[^\n]*\b•\s*$", "", clean_text)

    words = clean_text.split()
    clean_html = "\n\n".join(f"<p>{p}</p>" for p in paragraphs)

    return {
        "clean_text": clean_text,
        "clean_html": clean_html,
        "word_count": len(words),
        "url": url,
        "title": title,
    }