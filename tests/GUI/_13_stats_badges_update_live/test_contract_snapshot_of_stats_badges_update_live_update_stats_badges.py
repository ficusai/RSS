"""Contract-drift tests for gui/_13_stats_badges_update_live/update_stats_badges.py

CONTRACT SNAPSHOT
  module   : gui._13_stats_badges_update_live.update_stats_badges
  function : update_stats_badges(window) -> None
  imports  : core.storage.get_stats
  effects  : sets window.lbl_articles_stat.setText / window.lbl_feeds_stat.setText
  errors   : exception → badges unchanged (silent)
"""
# WHAT: Verifies the update_stats_badges contract survives refactor drift.
# OPTIONS: window with lbl_articles_stat, lbl_feeds_stat, feeds list
# DEFAULTS: On exception, badges remain unchanged
# OUTPUT/EFFECT: Two QLabel setText calls with formatted badge strings
# ERRORS/EDGE CASES: get_stats() raises → pass; feeds missing 'enabled' key → True
# HOW TO TEST: call update_stats_badges(window); inspect setText calls

import sys
import inspect
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure offscreen platform for headless Qt rendering
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.GUI.conftest import assert_signature, assert_constants, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
from gui._13_stats_badges_update_live.update_stats_badges import update_stats_badges


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(update_stats_badges, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_13_stats_badges_update_live" / "update_stats_badges.py")
        assert_source_imports(module_path, {"core.storage"})

    def test_callables(self):
        import gui._13_stats_badges_update_live.update_stats_badges as mod
        assert_callables(mod, {"update_stats_badges"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_sets_article_and_feed_badges(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "enabled": True},
            {"id": "b", "enabled": False},
            {"id": "c", "enabled": True},
        ]
        with patch("gui._13_stats_badges_update_live.update_stats_badges.get_stats",
                   return_value={"total_articles": 150}):
            update_stats_badges(window)

        window.lbl_articles_stat.setText.assert_called_once_with("📰 150 Articles")
        window.lbl_feeds_stat.setText.assert_called_once_with("📡 2/3 Feeds Active")

    def test_exception_preserves_badges(self):
        window = WindowStub()
        window.lbl_articles_stat.setText.side_effect = Exception("boom")
        # Should not propagate
        update_stats_badges(window)
        # Badges should not have been set (exception inside try is caught)
        window.lbl_articles_stat.setText.side_effect = None
        window.lbl_feeds_stat.setText.side_effect = Exception("boom")
        update_stats_badges(window)

    def test_missing_enabled_key_defaults_true(self):
        window = WindowStub()
        window.feeds = [{"id": "x"}]
        with patch("gui._13_stats_badges_update_live.update_stats_badges.get_stats",
                   return_value={"total_articles": 0}):
            update_stats_badges(window)
        window.lbl_feeds_stat.setText.assert_called_once_with("📡 1/1 Feeds Active")
