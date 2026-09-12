"""Contract-drift tests for gui/_19_feed_add_single_subscription/add_feed_subscription.py

CONTRACT SNAPSHOT
  module   : gui._19_feed_add_single_subscription.add_feed_subscription
  function : add_feed(window) -> None
  imports  : PyQt6.QtWidgets.QMessageBox
            , gui._09_feed_identifier_generate_from_name.generate_feed_id
            , gui._10_log_append_timestamped_message.append_timestamped_log
            , gui._15_feed_config_save_to_disk.save_feeds
            , gui._16_refresh_all_views_pipeline.refresh_all_views
  effects  : validates; appends feed dict; calls save_feeds + refresh_window
  errors   : missing name/url → QMessageBox.warning; duplicate URL → logged
"""
# WHAT: Verifies the add_feed contract survives refactor drift.
# OPTIONS: window with in_name, in_url, in_cat, cb_freq, feeds list
# DEFAULTS: category="General"; interval from cb_freq index via [1,3,6,12,24]
# OUTPUT/EFFECT: feed appended with exact keys; save_feeds + refresh_window called
# ERRORS/EDGE CASES: Missing fields → warning; duplicate URL → log; no https prefix
# HOW TO TEST: fill form fields; call add_feed(window); check feeds list

import sys
import inspect
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

# Ensure offscreen platform for headless Qt rendering
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
from gui._19_feed_add_single_subscription.add_feed_subscription import add_feed


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(add_feed, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_19_feed_add_single_subscription" / "add_feed_subscription.py")
        assert_source_imports(module_path, {
            "PyQt6.QtWidgets",
            "gui._09_feed_identifier_generate_from_name.generate_feed_id",
            "gui._10_log_append_timestamped_message.append_timestamped_log",
            "gui._15_feed_config_save_to_disk.save_feeds",
            "gui._16_refresh_all_views_pipeline.refresh_all_views",
        })

    def test_callables(self):
        import gui._19_feed_add_single_subscription.add_feed_subscription as mod
        assert_callables(mod, {"add_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_missing_name_or_url_shows_warning(self):
        window = WindowStub()
        window.in_name.text.return_value = ""
        window.in_url.text.return_value = "https://example.com/feed"
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.QMessageBox.warning") as mock_warn:
            add_feed(window)
            mock_warn.assert_called_once()

    def test_valid_feed_appended_with_exact_keys(self):
        window = WindowStub()
        window.in_name.text.return_value = "TechCrunch"
        window.in_url.text.return_value = "https://techcrunch.com/feed"
        window.in_cat.text.return_value = "Technology"
        window.cb_freq.currentIndex.return_value = 2
        window.feeds = []
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.generate_feed_id",
                   return_value="techcrunch") as mock_gid, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds") as mock_save, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window") as mock_refresh, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message"):
            add_feed(window)

        assert len(window.feeds) == 1
        feed = window.feeds[0]
        assert feed == {
            "id": "techcrunch",
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed",
            "category": "Technology",
            "fetch_interval_hours": 6,
            "enabled": True,
        }
        mock_save.assert_called_once_with(window)
        mock_refresh.assert_called_once_with(window)
        window.in_name.clear.assert_called_once()
        window.in_url.clear.assert_called_once()

    def test_url_gets_https_prefix_when_scheme_less(self):
        window = WindowStub()
        window.in_name.text.return_value = "Example"
        window.in_url.text.return_value = "example.com/feed"
        window.in_cat.text.return_value = ""
        window.cb_freq.currentIndex.return_value = 3
        window.feeds = []
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.generate_feed_id",
                   return_value="example"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message"):
            add_feed(window)

        assert window.feeds[0]["url"] == "https://example.com/feed"

    def test_duplicate_url_not_appended(self):
        window = WindowStub()
        window.in_name.text.return_value = "Duplicate"
        window.in_url.text.return_value = "https://duplicate.com/feed"
        window.in_cat.text.return_value = "Tech"
        window.cb_freq.currentIndex.return_value = 0
        window.feeds = [{"id": "x", "name": "Existing", "url": "https://duplicate.com/feed",
                        "enabled": True}]
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds") as mock_save, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window") as mock_refresh, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message") as mock_log:
            add_feed(window)

        assert len(window.feeds) == 1
        mock_save.assert_not_called()
        mock_refresh.assert_not_called()
        mock_log.assert_called_once()

    def test_duplicate_url_trailing_slash_normalized(self):
        window = WindowStub()
        window.in_name.text.return_value = "Dup"
        window.in_url.text.return_value = "https://dup.com/feed/"
        window.in_cat.text.return_value = "Tech"
        window.cb_freq.currentIndex.return_value = 0
        window.feeds = [{"id": "x", "name": "X", "url": "https://dup.com/feed",
                        "enabled": True}]
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message") as mock_log:
            add_feed(window)
        assert len(window.feeds) == 1
        mock_log.assert_called_once()

    def test_interval_index_maps_correctly(self):
        window = WindowStub()
        window.in_name.text.return_value = "F"
        window.in_url.text.return_value = "https://f.com/feed"
        window.in_cat.text.return_value = "G"
        window.cb_freq.currentIndex.return_value = 4
        window.feeds = []
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.generate_feed_id",
                   return_value="f"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message"):
            add_feed(window)

        assert window.feeds[0]["fetch_interval_hours"] == 24
