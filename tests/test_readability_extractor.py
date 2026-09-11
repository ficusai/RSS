"""
Unit tests for ReadabilityExtractor module.
"""

import unittest
from core.readability import ReadabilityExtractor


class TestReadabilityExtractor(unittest.TestCase):
    """Unit tests for Readability & Full-Text Content Extractor."""

    def test_extract_strips_noise_and_isolates_content(self):
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Sample Article Title</title></head>
        <body>
            <header><nav>Home | About | Contact</nav></header>
            <div class="ad">Banner Advertisement</div>
            <article>
                <h1>Sample Article Title</h1>
                <p>This is the first paragraph of the actual article content.</p>
                <p>This is the second paragraph with relevant text for reading.</p>
            </article>
            <aside class="sidebar">Sidebar content and widgets</aside>
            <script>console.log("analytics");</script>
            <footer>Copyright 2026</footer>
        </body>
        </html>
        """
        result = ReadabilityExtractor.extract(sample_html, url="https://example.com/article")
        
        self.assertEqual(result["title"], "Sample Article Title")
        self.assertIn("first paragraph", result["clean_text"])
        self.assertIn("second paragraph", result["clean_text"])
        self.assertNotIn("Banner Advertisement", result["clean_text"])
        self.assertNotIn("Home | About", result["clean_text"])
        self.assertNotIn("Sidebar content", result["clean_text"])
        self.assertNotIn("Copyright 2026", result["clean_text"])
        self.assertGreater(result["word_count"], 10)
        self.assertEqual(result["url"], "https://example.com/article")

    def test_extract_handles_empty_or_invalid_input(self):
        result_empty = ReadabilityExtractor.extract("", url="")
        self.assertEqual(result_empty["clean_text"], "")
        self.assertEqual(result_empty["word_count"], 0)

        result_none = ReadabilityExtractor.extract(None, url="")
        self.assertEqual(result_none["clean_text"], "")
        self.assertEqual(result_none["word_count"], 0)


if __name__ == "__main__":
    unittest.main()
