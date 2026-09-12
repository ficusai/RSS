"""Contract-drift tests for gui/_21_feed_toggle_enabled_state/toggle_feed_state.py

CONTRACT SNAPSHOT
  module   : gui._21_feed_toggle_enabled_state.toggle_feed_state
  function : toggle_feed(window, fid: str, on: bool) -> None
  imports  : gui._15_feed_config_save_to_disk.save_feeds.save_feeds
            , gui._13_stats_badges_update_live.update_stats_badges.update_stats_badges
  effects  : sets feed["enabled"] = on; calls save_feeds + update_stats_badges
  errors   : None — silently skips if fid not found
"""
# WHAT: Verifies the toggle_feed contract survives refactor drift.
# OPTIONS: window with feeds list; fid — feed ID; on — bool
# DEFAULTS: N/A
# OUTPUT/EFFECT: Feed enabled state changed; save_feeds + update_stats_badges called
# ERRORS/EDGE CASES: Unknown fid → no-op
# HOW TO TEST: toggle_feed(window, "fid", False); check feed.enabled and calls

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
from gui._21_feed_toggle_enabled_state.toggle_feed_state import toggle_feed


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(toggle_feed, [("window", 1, inspect.Parameter.empty),
                                       ("fid", 1, inspect.Parameter.empty),
                                       ("on", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_21_feed_toggle_enabled_state" / "toggle_feed_state.py")
        assert_source_imports(module_path, {
            "gui._15_feed_config_save_to_disk.save_feeds",
            "gui._13_stats_badges_update_live.update_stats_badges",
        })

    def test_callables(self):
        import gui._21_feed_toggle_enabled_state.toggle_feed_state as mod
        assert_callables(mod, {"toggle_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_sets_enabled_and_calls_save_and_stats(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "enabled": True},
            {"id": "b", "name": "B", "url": "https://b.com/feed", "enabled": True},
        ]
        with patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.save_feeds") as mock_save, \
             patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.update_stats_badges") as mock_stats:
            toggle_feed(window, "b", False)

        assert window.feeds[1]["enabled"] is False
        mock_save.assert_called_once_with(window)
        mock_stats.assert_called_once_with(window)

    def test_unknown_fid_is_noop(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "enabled": True},
        ]
        with patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.save_feeds") as mock_save, \
             patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.update_stats_badges") as mock_stats:
            toggle_feed(window, "nonexistent", False)

        assert window.feeds[0]["enabled"] is True
        mock_save.assert_not_called()
        mock_stats.assert_not_called()
