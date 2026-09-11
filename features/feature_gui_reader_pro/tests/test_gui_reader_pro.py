"""
Unit Test Suite for GUI Reader Pro Components (Git Branch: feature/gui-reader-pro)
"""

import unittest
from features.feature_gui_reader_pro.implementation.reader_pro_components import (
    get_category_color,
    calculate_reading_time_minutes,
)


class TestGuiReaderPro(unittest.TestCase):
    def test_get_category_color(self):
        self.assertEqual(get_category_color("Technology"), "#58a6ff")
        self.assertEqual(get_category_color("Finance"), "#3fb950")
        self.assertEqual(get_category_color("World News"), "#d29922")

    def test_calculate_reading_time(self):
        short_text = "Word " * 100
        self.assertEqual(calculate_reading_time_minutes(short_text), 1)

        long_text = "Word " * 600
        self.assertEqual(calculate_reading_time_minutes(long_text), 3)


if __name__ == "__main__":
    unittest.main()
