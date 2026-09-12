"""Contract-drift tests for gui/_22_feed_update_interval_frequency/set_feed_frequency.py

CONTRACT SNAPSHOT
  module   : gui._22_feed_update_interval_frequency.set_feed_frequency
  function : set_feed_frequency(window, fid: str, hours) -> None
  imports  : gui._15_feed_config_save_to_disk.save_feeds.save_feeds
  effects  : sets feed["fetch_interval_hours"] = hours; calls save_feeds
  errors   : None — silently skips if fid not found
"""
# WHAT: Verifies the set_feed_frequency contract survives refactor drift.
# OPTIONS: window with feeds list; fid — feed ID; hours — int
# DEFAULTS: N/A
# OUTPUT/EFFECT: Interval updated in window.feeds; save_feeds called
# ERRORS/EDGE CASES: Unknown fid → no-op
# HOW TO TEST: set_feed_frequency(window, "fid", 6); check feed.fetch_interval_hours

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
from gui._22_feed_update_interval_frequency.set_feed_frequency import set_feed_frequency


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(set_feed_frequency, [("window", 1, inspect.Parameter.empty),
                                               ("fid", 1, inspect.Parameter.empty),
                                               ("hours", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_22_feed_update_interval_frequency" / "set_feed_frequency.py")
        assert_source_imports(module_path, {"gui._15_feed_config_save_to_disk.save_feeds"})

    def test_callables(self):
        import gui._22_feed_update_interval_frequency.set_feed_frequency as mod
        assert_callables(mod, {"set_feed_frequency"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_sets_interval_and_calls_save(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "fetch_interval_hours": 12},
            {"id": "b", "name": "B", "url": "https://b.com/feed", "fetch_interval_hours": 6},
        ]
        with patch("gui._22_feed_update_interval_frequency.set_feed_frequency.save_feeds") as mock_save:
            set_feed_frequency(window, "b", 24)

        assert window.feeds[1]["fetch_interval_hours"] == 24
        mock_save.assert_called_once_with(window)

    def test_unknown_fid_is_noop(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "fetch_interval_hours": 12},
        ]
        with patch("gui._22_feed_update_interval_frequency.set_feed_frequency.save_feeds") as mock_save:
            set_feed_frequency(window, "nonexistent", 1)

        assert window.feeds[0]["fetch_interval_hours"] == 12
        mock_save.assert_not_called()
