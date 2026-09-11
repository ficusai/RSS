"""
Unit Test Suite for Web Scraper Fallback (Git Branch: feature/web-scraper-fallback)
"""

import unittest
from features.feature_web_scraper_fallback.implementation.web_scraper_fallback import (
    fetch_full_page_text,
    clean_html_simple,
)


class TestWebScraperFallback(unittest.TestCase):
    def test_clean_html_simple(self):
        sample = "<p>Article text preview</p><script>console.log(1);</script>"
        clean = clean_html_simple(sample)
        self.assertEqual(clean, "Article text preview")

    def test_invalid_url_fallback(self):
        res = fetch_full_page_text("invalid_url")
        self.assertEqual(res, "")


if __name__ == "__main__":
    unittest.main()
