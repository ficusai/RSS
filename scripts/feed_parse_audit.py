#!/usr/bin/env python3
"""
One-time RSS feed parsing audit.

For every feed in config/feeds.json this script runs the audit loop:

  STEP A - PING (real info):
      Fetch the raw feed bytes directly over HTTP (independent of the app's
      parser) and inspect the true RSS/Atom XML: feed title, item count and
      per-item {title, link, guid, pubDate, description}.

  STEP B - RSS.desktop output (app pipeline):
      Replicate exactly what the GUI "Ping" button does (RSS.desktop launches
      gui/window.py; ScrapeThread -> fetch_all_feeds -> save_articles, then the
      Articles Explorer shows load_articles output). Articles are written to a
      throwaway storage file so the real SCRAPED-RESULTS database is untouched.

  STEP C - COMPARE:
      Ground truth (A) is matched against the app-parsed articles (B) and the
      currently stored GUI database, reporting missing/garbled titles, missing
      links, broken dates and text-extraction quality.

Run with:  python3 scripts/feed_parse_audit.py
"""

import json
import os
import re
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CONFIG_PATH = PROJECT_ROOT / "config" / "feeds.json"

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    ),
    "Accept": "*/*",
}

REFERENCE_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def local_name(tag: str) -> str:
    """Returns local tag name ignoring any XML namespace."""
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def normalize_title(title: str) -> str:
    """Normalizes a title for identity comparison."""
    t = re.sub(r"<[^>]+>", "", title or "")
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


