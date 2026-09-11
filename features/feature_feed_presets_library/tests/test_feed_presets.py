"""
Unit Test Suite for Feed Presets Library (Git Branch: feature/feed-presets-library)
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from features.feature_feed_presets_library.implementation.feeds_presets import (
    get_preset_feeds,
    get_preset_categories,
    get_presets_by_category,
    search_presets,
    feed_already_present,
    PRESET_FEEDS,
    PRESET_CATEGORIES,
)


class TestFeedPresets(unittest.TestCase):
    def test_preset_feeds_non_empty(self):
        presets = get_preset_feeds()
        self.assertGreater(len(presets), 0)
        self.assertGreaterEqual(len(presets), 400)

    def test_preset_structure(self):
        for p in PRESET_FEEDS:
            self.assertIn("name", p)
            self.assertIn("url", p)
            self.assertIn("category", p)
            self.assertIsInstance(p["name"], str)
            self.assertIsInstance(p["url"], str)
            self.assertIsInstance(p["category"], str)

    def test_preset_urls_valid(self):
        for p in PRESET_FEEDS:
            self.assertTrue(p["url"].startswith("http"), f"Invalid URL: {p['url']}")

    def test_returns_copies(self):
        presets = get_preset_feeds()
        presets.append({"name": "Mutant", "url": "http://mutant", "category": "X"})
        self.assertEqual(len(get_preset_feeds()), len(PRESET_FEEDS))

    def test_15_plus_categories(self):
        cats = get_preset_categories()
        self.assertGreaterEqual(len(cats), 15)
        self.assertEqual(len(set(cats)), len(cats), "Categories must be unique")
        self.assertEqual(cats, PRESET_CATEGORIES)

    def test_categories_clean_names(self):
        for c in PRESET_CATEGORIES:
            self.assertNotIn("(", c, f"Category should not contain parentheses: {c}")
            self.assertNotIn("Additional", c)
            self.assertNotIn("Extended", c)
            self.assertNotIn("Curated", c)
            self.assertNotIn("Expanded", c)

    def test_all_categories_represented(self):
        used = {p["category"] for p in PRESET_FEEDS}
        self.assertEqual(used, set(PRESET_CATEGORIES))

    def test_get_presets_by_category(self):
        tech = get_presets_by_category("Technology")
        self.assertGreater(len(tech), 0)
        for p in tech:
            self.assertEqual(p["category"], "Technology")

    def test_get_presets_by_category_case_insensitive(self):
        tech = get_presets_by_category("technology")
        self.assertGreater(len(tech), 0)

    def test_get_presets_by_category_all(self):
        self.assertEqual(len(get_presets_by_category("all")), len(PRESET_FEEDS))

    def test_get_presets_by_category_empty(self):
        self.assertEqual(len(get_presets_by_category("NoSuchCategory")), 0)

    def test_search_presets(self):
        results = search_presets("TechCrunch")
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(all("techcrunch" in r["url"] for r in results))

    def test_search_presets_by_category(self):
        results = search_presets("crypto")
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertEqual(r["category"].lower(), "crypto & forex")

    def test_search_presets_empty_query(self):
        self.assertEqual(len(search_presets("")), len(PRESET_FEEDS))

    def test_feed_already_present(self):
        existing = [
            {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"},
            {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/rss.xml", "category": "World News"},
        ]
        preset = {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"}
        self.assertTrue(feed_already_present(preset, existing))

        new_preset = {"name": "Nature", "url": "https://www.nature.com/nature.rss", "category": "Science"}
        self.assertFalse(feed_already_present(new_preset, existing))

    def test_feed_already_present_empty(self):
        self.assertFalse(feed_already_present({"name": "X", "url": "http://x"}, []))
        self.assertFalse(feed_already_present({"name": "X", "url": "http://x"}, None))

    def test_no_duplicate_feeds_by_url(self):
        urls = {p["url"] for p in PRESET_FEEDS}
        self.assertEqual(len(urls), len(PRESET_FEEDS), "Preset catalog contains duplicate URLs")


if __name__ == "__main__":
    unittest.main()