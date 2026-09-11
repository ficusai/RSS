"""
Comprehensive Unit & Integration Test Suite for RSS Feed Tracker & Scraper.
Tests core cleaner, storage, fetcher, scheduler, and main entrypoint functions.
"""

import sys
import json
import gzip
import zlib
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
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
from core.fetcher import _local_tag, _parse_item_element, fetch_feed, fetch_all_feeds, parse_xml_bytes
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


class TestParseXmlBytesUnicodePreservation(unittest.TestCase):
    """Regression: the old allow-list regex mangled every non-ASCII character.

    Python backslash-x escapes consume only 2 hex digits, so the old pattern
    `[^x09 x0A x0D -xD7FF ...]` was misparsed and stripped Lambda, en/em
    dashes, curly quotes, apostrophes and n-tilde from titles/body text.
    """

    FEED_CONFIG = {"name": "Unicode Feed", "url": "http://example.com/feed", "category": "News"}

    def test_non_ascii_titles_preserved(self):
        xml = (
            "<rss version=\"2.0\"><channel>"
            "<item><title>Λ Snap – An inviting programming language — “it’s hell” ¿qué tal? </title>"
            "<link>http://example.com/1</link><guid>g1</guid>"
            "<description>&lt;p&gt;Café ñandú — prices&#160;surge&lt;/p&gt;</description>"
            "</item>"
            "</channel></rss>"
        )
        raw = xml.encode("utf-8")
        arts = parse_xml_bytes(raw, self.FEED_CONFIG)
        self.assertEqual(len(arts), 1)
        self.assertEqual(
            arts[0]["title"],
            "Λ Snap – An inviting programming language — “it’s hell” ¿qué tal?",
        )
        self.assertIn("Café ñandú — prices surge", arts[0]["text_clean"])

    def test_control_chars_still_removed(self):
        xml = ("<rss version=\"2.0\"><channel>"
               "<item><title>Clean</title><link>http://example.com/1</link>"
               "<guid>g2</guid><description>a\x00b\x1fc</description></item>"
               "</channel></rss>")
        arts = parse_xml_bytes(xml.encode("utf-8"), self.FEED_CONFIG)
        self.assertEqual(arts[0]["text_clean"], "abc")

    def test_rsshub_html_response_rejected_not_silently_corrupted(self):
        # Malformed HTML served by a proxy must raise, not silently produce mangled articles.
        with self.assertRaises(ET.ParseError):
            parse_xml_bytes(b"<html><body>Cloudflare challenge</body>", self.FEED_CONFIG)


class TestContentDecoding(unittest.TestCase):
    """Validates gzip/deflate/brotli decoding used by fetch_url_bytes."""

    def _fetch_module(self):
        import importlib
        return importlib.import_module("core.fetcher.fetch_url_bytes")

    def test_decompress_gzip(self):
        raw = gzip.compress(b"hello gzip")
        self.assertEqual(self._fetch_module()._decompress(raw, "gzip"), b"hello gzip")

    def test_decompress_deflate_zlib(self):
        raw = zlib.compress(b"hello deflate")
        self.assertEqual(self._fetch_module()._decompress(raw, "deflate"), b"hello deflate")

    def test_decompress_deflate_raw(self):
        comp = zlib.compressobj(wbits=-zlib.MAX_WBITS)
        raw = comp.compress(b"hello raw") + comp.flush()
        self.assertEqual(self._fetch_module()._decompress(raw, "deflate"), b"hello raw")

    def test_decompress_brotli(self):
        mod = self._fetch_module()
        if not mod.BROTLI_AVAILABLE:
            self.skipTest("brotli not installed")
        raw = mod.brotli.compress(b"hello brotli")
        self.assertEqual(mod._decompress(raw, "br"), b"hello brotli")

    def test_decompress_unknown_returns_raw(self):
        self.assertEqual(self._fetch_module()._decompress(b"plain", "identity"), b"plain")

    def test_accept_encoding_only_supported(self):
        enc = self._fetch_module()._build_accept_encoding()
        self.assertIn("gzip", enc)
        self.assertIn("deflate", enc)
        self.assertNotIn("zstd", enc)

    def test_end_to_end_brotli_fetch(self):
        mod = self._fetch_module()
        if not mod.BROTLI_AVAILABLE:
            self.skipTest("brotli not installed")

        payload = b"<rss><channel><item><title>br article</title></item></channel></rss>"
        encoded = mod.brotli.compress(payload)

        class Handler(BaseHTTPRequestHandler):
            enc = "br"

            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/rss+xml")
                self.send_header("Content-Encoding", self.enc)
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        port = server.server_address[1]
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        try:
            from core.fetcher import fetch_url_bytes
            body = fetch_url_bytes(f"http://127.0.0.1:{port}/rss", timeout=10)
            self.assertEqual(body, payload)
        finally:
            server.shutdown()
            server.server_close()
            t.join(timeout=5)


