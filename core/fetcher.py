"""
Feed fetcher engine supporting RSS 2.0 and Atom feeds.
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from .cleaner import clean_html, parse_to_iso
from .storage import generate_article_id

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _local_tag(elem: ET.Element) -> str:
    """Returns local tag name without XML namespace."""
    if elem.tag.startswith("{"):
        return elem.tag.split("}", 1)[1].lower()
    return elem.tag.lower()


def _parse_item_element(elem: ET.Element, feed_config: Dict[str, Any]) -> Dict[str, Any]:
    """Parses single RSS <item> or Atom <entry> XML element into standardized dict."""
    feed_url = feed_config.get("url", "")
    feed_name = feed_config.get("name", "")
    feed_cat = feed_config.get("category", "General")

    title = ""
    link = ""
    guid = ""
    pub_date = ""
    author = ""
    summary_raw = ""
    tags: List[str] = []

    for child in elem:
        ltag = _local_tag(child)

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
                if _local_tag(sub) == "name":
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
        elif ltag in ("description", "summary", "encoded", "content"):
            text_val = child.text or ""
            if text_val and (not summary_raw or ltag in ("encoded", "content")):
                summary_raw = text_val.strip()

    title_clean = clean_html(title) or "Untitled"
    text_clean = clean_html(summary_raw)
    published_iso = parse_to_iso(pub_date)
    scraped_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    article_id = generate_article_id(feed_url, link, title_clean, guid)

    return {
        "article_id": article_id,
        "feed_name": feed_name,
        "feed_url": feed_url,
        "category": feed_cat,
        "title": title_clean,
        "author": author,
        "url": link,
        "published_at_iso": published_iso,
        "scraped_at_iso": scraped_iso,
        "summary_raw": summary_raw,
        "text_clean": text_clean,
        "tags": tags,
    }


def fetch_feed(feed_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Fetches RSS/Atom XML from feed_config['url'] using urllib.request and returns standardized article list.
    """
    url = feed_config.get("url")
    if not url:
        raise ValueError("Feed configuration missing 'url' key")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        },
    )

    with urllib.request.urlopen(req, timeout=15) as response:
        raw_data = response.read()

    root = ET.fromstring(raw_data)
    articles = []

    for elem in root.iter():
        ltag = _local_tag(elem)
        if ltag in ("item", "entry"):
            articles.append(_parse_item_element(elem, feed_config))

    return articles


def fetch_all_feeds(feeds_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Loops over enabled feeds in feeds_list and returns (all_articles, errors_list).
    """
    all_articles: List[Dict[str, Any]] = []
    errors_list: List[Dict[str, Any]] = []

    for feed in feeds_list:
        if not isinstance(feed, dict):
            continue
        if not feed.get("enabled", True):
            continue

        try:
            articles = fetch_feed(feed)
            all_articles.extend(articles)
        except Exception as e:
            errors_list.append(
                {
                    "feed_name": feed.get("name", "Unknown Feed"),
                    "feed_url": feed.get("url", ""),
                    "error": str(e),
                }
            )

    return all_articles, errors_list
