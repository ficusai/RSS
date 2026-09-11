"""
Feed fetcher engine supporting RSS 2.0 and Atom feeds.
Features a Tiered Dual-Engine Fetcher:
  Tier 1: Fast urllib.request with dynamic Chrome Client Hints (Sec-Ch-Ua) and Proxy Manager.
  Tier 2: Evasion-hardened Playwright stealth browser with CDP request replaying,
          cookie synchronization, proxy failover, and interactive headless=False fallback.
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional, Tuple
import random
import gzip
import io
import re

from .cleaner import clean_html, parse_to_iso
from .storage import generate_article_id
from .header_generator import get_client_hints_headers, USER_AGENTS
from .stealth_fetcher import fetch_with_stealth_browser, is_stealth_available
from .proxy_manager import global_proxy_manager
from .cookie_manager import parse_cookie_header

DEFAULT_USER_AGENT = USER_AGENTS[0]


def get_browser_headers(ua: Optional[str] = None) -> Dict[str, str]:
    """Generates modern browser request headers including Client Hints to bypass bot blocks."""
    return get_client_hints_headers(ua=ua)


def _local_tag(elem: ET.Element) -> str:
    """Returns local tag name without XML namespace."""
    if elem.tag.startswith("{"):
        return elem.tag.split("}", 1)[1].lower()
    return elem.tag.lower()


def _parse_item_element(elem: ET.Element, feed_config: Dict[str, Any], extract_full_text: bool = False) -> Dict[str, Any]:
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
        elif ltag in ("description", "summary") and not child.tag.startswith("{http://search.yahoo.com/mrss/}"):
            text_val = (child.text or "").strip()
            if text_val and not description_raw:
                description_raw = text_val
        elif ltag in ("encoded", "content") and not child.tag.startswith("{http://search.yahoo.com/mrss/}"):
            text_val = (child.text or "").strip()
            if text_val and not content_encoded_raw:
                content_encoded_raw = text_val

    title_clean = clean_html(title) or "Untitled"
    preview_clean = clean_html(description_raw)
    full_text_clean = clean_html(content_encoded_raw)

    if not preview_clean and full_text_clean:
        preview_clean = full_text_clean[:400] + ("..." if len(full_text_clean) > 400 else "")

    text_clean = full_text_clean if len(full_text_clean) > len(preview_clean) else (preview_clean or full_text_clean)

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
        "preview": preview_clean,
        "summary_raw": description_raw or content_encoded_raw,
        "content_encoded_raw": content_encoded_raw,
        "full_text_clean": full_text_clean,
        "text_clean": text_clean,
        "tags": tags,
    }


def _fetch_url_bytes(
    url: str,
    timeout: int = 10,
    headers: Optional[Dict[str, str]] = None,
    proxy_uri: Optional[str] = None,
) -> bytes:
    """Helper that executes HTTP GET request with de-compression & proxy support."""
    req_headers = headers or get_browser_headers()
    req = urllib.request.Request(url, headers=req_headers)

    proxy_handler = global_proxy_manager.get_urllib_handler(proxy_uri)
    opener = urllib.request.build_opener(proxy_handler)

    with opener.open(req, timeout=timeout) as response:
        content_encoding = response.info().get("Content-Encoding", "").lower()
        raw_bytes = response.read()
        if content_encoding == "gzip" or raw_bytes[:2] == b"\x1f\x8b":
            try:
                raw_bytes = gzip.decompress(raw_bytes)
            except Exception:
                pass
        return raw_bytes


def _parse_xml_bytes(raw_data: bytes, feed_config: Dict[str, Any], extract_full_text: bool = False) -> List[Dict[str, Any]]:
    """Helper to parse raw bytes into article objects."""
    raw_data = raw_data.lstrip(b"\xef\xbb\xbf").strip()

    try:
        root = ET.fromstring(raw_data)
    except ET.ParseError as pe:
        sanitized_bytes = re.sub(b"[\x00-\x08\x0B\x0C\x0E-\x1F]", b"", raw_data)
        try:
            root = ET.fromstring(sanitized_bytes)
        except ET.ParseError:
            lower_data = raw_data.lower()
            if b"<!doctype html" in lower_data or b"<html" in lower_data:
                raise ValueError("Server returned an HTML web page instead of a valid RSS/Atom XML feed") from pe
            raise ValueError(f"XML parse error: {pe}") from pe

    articles = []
    for elem in root.iter():
        ltag = _local_tag(elem)
        if ltag in ("item", "entry"):
            articles.append(_parse_item_element(elem, feed_config, extract_full_text=extract_full_text))

    return articles


def fetch_feed(feed_config: Dict[str, Any], extract_full_text: bool = False, timeout: int = 10) -> List[Dict[str, Any]]:
    """
    Fetches RSS/Atom XML from feed_config['url'] using a Tiered Dual-Engine approach:
      Tier 1: Fast urllib.request with Client Hints headers and proxy support.
      Tier 2: Evasion-hardened Playwright stealth browser with CDP response interception,
              cookie synchronization, proxy failover, and interactive headless=False fallback.
    """
    url = feed_config.get("url")
    if not url:
        raise ValueError("Feed configuration missing 'url' key")

    raw_data = None
    last_err = None
    cookie_str = feed_config.get("cookie")
    proxy_uri = feed_config.get("proxy")

    # Tier 1: urllib.request with Client Hints header rotation
    for attempt in range(2):
        try:
            ua = USER_AGENTS[attempt % len(USER_AGENTS)]
            headers = get_client_hints_headers(ua)
            if cookie_str:
                headers["Cookie"] = cookie_str
            raw_data = _fetch_url_bytes(url, timeout=timeout, headers=headers, proxy_uri=proxy_uri)
            break
        except Exception as e:
            last_err = e
            err_msg = str(e).lower()
            if proxy_uri:
                global_proxy_manager.mark_proxy_failed(proxy_uri)
            if any(code in err_msg for code in ["403", "412", "503", "500", "502", "504", "timed out"]):
                break

    # Tier 2: Stealth Playwright Browser Fallback if Tier 1 failed or returned HTML block
    should_use_stealth = False
    if raw_data is None and last_err:
        should_use_stealth = True
    elif raw_data:
        lower_raw = raw_data.lower()
        if b"<!doctype html" in lower_raw or b"cf-browser-verification" in lower_raw or b"just a moment..." in lower_raw:
            should_use_stealth = True

    if should_use_stealth and is_stealth_available():
        try:
            raw_data = fetch_with_stealth_browser(
                url,
                timeout=30,
                allow_interactive_fallback=True,
                cookie_str=cookie_str,
                proxy_uri=proxy_uri,
            )
            last_err = None
        except Exception as stealth_err:
            if not last_err:
                last_err = stealth_err

    if raw_data is None and last_err:
        raise last_err

    return _parse_xml_bytes(raw_data, feed_config, extract_full_text=extract_full_text)


def fetch_all_feeds(
    feeds_list: List[Dict[str, Any]],
    progress_callback: Optional[Callable[[str], None]] = None,
    max_workers: int = 20,
    extract_full_text: bool = False,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Loops over enabled feeds in feeds_list in parallel using ThreadPoolExecutor
    and returns (all_articles, errors_list).
    """
    all_articles: List[Dict[str, Any]] = []
    errors_list: List[Dict[str, Any]] = []

    enabled_feeds = [
        f for f in feeds_list if isinstance(f, dict) and f.get("enabled", True)
    ]
    total_enabled = len(enabled_feeds)

    if not enabled_feeds:
        return all_articles, errors_list

    if progress_callback:
        progress_callback(f"Starting parallel fetch of {total_enabled} feed(s)...")

    completed = 0

    def _worker(feed: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Optional[str]]:
        try:
            arts = fetch_feed(feed, extract_full_text=extract_full_text, timeout=10)
            return feed, arts, None
        except Exception as e:
            return feed, [], str(e)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_worker, f): f for f in enabled_feeds}
        for future in as_completed(futures):
            feed, arts, err = future.result()
            completed += 1
            feed_name = feed.get("name", "Unknown Feed")
            if err:
                errors_list.append(
                    {
                        "feed_name": feed_name,
                        "feed_url": feed.get("url", ""),
                        "error": err,
                    }
                )
                if progress_callback:
                    progress_callback(f"[{completed}/{total_enabled}] ❌ {feed_name}: {err}")
            else:
                all_articles.extend(arts)
                if progress_callback:
                    progress_callback(f"[{completed}/{total_enabled}] ✅ {feed_name}: {len(arts)} article(s)")

    return all_articles, errors_list