class TestExtractArticleText(unittest.TestCase):
    def _extract(self, html):
        import core.extractors.extract_article_text as mod
        return mod.extract_article_text(html, url="http://example.com/a")

    def test_inline_tags_do_not_split_paragraphs(self):
        html = (
            "<html><head><title>T</title></head><body><article>"
            "<p>In <a href='#'>a blog post</a>, the <code>maker</code> said it was "
            "<strong>serious</strong>.</p>"
            "<p>Second paragraph with more details and enough length to survive.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertIn("In a blog post, the maker said it was serious.", result["clean_text"])
        self.assertNotIn("pose\n", result["clean_text"])
        self.assertEqual(result["clean_text"].count("\n\n"), 1)

    def test_paragraph_structure_preserved(self):
        html = (
            "<html><body><article>"
            "<p>First real paragraph of the story with plenty of words here.</p>"
            "<p>Second real paragraph of the story with plenty of words here.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertTrue(result["clean_text"].startswith("First real paragraph"))
        self.assertIn("\n\nSecond real paragraph", result["clean_text"])

    def test_boilerplate_blocks_pruned(self):
        html = (
            "<html><body><article>"
            "<p>Hardware wallet maker Trezor is warning its users about a phishing "
            "campaign that tries to drain their devices.</p>"
            "<section class='most-popular'><h3>Most Popular</h3><a>Story One</a>"
            "<a>Story Two</a></section>"
            "<p>Don't miss out on our conference October 13-15 San Francisco. "
            "REGISTER NOW and get a free ticket.</p>"
            "<p>by John Doe</p>"
            "<p>The company said this vulnerability affected several models.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("Most Popular", result["clean_text"])
        self.assertNotIn("REGISTER", result["clean_text"])
        self.assertNotIn("by John Doe", result["clean_text"])
        self.assertIn("phishing", result["clean_text"])
        self.assertIn("affected several models", result["clean_text"])

    def test_byline_gallery_rows_removed(self):
        html = (
            "<html><body><article>"
            "<p>OEIStreams</p><p>by mobility212</p>"
            "<p>ScratchJr</p><p>by dana-dai</p>"
            "<p>This is the genuine introduction to the project with enough words "
            "to be kept by the extractor.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("mobility212", result["clean_text"])
        self.assertNotIn("OEIStreams", result["clean_text"])
        self.assertIn("genuine introduction", result["clean_text"])

    def test_continue_reading_artifact_removed(self):
        html = (
            "<html><body><article>"
            "<p>The full article text that the publisher provided in full with "
            "enough length to survive extraction cleanly.</p>"
            "<p>Continue reading...</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("Continue reading", result["clean_text"])

    def test_nav_intro_lines_trimmed(self):
        html = (
            "<html><body><article>"
            "<p>Previous</p><p>Next</p><p>Welcome to Snap!</p>"
            "<p>Here begins the actual documentation of the project in detail.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("Welcome to Snap!", result["clean_text"])
        self.assertTrue(result["clean_text"].startswith("Here begins"), result["clean_text"])

    def test_unwanted_sections_removed(self):
        html = (
            "<html><body>"
            "<header>Site Header Navigation Links Galore</header>"
            "<footer>Copyright 2026 All Rights Reserved</footer>"
            "<article><p>A real article paragraph that survives extraction with "
            "sufficient length to be counted as news content.</p></article>"
            "</body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("Site Header", result["clean_text"])
        self.assertNotIn("All Rights Reserved", result["clean_text"])
        self.assertIn("real article paragraph", result["clean_text"])

    def test_link_dense_headline_boxes_removed(self):
        html = (
            "<html><body><article>"
            "<div class='mobility-box'>"
            "<p><a href='/1'>Tesla cybercab hits the road and hits a snag</a></p>"
            "<p><a href='/2'>Hikers rescued after using Google Gemini for planning</a></p>"
            "</div>"
            "<p>The real reporting about the crypto wallet breach follows here with "
            "enough words to pass the minimum bar comfortably.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("cybercab", result["clean_text"])
        self.assertNotIn("Gemini", result["clean_text"])
        self.assertIn("crypto wallet breach", result["clean_text"])

    def test_link_only_headings_dropped_but_headline_kept(self):
        html = (
            "<html><body><article>"
            "<h1><a href='/article'>A Real Long Headline That Describes The Story</a></h1>"
            "<p>First paragraph delivering the actual news with plenty of text so it "
            "survives the boilerplate heuristics unchanged and intact.</p>"
            "<section class='most-popular'><h2>Most Popular</h2>"
            "<h3><a href='/x'>Documentary stuns Telluride festival</a></h3>"
            "<h3><a href='/y'>TechCrunch Mobility Tesla cybercab hits the road</a></h3>"
            "</section>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertIn("Real Long Headline", result["clean_text"])
        self.assertNotIn("Documentary stuns Telluride", result["clean_text"])
        self.assertNotIn("Mobility Tesla cybercab", result["clean_text"])
        self.assertIn("delivering the actual news", result["clean_text"])

    def test_trailing_comment_bullet_line_removed(self):
        html = (
            "<html><body><article>"
            "<p>The article body is genuine and long enough to survive extraction "
            "while other lines get cleaned away from the endings here.</p>"
            "<p>joshenders commented Dec 7, 2023 •</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("joshenders commented", result["clean_text"])

    def test_ui_chrome_terms_removed(self):
        html = (
            "<html><body><article>"
            "<div>Select an option</div>"
            "<div>No results found</div>"
            "<div>Learn more about clone URLs</div>"
            "<p>The switch to swap files is straightforward on modern Linux systems "
            "and removes an entire class of disk layout problems.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("Select an option", result["clean_text"])
        self.assertNotIn("No results found", result["clean_text"])
        self.assertNotIn("clone URLs", result["clean_text"])
        self.assertIn("swap files", result["clean_text"])
        self.assertTrue(result["clean_text"].startswith("The switch to swap files"))

    def test_event_promo_copy_removed(self):
        html = (
            "<html><body><article>"
            "<p>Disrupt 2026: OpenAI, Anthropic, Replit, and more take over 6 "
            "industry stages. 25% off tickets now.</p>"
            "<p>Back by popular demand: Save up to $300 on Disrupt.</p>"
            "<p>The scammers targeted customers right after the vendor confirmed a "
            "breach at its marketing email provider over the weekend.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("tickets", result["clean_text"])
        self.assertNotIn("Save up to", result["clean_text"])
        self.assertNotIn("Disrupt 2026", result["clean_text"])
        self.assertIn("marketing email provider", result["clean_text"])

    def test_curly_apostrophe_boilerplate_removed(self):
        html = (
            "<html><body><article>"
            "<p>Don\u2019t miss out. The startup community will gather to answer a "
            "pivotal question: How do you build sustainably in the AI era?</p>"
            "<p>The genuine reporting with a decent number of words follows the "
            "promo paragraph and should be the last block that remains.</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn("miss out", result["clean_text"])
        self.assertIn("genuine reporting", result["clean_text"])

    def test_ui_fragment_tail_removed(self):
        html = (
            "<html><body><article>"
            "<p>The substantive article body that survives the extraction by "
            "having enough real content to pass every single filter here.</p>"
            "<p>.com</p>"
            "</article></body></html>"
        )
        result = self._extract(html)
        self.assertNotIn(".com", result["clean_text"])
        self.assertTrue(result["clean_text"].endswith("filter here."), result["clean_text"])

    def test_empty_html(self):
        result = self._extract("")
        self.assertEqual(result["clean_text"], "")
        self.assertEqual(result["word_count"], 0)


class TestPreviewDerivation(unittest.TestCase):
    def _parse_item(self, description, content):
        import xml.etree.ElementTree as ET
        from core.fetcher import parse_item_element
        xml = (
            "<item xmlns:content=\"http://purl.org/rss/1.0/modules/content/\">"
            f"<title>Demo Title</title>"
            f"<link>http://example.com/demo</link>"
            f"<description>{description}</description>"
            f"<content:encoded>{content}</content:encoded>"
            "</item>"
        )
        root = ET.fromstring(xml)
        feed_config = {
            "url": "http://example.com/rss",
            "name": "Demo Feed",
            "category": "Tech",
        }
        return parse_item_element(root, feed_config, extract_full_text=False)

    def test_trivial_comments_description_uses_full_text_lead(self):
        desc = (
            "&lt;p&gt;&lt;a href=&quot;https://news.ycombinator.com/item?id=4&quot;"
            "&gt;Comments&lt;/a&gt;&lt;/p&gt;"
        )
        content = (
            "Swap files have had the same performance characteristics as swap "
            "partitions for more than twenty years now."
        )
        item = self._parse_item(desc, content)
        self.assertNotEqual(item["preview"], "Comments")
        self.assertNotIn("Comments", item["preview"])
        self.assertEqual(item["preview"], content)
        self.assertEqual(item["full_text_clean"], content)

    def test_substantive_description_kept_as_preview(self):
        desc = "Trezor is warning users about a phishing campaign targeting wallets."
        content = "A much longer full article body that would follow the summary."
        item = self._parse_item(desc, content)
        self.assertEqual(item["preview"], desc)
        self.assertEqual(item["full_text_clean"], content)


class TestCleanerReplacement(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.patch_results_dir = Path(self.temp_dir.name)

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

    def _article(self, title, text, preview="Preview lead here."):
        return {
            "article_id": "clean_repl_hash",
            "feed_name": "Test Feed",
            "feed_url": "http://example.com/rss",
            "category": "Tech",
            "title": title,
            "author": "Alice",
            "url": "http://example.com/1",
            "guid": "guide1",
            "published_at_iso": "2026-09-11T10:00:00Z",
            "scraped_at_iso": "2026-09-11T10:00:00Z",
            "preview": preview,
            "text_clean": text,
            "tags": [],
        }

    def _sum_preview_problem(self):
        junk = (
            "Most Popular Stories REGISTER NOW Don't miss out Subscribe to our "
            "newsletter Today's deals Sponsored content you may also like follow us "
            + ("boilerplate padding words " * 10)
        )
        return junk

    def test_cleaner_shorter_text_replaces_junk(self):
        from core.storage import save_articles, load_articles
        junk = self._sum_preview_problem()
        save_articles([self._article("A", junk)])
        self.assertIn("Most Popular", load_articles()[0]["text_clean"])

        clean = (
            "Hardware wallet maker Trezor is warning users about a phishing "
            "campaign that tries to drain their devices."
        )
        new_count, total = save_articles([self._article("A", clean)])
        self.assertEqual(new_count, 1)
        loaded = load_articles()
        self.assertEqual(len(loaded), 1)
        self.assertNotIn("Most Popular", loaded[0]["text_clean"])

    def test_short_clean_text_does_not_clobber_long_real_text(self):
        from core.storage import save_articles, load_articles
        real = (
            "The full and substantive article body with many paragraphs of "
            "genuine news reporting that goes on for quite some length. " * 3
        )
        save_articles([self._article("B", real)])
        short = "Just a tiny snippet with no junk markers."
        save_articles([self._article("B", short)])
        loaded = load_articles()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["text_clean"], real)

    def test_new_extractor_version_refreshes_existing_row(self):
        from core.storage import save_articles, load_articles
        seed = self._article("V", "old text without boilerplate markers but long")
        seed["extractor_version"] = 1
        save_articles([seed])
        upgraded = self._article("V", "brand new compact clean text without markers")
        upgraded["extractor_version"] = 2
        new_count, _ = save_articles([upgraded])
        self.assertEqual(new_count, 1)
        loaded = load_articles()[0]
        self.assertEqual(loaded["extractor_version"], 2)
        self.assertEqual(loaded["text_clean"], "brand new compact clean text without markers")


if __name__ == "__main__":
    unittest.main()
