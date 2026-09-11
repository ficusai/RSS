"""
Feed fetcher engine supporting RSS 2.0 and Atom feeds.
"""

# WHAT: Standard Python library module for sending HTTP/HTTPS web requests to download RSS feeds over the Internet.
# OPTIONS/VALUES: urllib.request.Request(), urllib.request.urlopen().
# DEFAULTS: Standard Python library module.
# OUTPUT/EFFECT: Downloads raw XML feed data from remote web servers.
# ERRORS/EDGE CASES: Raises HTTPError or URLError on network disconnection or 404/500 HTTP responses.
# HOW TO TEST: Run 'python3 -c "import urllib.request; print(urllib.request.urlopen(\"https://www.federalreserve.gov/feeds/press_all.xml\").status)"'.
import urllib.request

# WHAT: Error definitions module for catching web fetch failures like 403 Forbidden or 404 Not Found.
# OPTIONS/VALUES: urllib.error.HTTPError, urllib.error.URLError.
# DEFAULTS: Standard library error handler.
# OUTPUT/EFFECT: Allows catching web request errors cleanly.
# ERRORS/EDGE CASES: Catches socket timeouts and invalid domain names.
# HOW TO TEST: Pass invalid domain to urllib.request.urlopen().
import urllib.error

# WHAT: Built-in XML parsing library for reading RSS 2.0 (<item>) and Atom 1.0 (<entry>) feed data structures.
# OPTIONS/VALUES: ET.fromstring(), elem.iter(), elem.findtext().
# DEFAULTS: Standard Python ElementTree XML parser.
# OUTPUT/EFFECT: Parses XML strings into tree structures of elements and tags.
# ERRORS/EDGE CASES: Raises ET.ParseError on invalid or corrupt XML syntax.
# HOW TO TEST: Run 'python3 -c "import xml.etree.ElementTree as ET; print(ET.fromstring(\"<rss><channel><title>Test</title></channel></rss>\").findtext(\"channel/title\"))"'.
import xml.etree.ElementTree as ET

# WHAT: Date utilities for recording current UTC timestamp when an article is scraped.
# OPTIONS/VALUES: datetime.now(timezone.utc).
# DEFAULTS: Coordinated Universal Time (UTC).
# OUTPUT/EFFECT: Sets 'scraped_at_iso' timestamp on parsed article records.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc))"'.
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# WHAT: Type hints for list, dict, and tuple data structures.
# OPTIONS/VALUES: Any, Dict, List, Tuple, Callable, Optional.
# DEFAULTS: Static typing annotations.
# OUTPUT/EFFECT: Enhances IDE code completion and type verification.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Checked by static code analysis tools.
from typing import Any, Callable, Dict, List, Optional, Tuple

# WHAT: Imports HTML scrubbing and date parsing functions from the local cleaner module.
# OPTIONS/VALUES: clean_html(), parse_to_iso().
# DEFAULTS: Local package import.
# OUTPUT/EFFECT: Strips raw HTML and normalizes date strings.
# ERRORS/EDGE CASES: Handled inside cleaner.py functions.
# HOW TO TEST: Run 'python3 -c "from core.cleaner import clean_html, parse_to_iso"'.
from .cleaner import clean_html, parse_to_iso

# WHAT: Imports unique article SHA-256 hash generator from local storage module.
# OPTIONS/VALUES: generate_article_id().
# DEFAULTS: Local package import.
# OUTPUT/EFFECT: Computes deduplication article IDs.
# ERRORS/EDGE CASES: Handled inside storage.py.
# HOW TO TEST: Run 'python3 -c "from core.storage import generate_article_id"'.
from .storage import generate_article_id

# WHAT: User-Agent browser header string sent with HTTP requests to prevent servers from blocking python web requests.
# OPTIONS/VALUES: Mimics Google Chrome browser on Windows 10.
# DEFAULTS: Chrome/120.0 User-Agent string.
# OUTPUT/EFFECT: Bypasses basic 403 Forbidden bot protection on news servers.
# ERRORS/EDGE CASES: Some strict servers may require unique user agents.
# HOW TO TEST: Verify headers sent in urllib Request objects.
import random
import gzip
import io

# WHAT: User-Agent browser header pool sent with HTTP requests to bypass strict bot protection on news servers.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
]

DEFAULT_USER_AGENT = USER_AGENTS[0]


def get_browser_headers(ua: Optional[str] = None) -> Dict[str, str]:
    """Generates modern browser request headers to bypass bot blocks."""
    user_agent = ua or random.choice(USER_AGENTS)
    return {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }


