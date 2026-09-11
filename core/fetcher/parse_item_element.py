"""Single-function module for parsing RSS item or Atom entry XML elements."""
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional
from core.cleaner import clean_html, parse_to_iso
from core.storage import generate_article_id
from .parse_local_tag import parse_local_tag

WHITESPACE_RE = re.compile(r"\s+")


def _extract_text_from_html(html_str: str) -> str:
    """Extracts plain text from HTML string, handling both raw HTML and escaped entities."""
    if not html_str:
        return ""
    # First unescape HTML entities
    import html as html_module
    text = html_module.unescape(html_str)
    # Then strip tags
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _parse_html_content(content_raw: str) -> str:
    """Parses HTML content from RSS item, handling CDATA, escaped entities, and nested tags."""
    if not content_raw:
        return ""
    # Handle CDATA sections
    content_raw = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", content_raw, flags=re.DOTALL)
    # Handle escaped HTML entities in attributes
    content_raw = re.sub(r"&quot;", '"', content_raw)
    content_raw = re.sub(r"&apos;", "'", content_raw)
    content_raw = re.sub(r"&lt;", "<", content_raw)
    content_raw = re.sub(r"&gt;", ">", content_raw)
    content_raw = re.sub(r"&amp;", "&", content_raw)
    return content_raw


def _is_trivial_preview(text: str) -> bool:
    """True when a feed's description is just a link artifact (e.g. 'Comments')."""
    low = re.sub(r"\s+", " ", text or "").strip().lower().rstrip(".")
    return low in ("", "comments", "read more", "continue reading", "-", "discussion", "sign in", "view") or len(low) < 12


def _make_preview(text: str, limit: int = 400) -> str:
    """Builds a preview from the head of a text, cutting on sentence boundaries."""
    t = WHITESPACE_RE.sub(" ", text or "").strip()
    if not t:
        return ""
    if len(t) <= limit:
        return t
    cut = None
    for m in re.finditer(r"[.!?…](?:\s|$)", t):
        if m.end() <= limit:
            cut = m.end()
        else:
            break
    if cut:
        return t[:cut]
    clipped = t[: limit - 3].rsplit(" ", 1)[0]
    return clipped.rstrip(".,;:") + "..."


def _try_readability_fallback(url: str) -> Optional[str]:
    """Attempts to fetch and extract article text using readability algorithm."""
    import urllib.request
    try:
        from core.extractors.extract_article_text import extract_article_text
        req = urllib.request.Request(url, headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html_bytes = resp.read()
            html_str = html_bytes.decode("utf-8", errors="ignore")
            result = extract_article_text(html_str, url=url)
            return result.get("clean_text", "")
    except Exception:
        pass
    return None


def parse_item_element(elem: ET.Element, feed_config: Dict[str, Any], extract_full_text: bool = False) -> Dict[str, Any]:
    """Parses single RSS <item> or Atom <entry> XML element into standardized dict with preview & full content."""
    feed_url = feed_config.get("url", "")
    feed_name = feed_config.get("name", "")
    feed_cat = feed_config.get("category", "General")

    title = ""
    link = ""
    guid = ""
    pub_date = ""
    author = ""
    description_raw = ""
    content_encoded_raw = ""
    content_html = ""
    tags: List[str] = []

    for child in elem:
        ltag = parse_local_tag(child)

        if ltag == "title" and child.text and not title:
            title = child.text.strip()
        elif ltag == "link":
            href = child.attrib.get("href")
            rel = child.attrib.get("rel", "alternate")
            if href:
                if not link or rel == "alternate":
                    link = href.strip()
            elif child.text:
                link = child.text.strip()
        elif ltag in ("guid", "id") and child.text and not guid:
            guid = child.text.strip()
        elif ltag in ("pubdate", "published", "updated", "date") and child.text and not pub_date:
            pub_date = child.text.strip()
        elif ltag in ("creator", "author"):
            name_child = None
            for sub in child:
                if parse_local_tag(sub) == "name":
                    name_child = sub
                    break
            if name_child is not None and name_child.text:
                author = name_child.text.strip()
            elif child.text and child.text.strip():
                author = child.text.strip()
        elif ltag == "category":
            cat_val = child.attrib.get("term") or child.text
            if cat_val and cat_val.strip():
                tags.append(cat_val.strip())
        elif ltag == "description" and not child.tag.startswith("{http://search.yahoo.com/mrss/}"):
            if child.text:
                description_raw = _parse_html_content(child.text)
            # Handle nested content
            for sub in child:
                if parse_local_tag(sub) == "encoded":
                    description_raw = _parse_html_content((sub.text or ""))
                    break
        elif ltag in ("encoded", "content") and not child.tag.startswith("{http://search.yahoo.com/mrss/}"):
            if child.text:
                content_encoded_raw = _parse_html_content(child.text)
            if not content_html and child.text:
                content_html = child.text
            # Handle xmlns:content
            for sub in child:
                if parse_local_tag(sub) in ("div", "p", "span", "a"):
                    content_html = (child.text or "") + "".join(ET.tostring(sub, encoding='unicode') for sub in child)
                    break
        elif ltag == "content" and not child.tag.startswith("{http://search.yahoo.com/mrss/}"):
            content_raw = child.text or ""
            if content_raw:
                content_encoded_raw = _parse_html_content(content_raw)
            if not content_html:
                content_html = content_raw

    # Clean extracted text
    title_clean = clean_html(title) or "Untitled"
    full_text_clean = clean_html(content_encoded_raw) if content_encoded_raw else ""

    # If we have HTML content but no text, try to extract
    if not full_text_clean and content_html:
        full_text_clean = _extract_text_from_html(content_html)

    # Fallback: try readability extraction if content is too short
    if extract_full_text and link and len(full_text_clean or "") < 150:
        readability_text = _try_readability_fallback(link)
        if readability_text and len(readability_text) > len(full_text_clean or ""):
            full_text_clean = readability_text

    # Derive preview from a substantive feed description, else from full text lead
    preview_clean = ""
    desc_clean = clean_html(description_raw) if description_raw else ""
    if desc_clean and not _is_trivial_preview(desc_clean):
        preview_clean = _make_preview(desc_clean)
    if not preview_clean and full_text_clean:
        preview_clean = _make_preview(full_text_clean)

    # Final text selection: full content if available, else fall back to the
    # feed description (even a short one beats an empty reader pane).
    final_text = full_text_clean if full_text_clean else desc_clean
    pub_date_iso = parse_to_iso(pub_date)
    art_id = generate_article_id(feed_url, link, title_clean, guid)

    return {
        "article_id": art_id,
        "feed_url": feed_url,
        "feed_name": feed_name,
        "category": feed_cat,
        "title": title_clean,
        "url": link,
        "guid": guid,
        "pub_date": pub_date_iso,
        "published_at_iso": pub_date_iso,
        "author": author,
        "preview": preview_clean[:500] if preview_clean else "",
        "full_text_clean": full_text_clean,
        "text_clean": final_text,
        "extractor_version": 2,
        "tags": tags,
    }
