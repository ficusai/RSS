"""
Comprehensive Unit & Integration Test Suite for RSS Feed Tracker & Scraper.
Tests core cleaner, storage, fetcher, scheduler, and main entrypoint functions.
"""

import sys
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.cleaner import clean_html, parse_to_iso
from core.storage import (
    generate_article_id,
    is_duplicate,
    save_articles,
    get_stats,
    load_articles,
    RESULTS_DIR,
    ARTICLES_FILE,
    DEDUP_FILE,
)
from core.fetcher import _local_tag, _parse_item_element, fetch_feed, fetch_all_feeds
from core.scheduler import get_timer_status
import xml.etree.ElementTree as ET


class TestCleanerModule(unittest.TestCase):
    def test_clean_html_basic(self):
        raw = "<p>Hello &amp; <b>World</b>!</p><script>var x=1;</script>"
        clean = clean_html(raw)
        self.assertEqual(clean, "Hello & World !")

    def test_clean_html_edge_cases(self):
        self.assertEqual(clean_html(""), "")
        self.assertEqual(clean_html(None), "")
        self.assertEqual(clean_html(123), "")
        self.assertEqual(clean_html("<style>body{color:red;}</style>Content"), "Content")

    def test_parse_to_iso_rfc822(self):
        rfc_date = "Thu, 10 Sep 2026 20:00:00 GMT"
        iso_str = parse_to_iso(rfc_date)
        self.assertEqual(iso_str, "2026-09-10T20:00:00Z")

    def test_parse_to_iso_iso8601(self):
        iso_input = "2026-09-10T20:00:00Z"
        iso_output = parse_to_iso(iso_input)
        self.assertEqual(iso_output, "2026-09-10T20:00:00Z")

    def test_parse_to_iso_fallback(self):
        fallback = parse_to_iso("Invalid Date String")
        # Should return a valid ISO timestamp format string ending in Z
        self.assertTrue(fallback.endswith("Z"))
        self.assertIn("T", fallback)


class TestStorageModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.patch_results_dir = Path(self.temp_dir.name)
        
        # Patch storage module paths during tests
        import core.storage as storage_mod
        self.orig_results = storage_mod.RESULTS_DIR
        self.orig_articles = storage_mod.ARTICLES_FILE
        self.orig_dedup = storage_mod.DEDUP_FILE
        
        storage_mod.RESULTS_DIR = self.patch_results_dir
        storage_mod.ARTICLES_FILE = self.patch_results_dir / "scraped_articles.jsonl"
        storage_mod.DEDUP_FILE = self.patch_results_dir / "dedup_state.json"

    def tearDown(self):
        import core.storage as storage_mod
        storage_mod.RESULTS_DIR = self.orig_results
        storage_mod.ARTICLES_FILE = self.orig_articles
        storage_mod.DEDUP_FILE = self.orig_dedup
        self.temp_dir.cleanup()

    def test_generate_article_id(self):
        id1 = generate_article_id("http://feed.com", "http://item.com/1", "Title 1", "guid123")
        id2 = generate_article_id("http://feed.com", "http://item.com/1", "Title 1", "guid123")
        self.assertEqual(id1, id2)
        self.assertEqual(len(id1), 64)

    def test_save_and_load_articles(self):
        sample_articles = [
            {
                "article_id": "test_hash_1",
                "feed_name": "Test Feed",
                "feed_url": "http://example.com/rss",
                "category": "Technology",
                "title": "Test Title 1",
                "author": "Alice",
                "url": "http://example.com/1",
                "published_at_iso": "2026-09-11T10:00:00Z",
                "scraped_at_iso": "2026-09-11T10:00:00Z",
                "summary_raw": "<p>Raw text</p>",
                "text_clean": "Raw text",
                "tags": ["tech", "ai"],
            }
        ]
        new_count, total_count = save_articles(sample_articles)
        self.assertEqual(new_count, 1)
        self.assertEqual(total_count, 1)

        loaded = load_articles()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "Test Title 1")

        # Test duplicate prevention
        new_count2, total_count2 = save_articles(sample_articles)
        self.assertEqual(new_count2, 0)
        self.assertEqual(total_count2, 1)

    def test_update_incomplete_article(self):
        incomplete_art = {
            "article_id": "test_hash_update",
            "feed_name": "Test Feed",
            "feed_url": "http://example.com/rss",
            "category": "Technology",
            "title": "Incomplete Article",
            "author": "Bob",
            "url": "http://example.com/2",
            "published_at_iso": "2026-09-11T10:00:00Z",
            "scraped_at_iso": "2026-09-11T10:00:00Z",
            "summary_raw": "",
            "text_clean": "",
            "tags": [],
        }
        save_articles([incomplete_art])
        self.assertEqual(load_articles()[0]["text_clean"], "")

        # Now re-save with complete text
        complete_art = dict(incomplete_art)
        complete_art["text_clean"] = "Full body content now present"

        updated_count, total_count = save_articles([complete_art])
        self.assertEqual(updated_count, 1)
        self.assertEqual(load_articles()[0]["text_clean"], "Full body content now present")

    def test_search_and_category_filter(self):
        art1 = {
            "article_id": "id_1",
            "feed_name": "Tech Times",
            "category": "Technology",
            "title": "Python 3.14 Released",
            "text_clean": "Python is awesome",
            "url": "http://test.com/1",
        }
        art2 = {
            "article_id": "id_2",
            "feed_name": "World News",
            "category": "World",
            "title": "Global Summit Meets",
            "text_clean": "Leaders gather today",
            "url": "http://test.com/2",
        }
        save_articles([art1, art2])

        tech_res = load_articles(category="Technology")
        self.assertEqual(len(tech_res), 1)
        self.assertEqual(tech_res[0]["title"], "Python 3.14 Released")

        search_res = load_articles(search_query="Python")
        self.assertEqual(len(search_res), 1)
        self.assertEqual(search_res[0]["article_id"], "id_1")

    def test_get_stats(self):
        art = {"article_id": "id_stat", "feed_name": "Stat Feed", "url": "http://stat.com"}
        save_articles([art])
        stats = get_stats()
        self.assertEqual(stats["total_articles"], 1)
        self.assertEqual(stats["dedup_count"], 1)
        self.assertTrue(stats["storage_file_exists"])