# WHAT: Internal helper function that strips XML namespace prefixes (like '{http://www.w3.org/2005/Atom}') to return plain tag names ('entry').
# OPTIONS/VALUES: Input XML element.
# DEFAULTS: Returns lower-cased tag string.
# OUTPUT/EFFECT: Simplifies XML tag checking for RSS and Atom feeds.
# ERRORS/EDGE CASES: Handles tags with or without namespace brackets.
# HOW TO TEST: Run 'python3 -c "import xml.etree.ElementTree as ET; from core.fetcher import _local_tag; e = ET.Element(\"{http://www.w3.org/2005/Atom}title\"); print(_local_tag(e))"'.
def _local_tag(elem: ET.Element) -> str:
    """Returns local tag name without XML namespace."""
    if elem.tag.startswith("{"):
        return elem.tag.split("}", 1)[1].lower()
    return elem.tag.lower()


# WHAT: Internal parser function that extracts title, URL link, GUID, publication date, author, preview, and full content from an RSS <item> or Atom <entry>.
# OPTIONS/VALUES: Inputs: XML element, feed_config dict.
# DEFAULTS: Returns standardized dictionary with preview, raw summary, encoded content, and clean full text.
# OUTPUT/EFFECT: Produces comprehensive article object ready for JSON Lines saving.
# ERRORS/EDGE CASES: Handles missing author, missing dates, missing tags, or raw HTML content cleanly.
# HOW TO TEST: Pass an XML element into _parse_item_element() and check returned keys.
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

    # If preview is empty, derive preview from first 400 chars of full text
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


# WHAT: Downloads RSS or Atom XML from a feed URL and parses all contained articles.
# OPTIONS/VALUES: Input feed_config dictionary containing 'url', 'name', 'category'.
# DEFAULTS: 15-second network request timeout.
# OUTPUT/EFFECT: Returns list of parsed article dictionaries.
# ERRORS/EDGE CASES: Throws ValueError if feed_config lacks 'url'; throws HTTP errors on network failure.
# HOW TO TEST: Run 'python3 -c "from core.fetcher import fetch_feed; print(len(fetch_feed({\"url\": \"https://www.federalreserve.gov/feeds/press_all.xml\"})))"'.
def _fetch_url_bytes(url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None) -> bytes:
    """Helper that executes HTTP GET request with de-compression support."""
    req = urllib.request.Request(url, headers=headers or get_browser_headers())
    with urllib.request.urlopen(req, timeout=timeout) as response:
        content_encoding = response.info().get("Content-Encoding", "").lower()
        raw_bytes = response.read()
        if content_encoding == "gzip" or raw_bytes[:2] == b"\x1f\x8b":
            try:
                raw_bytes = gzip.decompress(raw_bytes)
            except Exception:
                pass
        return raw_bytes


def fetch_feed(feed_config: Dict[str, Any], extract_full_text: bool = False, timeout: int = 10) -> List[Dict[str, Any]]:
    """
    Fetches RSS/Atom XML from feed_config['url'] using urllib.request with retries & header rotation.
    """
    url = feed_config.get("url")
    if not url:
        raise ValueError("Feed configuration missing 'url' key")

    raw_data = None
    last_err = None

    # Retry loop with header rotation for 403 / transient errors
    for attempt in range(2):
        try:
            ua = USER_AGENTS[attempt % len(USER_AGENTS)]
            headers = get_browser_headers(ua)
            raw_data = _fetch_url_bytes(url, timeout=timeout, headers=headers)
            break
        except Exception as e:
            last_err = e
            if attempt == 0 and any(code in str(e) for code in ["403", "503", "500", "502", "504", "timed out"]):
                continue
            raise e

    if raw_data is None and last_err:
        raise last_err

    raw_data = raw_data.lstrip(b"\xef\xbb\xbf").strip()

    try:
        root = ET.fromstring(raw_data)
    except ET.ParseError as pe:
        # Sanitize control characters and retry parsing
        import re
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


# WHAT: Loops over all enabled feeds in a configuration list, fetching articles and capturing any network errors.
# OPTIONS/VALUES: Input feeds_list containing feed configuration dicts.
# DEFAULTS: Skips feeds where 'enabled' is set to False.
# OUTPUT/EFFECT: Returns tuple (all_articles_list, errors_list).
# ERRORS/EDGE CASES: Captures individual feed errors in errors_list so one bad feed doesn't crash the entire run.
# HOW TO TEST: Call fetch_all_feeds([{'url': 'https://www.federalreserve.gov/feeds/press_all.xml', 'enabled': True}]).
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
