"""
Unit Test Suite for Feed Presets Library (Git Branch: feature/feed-presets-library)
"""

import unittest
from features.feature_feed_presets_library.implementation.feeds_presets import (
    get_preset_feeds,
    PRESET_FEEDS,
)


class TestFeedPresets(unittest.TestCase):
    def test_preset_feeds_non_empty(self):
        presets = get_preset_feeds()
        self.assertGreater(len(presets), 0)

    def test_preset_structure(self):
        for p in PRESET_FEEDS:
            self.assertIn("name", p)
            self.assertIn("url", p)
            self.assertIn("category", p)


if __name__ == "__main__":
    unittest.main()
