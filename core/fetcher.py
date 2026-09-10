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

# WHAT: Type hints for list, dict, and tuple data structures.
# OPTIONS/VALUES: Any, Dict, List, Tuple.
# DEFAULTS: Static typing annotations.
# OUTPUT/EFFECT: Enhances IDE code completion and type verification.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Checked by static code analysis tools.
from typing import Any, Dict, List, Tuple

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
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


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


# WHAT: Internal parser function that extracts title, URL link, GUID, publication date, author, and content from an RSS <item> or Atom <entry>.
# OPTIONS/VALUES: Inputs: XML element, feed_config dict.
# DEFAULTS: Returns standardized dictionary with 12 clean key fields.
# OUTPUT/EFFECT: Produces clean article object ready for JSON Lines saving.
# ERRORS/EDGE CASES: Handles missing author, missing dates, missing tags, or raw HTML content cleanly.
# HOW TO TEST: Pass an XML element into _parse_item_element() and check returned keys.
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


# WHAT: Downloads RSS or Atom XML from a feed URL and parses all contained articles.
# OPTIONS/VALUES: Input feed_config dictionary containing 'url', 'name', 'category'.
# DEFAULTS: 15-second network request timeout.
# OUTPUT/EFFECT: Returns list of parsed article dictionaries.
# ERRORS/EDGE CASES: Throws ValueError if feed_config lacks 'url'; throws HTTP errors on network failure.
# HOW TO TEST: Run 'python3 -c "from core.fetcher import fetch_feed; print(len(fetch_feed({\"url\": \"https://www.federalreserve.gov/feeds/press_all.xml\"})))"'.
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

    raw_data = raw_data.lstrip(b"\xef\xbb\xbf").strip()

    try:
        root = ET.fromstring(raw_data)
    except ET.ParseError as pe:
        lower_data = raw_data.lower()
        if b"<!doctype html" in lower_data or b"<html" in lower_data:
            raise ValueError("Server returned an HTML web page instead of a valid RSS/Atom XML feed") from pe
        raise ValueError(f"XML parse error: {pe}") from pe

    articles = []

    for elem in root.iter():
        ltag = _local_tag(elem)
        if ltag in ("item", "entry"):
            articles.append(_parse_item_element(elem, feed_config))

    return articles


# WHAT: Loops over all enabled feeds in a configuration list, fetching articles and capturing any network errors.
# OPTIONS/VALUES: Input feeds_list containing feed configuration dicts.
# DEFAULTS: Skips feeds where 'enabled' is set to False.
# OUTPUT/EFFECT: Returns tuple (all_articles_list, errors_list).
# ERRORS/EDGE CASES: Captures individual feed errors in errors_list so one bad feed doesn't crash the entire run.
# HOW TO TEST: Call fetch_all_feeds([{'url': 'https://www.federalreserve.gov/feeds/press_all.xml', 'enabled': True}]).
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
