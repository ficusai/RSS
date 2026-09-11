"""
Unit Test Suite for Web Scraper Fallback (Git Branch: feature/web-scraper-fallback)
"""

import unittest
from unittest.mock import patch, MagicMock
from features.feature_web_scraper_fallback.implementation.web_scraper_fallback import (
    fetch_full_page_text,
    clean_html_simple,
)


class TestWebScraperFallback(unittest.TestCase):
    def test_clean_html_simple(self):
        sample = "<p>Article text preview</p><script>console.log(1);</script>"
        clean = clean_html_simple(sample)
        self.assertEqual(clean, "Article text preview")

        self.assertEqual(clean_html_simple(None), "")
        self.assertEqual(clean_html_simple(123), "")
        self.assertEqual(clean_html_simple(""), "")
        self.assertEqual(clean_html_simple("&amp; &lt;hello&gt;"), "& <hello>")

    def test_invalid_url_fallback(self):
        res = fetch_full_page_text("invalid_url")
        self.assertEqual(res, "")
        self.assertEqual(fetch_full_page_text("ftp://example.com"), "")

    @patch("urllib.request.urlopen")
    def test_fetch_full_page_text_success(self, mock_urlopen):
        html_content = """
        <html>
            <body>
                <article>
                    <p>This is a sufficiently long valid paragraph of text extracted from an article webpage.</p>
                    <p>Short</p>
                    <p>This is another valid paragraph with sufficient length to pass the threshold check.</p>
                    <p>All rights reserved on this website.</p>
                </article>
            </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.read.return_value = html_content.encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        text = fetch_full_page_text("https://example.com/article")
        self.assertIn("This is a sufficiently long valid paragraph", text)
        self.assertIn("This is another valid paragraph", text)
        self.assertNotIn("Short", text)
        self.assertNotIn("All rights reserved", text)

    @patch("urllib.request.urlopen")
    def test_fetch_full_page_text_exception(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection error")
        text = fetch_full_page_text("https://example.com/article")
        self.assertEqual(text, "")


if __name__ == "__main__":
    unittest.main()