# ---------------------------------------------------------------------------
# STEP A: independent ping / ground truth
# ---------------------------------------------------------------------------
def ping_feed_raw(url: str, timeout: int = 15) -> Tuple[bool, str, Dict[str, Any]]:
    """Fetches raw bytes and parses RSS/Atom XML independently of the app."""
    try:
        req = urllib.request.Request(url, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            ctype = resp.info().get("Content-Type", "")
            status = resp.status
    except Exception as e:
        return False, f"FETCH ERROR: {type(e).__name__}: {e}", {}

    try:
        xml_str = raw.decode("utf-8", errors="replace")
        root = ET.fromstring(xml_str)
    except Exception as e:
        return True, f"XML PARSE ERROR: {type(e).__name__}: {e}", {}

    feed_title = ""
    feed_link = ""
    items: List[Dict[str, str]] = []

    root_tag = local_name(root.tag)
    if root_tag == "rss":
        channel = root.find("channel")
        if channel is not None:
            for ch in channel:
                if local_name(ch.tag) == "title":
                    feed_title = (ch.text or "").strip()
                elif local_name(ch.tag) == "link" and not feed_link:
                    feed_link = (ch.text or "").strip()
                elif local_name(ch.tag) == "item":
                    item = {"title": "", "link": "", "guid": "", "date": "", "description": "", "raw_html_desc": ""}
                    for f in ch:
                        nm = local_name(f.tag)
                        if nm == "title" and not item["title"]:
                            item["title"] = (f.text or "").strip()
                        elif nm == "link":
                            href = f.attrib.get("href")
                            if href:
                                item["link"] = href.strip()
                            elif f.text:
                                item["link"] = f.text.strip()
                        elif nm == "guid":
                            item["guid"] = (f.text or "").strip()
                        elif nm in ("pubDate", "published", "updated", "date") and not item["date"]:
                            item["date"] = (f.text or "").strip()
                        elif nm in ("description", "summary"):
                            item["description"] = (f.text or "").strip()
                            item["raw_html_desc"] = (f.text or "").strip()
                        elif nm == "encoded" and not item["description"]:
                            item["description"] = (f.text or "").strip()
                            item["raw_html_desc"] = (f.text or "").strip()
                    items.append(item)
    elif root_tag == "feed":
        for ch in root:
            nm = local_name(ch.tag)
            if nm == "title" and not feed_title:
                feed_title = (ch.text or "").strip()
            elif nm == "link" and not feed_link:
                feed_link = ch.attrib.get("href", "")
            elif nm == "entry":
                item = {"title": "", "link": "", "guid": "", "date": "", "description": "", "raw_html_desc": ""}
                for f in ch:
                    fn = local_name(f.tag)
                    if fn == "title" and not item["title"]:
                        item["title"] = (f.text or "").strip()
                    elif fn == "link":
                        rel = f.attrib.get("rel", "alternate")
                        href = f.attrib.get("href")
                        if href and (rel == "alternate" or not item["link"]):
                            item["link"] = href.strip()
                    elif fn == "id" and not item["guid"]:
                        item["guid"] = (f.text or "").strip()
                    elif fn in ("updated", "published", "date") and not item["date"]:
                        item["date"] = (f.text or "").strip()
                    elif fn in ("summary", "content") and not item["description"]:
                        item["description"] = (f.text or "").strip()
                        item["raw_html_desc"] = (f.text or "").strip()
                items.append(item)
    else:
        for item in root.iter():
            if local_name(item.tag) in ("item", "entry"):
                d = {"title": "", "link": "", "guid": "", "date": "", "description": "", "raw_html_desc": ""}
                for f in item:
                    fn = local_name(f.tag)
                    if fn == "title" and not d["title"]:
                        d["title"] = (f.text or "").strip()
                    elif fn == "link":
                        if f.attrib.get("href"):
                            d["link"] = f.attrib["href"].strip()
                        elif f.text:
                            d["link"] = f.text.strip()
                    elif fn == "guid" and not d["guid"]:
                        d["guid"] = (f.text or "").strip()
                    elif fn in ("pubDate", "published", "updated") and not d["date"]:
                        d["date"] = (f.text or "").strip()
                    elif fn in ("description", "summary") and not d["description"]:
                        d["description"] = (f.text or "").strip()
                        d["raw_html_desc"] = (f.text or "").strip()
                items.append(d)

    info = {
        "status": status,
        "content_type": ctype,
        "feed_title": feed_title,
        "feed_link": feed_link,
        "root_tag": root_tag,
        "items": items,
        "item_count": len(items),
    }
    return True, "OK", info


# ---------------------------------------------------------------------------
# STEP B: app pipeline (same as GUI "Ping" via RSS.desktop)
# ---------------------------------------------------------------------------
def run_app_pipeline(feed_config: Dict[str, Any]) -> Tuple[int, Dict[str, Any], List[Dict[str, Any]]]:
    """Runs fetch_feed + save_articles + load_articles in an isolated db."""
    from core.fetcher import fetch_feed
    from core.storage import save_articles, load_articles

    # Keep the audit deterministic: never fall back to the Playwright stealth
    # browser during the parse check. Use sys.modules because the submodule name
    # is shadowed by a same-named function in core/fetcher/__init__.py.
    import sys as _sys
    ff_mod = _sys.modules["core.fetcher.fetch_feed"]
    _orig_stealth = ff_mod.is_stealth_available
    ff_mod.is_stealth_available = lambda: False

    tmp_dir = Path(tempfile.mkdtemp(prefix="rss_audit_"))
    tmp_articles = tmp_dir / "audit.jsonl"
    tmp_dedup = tmp_dir / "audit_dedup.json"

    import core.storage as storage
    old_a = getattr(storage, "ARTICLES_FILE", None)
    old_d = getattr(storage, "DEDUP_FILE", None)
    old_r = getattr(storage, "RESULTS_DIR", None)
    storage.ARTICLES_FILE = tmp_articles
    storage.DEDUP_FILE = tmp_dedup
    storage.RESULTS_DIR = tmp_dir

    try:
        articles = fetch_feed(feed_config, extract_full_text=False, timeout=12)
        new_n, total_n = save_articles(articles)
        shown = load_articles(limit=1000)
        result = {"articles": articles, "new_n": new_n, "total_n": total_n, "shown": shown}
    finally:
        storage.ARTICLES_FILE = old_a
        storage.DEDUP_FILE = old_d
        storage.RESULTS_DIR = old_r
        ff_mod.is_stealth_available = _orig_stealth

    return tmp_dir, result, result["articles"]


def strip_html_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------------------
# STEP C: comparison
# ---------------------------------------------------------------------------
def compare(a_info: Dict[str, Any], app_articles: List[Dict[str, Any]]):
    real_items = a_info.get("items", [])
    real_titles = [normalize_title(i["title"]) for i in real_items if normalize_title(i["title"])]
    real_links = {i["link"] for i in real_items if i["link"]}
    real_count = len(real_items)

    app_titles = [normalize_title(a.get("title") or "") for a in app_articles]
    app_links = {a.get("url", "") for a in app_articles if a.get("url")}
    app_count = len(app_articles)

    # titles matched (real -> app)
    matched_titles = sum(1 for t in real_titles if t in app_titles)
    # links matched (real -> app)
    matched_links = sum(1 for l in real_links if l in app_links)

    # Items in real feed missing from app parse (by normalized title)
    app_title_set = set(app_titles)
    missing_titles = [t for t in dict.fromkeys(real_titles) if t not in app_title_set]
    # Garbage: app articles whose title is not in real feed
    real_title_set = set(real_titles)
    extra_titles = [t for t in dict.fromkeys(app_titles) if t not in real_title_set]

    # Date parse rate
    dated = sum(1 for a in app_articles if a.get("published_at_iso"))
    date_rate = (dated / app_count * 100) if app_count else 0.0

    # Text quality
    lens = [len(a.get("full_text_clean") or "") for a in app_articles]
    preview_lens = [len(a.get("preview") or "") for a in app_articles]
    text_clean_lens = [len(a.get("text_clean") or "") for a in app_articles]
    empty_text = sum(1 for l in text_clean_lens if l == 0)
    short_text = sum(1 for l in text_clean_lens if 0 < l < 100)
    avg_text = (sum(text_clean_lens) / len(text_clean_lens)) if text_clean_lens else 0
    avg_preview = (sum(preview_lens) / len(preview_lens)) if preview_lens else 0
    avg_full = (sum(lens) / len(lens)) if lens else 0

    return {
        "real_count": real_count,
        "app_count": app_count,
        "matched_titles": matched_titles,
        "matched_links": matched_links,
        "missing_titles": missing_titles[:8],
        "missing_title_count": len(missing_titles),
        "extra_titles": extra_titles[:8],
        "extra_title_count": len(extra_titles),
        "title_overlap_rate": (matched_titles / len(real_titles) * 100) if real_titles else 0.0,
        "date_rate": date_rate,
        "empty_text_count": empty_text,
        "short_text_count": short_text,
        "avg_text_len": avg_text,
        "avg_preview_len": avg_preview,
        "avg_full_text_len": avg_full,
    }


def load_live_db(feed_name: str) -> List[Dict[str, Any]]:
    from core.storage import load_articles
    return load_articles(limit=1000, feed_filter=feed_name)


def verdict(total_obj: Dict[str, Any], cmp_obj: Dict[str, Any], ping_ok: bool, parse_ok: bool) -> str:
    if not ping_ok:
        return "PING-FAIL"
    if not parse_ok:
        return "APP-PARSE-FAIL"
    if cmp_obj["real_count"] and cmp_obj["app_count"] == 0:
        return "FAIL (0 items parsed)"
    if cmp_obj["title_overlap_rate"] < 50:
        return "BAD PARSING (overlap < 50%)"
    if cmp_obj["app_count"] > 0 and (cmp_obj["empty_text_count"] / cmp_obj["app_count"]) > 0.3:
        return "EMPTY TEXT (no content extracted)"
    if cmp_obj["short_text_count"] / max(1, cmp_obj["app_count"]) > 0.5:
        return "SHORT TEXT (preview-only)"
    if cmp_obj["real_count"] > 0 and cmp_obj["missing_title_count"] >= max(1, int(cmp_obj["real_count"] * 0.5)):
        return "MISSING ITEMS (>=50% not parsed)"
    return "OK"


def main() -> int:
    if not CONFIG_PATH.exists():
        print(f"[FATAL] Config not found: {CONFIG_PATH}")
        return 1

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        feeds = data.get("feeds", []) if isinstance(data, dict) else data

    print("=" * 100)
    print("ONE-TIME RSS FEED PARSING AUDIT")
    print("Loop: (A) ping real feed -> (B) app pipeline [RSS.desktop GUI Ping] -> (C) compare")
    print("=" * 100)

    summary_rows: List[Dict[str, Any]] = []
    max_name = max((len(f.get("name", "?")) for f in feeds), default=8)

    for idx, feed in enumerate(feeds, 1):
        name = feed.get("name", "?")
        url = feed.get("url", "")
        cat = feed.get("category", "General")
        enabled = feed.get("enabled", True)

        print(f"\n{'─' * 100}")
        print(f"[{idx:02d}] {name:<{max_name}} | {cat} | {'ENABLED' if enabled else 'DISABLED'}")
        print(f"    URL: {url}")

        # STEP A - ping real feed
        ping_ok, msg, a_info = ping_feed_raw(url)
        real_count = a_info.get("item_count", 0)
        feed_title = a_info.get("feed_title", "")
        print(f"[A] PING: {'OK' if ping_ok else 'FAIL'} | {msg}")
        if ping_ok:
            print(f"    Real feed title: {feed_title or '(none)'}")
            print(f"    Real item count: {real_count}  (root: {a_info.get('root_tag', '?')}, ct: {a_info.get('content_type', '?')})")

        # STEP B - app pipeline
        parse_status = "OK"
        app_articles: List[Dict[str, Any]] = []
        if ping_ok:
            try:
                _dir, result, app_articles = run_app_pipeline(feed)
                app_count = len(app_articles)
                print(f"[B] APP PIPELINE: parsed {app_count} item(s)")
            except Exception as e:
                parse_status = f"ERROR: {type(e).__name__}: {e}"
                print(f"[B] APP PIPELINE: FAILED - {parse_status}")
        else:
            print("[B] APP PIPELINE: skipped (feed unreachable)")

        # STEP C - compare (only when both sides available)
        cmp_obj: Dict[str, Any] = {}
        if ping_ok and parse_status == "OK":
            cmp_obj = compare(a_info, app_articles)
            print(f"[C] COMPARE: real={cmp_obj['real_count']} app={cmp_obj['app_count']} "
                  f"title-overlap={cmp_obj['title_overlap_rate']:.0f}% "
                  f"matched-titles={cmp_obj['matched_titles']}/{len(a_info.get('items', []))} "
                  f"matched-links={cmp_obj['matched_links']} "
                  f"date-rate={cmp_obj['date_rate']:.0f}% "
                  f"empty-text={cmp_obj['empty_text_count']} short-text={cmp_obj['short_text_count']}")
            print(f"    avg text len: {cmp_obj['avg_text_len']:.0f} | avg preview len: {cmp_obj['avg_preview_len']:.0f} "
                  f"| avg full-text len: {cmp_obj['avg_full_text_len']:.0f}")
            if cmp_obj["missing_titles"]:
                print(f"    MISSING from app parse ({cmp_obj['missing_title_count']}):")
                for t in cmp_obj["missing_titles"]:
                    print(f"      - {t[:90]}")
            if cmp_obj["extra_titles"]:
                print(f"    Extra in app (not in feed) ({cmp_obj['extra_title_count']}):")
                for t in cmp_obj["extra_titles"]:
                    print(f"      + {t[:90]}")

        # GUI live database comparison
        live = load_live_db(name)
        live_lens = [len(a.get("text_clean") or "") for a in live]
        live_avg = (sum(live_lens) / len(live_lens)) if live_lens else 0
        live_empty = sum(1 for l in live_lens if l == 0)
        print(f"    GUI DB (live jsonl): {len(live)} article(s) for '{name}' | "
              f"avg text len={live_avg:.0f} | empty={live_empty}")

        v = verdict({}, cmp_obj, ping_ok, parse_status == "OK")
        print(f"    VERDICT: {v}")
        summary_rows.append({
            "name": name, "url": url, "ping": "OK" if ping_ok else "FAIL",
            "real": real_count, "app": len(app_articles),
            "overlap": cmp_obj.get("title_overlap_rate", 0),
            "missing": cmp_obj.get("missing_title_count", 0),
            "empty": cmp_obj.get("empty_text_count", 0),
            "short": cmp_obj.get("short_text_count", 0),
            "db_count": len(live), "db_avg": live_avg,
            "verdict": v,
        })

    print(f"\n{'=' * 100}")
    print("SUMMARY TABLE")
    print(f"{'FEED':<30}{'PING':<6}{'REAL':<7}{'APP':<6}{'OVLP%':<8}{'MISS':<7}{'EMPTY':<8}{'SHORT':<8}{'DB':<6}{'DB_AVG':<9}VERDICT")
    print(f"{'-' * 100}")
    for r in summary_rows:
        print(f"{r['name'][:30]:<30}{r['ping']:<6}{r['real']:<7}{r['app']:<6}{r['overlap']:>6.0f}% {r['missing']:<5}{r['empty']:<8}{r['short']:<8}{r['db_count']:<6}{r['db_avg']:>7.0f}  {r['verdict']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())