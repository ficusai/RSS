"""Contract-drift tests for gui/_20_feed_delete_subscription/delete_feed_subscription.py

CONTRACT SNAPSHOT
  module   : gui._20_feed_delete_subscription.delete_feed_subscription
  function : delete_feed(window, fid: str) -> None
  imports  : gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
            , gui._15_feed_config_save_to_disk.save_feeds.save_feeds
            , gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_window
  effects  : removes matching feed; calls save_feeds + refresh_window
  errors   : None — silently skips if fid not found
"""
# WHAT: Verifies the delete_feed contract survives refactor drift.
# OPTIONS: window with feeds list; fid — feed ID string
# DEFAULTS: N/A
# OUTPUT/EFFECT: Matching feed removed; save_feeds + refresh_window called
# ERRORS/EDGE CASES: Unknown fid → no-op, no save
# HOW TO TEST: delete_feed(window, "some-fid"); assert feed removed

import sys
import inspect
from pathlib import Path
from unittest.mock import MagicMock, patch

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
from gui._20_feed_delete_subscription.delete_feed_subscription import delete_feed


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(delete_feed, [("window", 1, inspect.Parameter.empty),
                                       ("fid", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_20_feed_delete_subscription" / "delete_feed_subscription.py")
        assert_source_imports(module_path, {
            "gui._10_log_append_timestamped_message.append_timestamped_log",
            "gui._15_feed_config_save_to_disk.save_feeds",
        })

    def test_callables(self):
        import gui._20_feed_delete_subscription.delete_feed_subscription as mod
        assert_callables(mod, {"delete_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_removes_matching_feed_and_calls_save_refresh(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
            {"id": "b", "name": "Feed B", "url": "https://b.com/feed"},
            {"id": "c", "name": "Feed C", "url": "https://c.com/feed"},
        ]
        with patch("gui._20_feed_delete_subscription.delete_feed_subscription.save_feeds") as mock_save, \
             patch("gui._20_feed_delete_subscription.delete_feed_subscription.refresh_window") as mock_refresh, \
             patch("gui._20_feed_delete_subscription.delete_feed_subscription.append_log_message"):
            delete_feed(window, "b")

        assert len(window.feeds) == 2
        assert all(f["id"] != "b" for f in window.feeds)
        mock_save.assert_called_once_with(window)
        mock_refresh.assert_called_once_with(window)

    def test_unknown_fid_is_noop(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
        ]
        original_len = len(window.feeds)
        with patch("gui._20_feed_delete_subscription.delete_feed_subscription.save_feeds") as mock_save, \
             patch("gui._20_feed_delete_subscription.delete_feed_subscription.refresh_window") as mock_refresh:
            delete_feed(window, "nonexistent")

        assert len(window.feeds) == original_len
        mock_save.assert_not_called()
        mock_refresh.assert_not_called()