class TestFetcherModule(unittest.TestCase):
    def test_local_tag(self):
        elem = ET.Element("{http://www.w3.org/2005/Atom}entry")
        self.assertEqual(_local_tag(elem), "entry")

        elem_rss = ET.Element("item")
        self.assertEqual(_local_tag(elem_rss), "item")

    def test_parse_rss_item_preview_and_full_content(self):
        xml_str = """<item xmlns:content="http://purl.org/rss/1.0/modules/content/">
            <title>Sample RSS Title</title>
            <link>http://example.com/rss1</link>
            <guid>guid-100</guid>
            <pubDate>Thu, 10 Sep 2026 12:00:00 GMT</pubDate>
            <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">John Doe</dc:creator>
            <description>&lt;p&gt;Short blurb summary&lt;/p&gt;</description>
            <content:encoded>&lt;p&gt;Detailed multi-paragraph full article content text.&lt;/p&gt;</content:encoded>
        </item>"""
        elem = ET.fromstring(xml_str)
        feed_config = {"name": "Test RSS", "url": "http://example.com/rss", "category": "News"}
        parsed = _parse_item_element(elem, feed_config)

        self.assertEqual(parsed["title"], "Sample RSS Title")
        self.assertEqual(parsed["preview"], "Short blurb summary")
        self.assertEqual(parsed["full_text_clean"], "Detailed multi-paragraph full article content text.")
        self.assertEqual(parsed["text_clean"], "Detailed multi-paragraph full article content text.")
        self.assertEqual(parsed["published_at_iso"], "2026-09-10T12:00:00Z")

    def test_parse_atom_entry(self):
        xml_str = """<entry xmlns="http://www.w3.org/2005/Atom">
            <title>Atom Entry Title</title>
            <link href="http://example.com/atom1" rel="alternate"/>
            <id>atom-id-200</id>
            <updated>2026-09-10T15:30:00Z</updated>
            <author><name>Jane Smith</name></author>
            <content type="html">&lt;p&gt;Atom body content&lt;/p&gt;</content>
        </entry>"""
        elem = ET.fromstring(xml_str)
        feed_config = {"name": "Test Atom", "url": "http://example.com/atom", "category": "Tech"}
        parsed = _parse_item_element(elem, feed_config)

        self.assertEqual(parsed["title"], "Atom Entry Title")
        self.assertEqual(parsed["url"], "http://example.com/atom1")
        self.assertEqual(parsed["author"], "Jane Smith")
        self.assertEqual(parsed["text_clean"], "Atom body content")
        self.assertEqual(parsed["published_at_iso"], "2026-09-10T15:30:00Z")


class TestSchedulerModule(unittest.TestCase):
    def test_get_timer_status_structure(self):
        status = get_timer_status()
        self.assertIn("installed", status)
        self.assertIn("active", status)
        self.assertIn("enabled", status)
        self.assertIn("detail", status)


if __name__ == "__main__":
    unittest.main()
