"""Contract-drift tests for gui/_23_feed_ping_endpoint_single_scrape/ping_feed_endpoint.py

CONTRACT SNAPSHOT
  module   : gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint
  function : ping_feed(window, fid: str) -> None
  imports  : gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
            , gui._35_scrape_run_background_orchestrator.run_scrape_background.run_scrape
  effects  : starts single-feed scrape via run_scrape
  errors   : Silently returns if feed not found or scrape already running
"""
# WHAT: Verifies the ping_feed contract survives refactor drift.
# OPTIONS: window with feeds list and scrape_thread; fid — feed ID
# DEFAULTS: Returns without action if thread running or feed not found
# OUTPUT/EFFECT: run_scrape(window, [target_feed]) called
# ERRORS/EDGE CASES: Thread running → no-op; unknown fid → no-op
# HOW TO TEST: ping_feed(window, "fid"); verify run_scrape called

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
from gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint import ping_feed


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(ping_feed, [("window", 1, inspect.Parameter.empty),
                                      ("fid", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_23_feed_ping_endpoint_single_scrape" / "ping_feed_endpoint.py")
        assert_source_imports(module_path, {
            "gui._10_log_append_timestamped_message.append_timestamped_log",
            "gui._35_scrape_run_background_orchestrator.run_scrape_background",
        })

    def test_callables(self):
        import gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint as mod
        assert_callables(mod, {"ping_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_runs_scrape_when_thread_not_running(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
            {"id": "b", "name": "Feed B", "url": "https://b.com/feed"},
        ]
        window.scrape_thread = MagicMock()
        window.scrape_thread.isRunning.return_value = False
        with patch("gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint.run_scrape") as mock_run, \
             patch("gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint.append_log_message"):
            ping_feed(window, "b")

        mock_run.assert_called_once_with(window, [window.feeds[1]])

    def test_no_op_when_thread_running(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
        ]
        window.scrape_thread = MagicMock()
        window.scrape_thread.isRunning.return_value = True
        with patch("gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint.run_scrape") as mock_run:
            ping_feed(window, "a")

        mock_run.assert_not_called()

    def test_unknown_fid_is_noop(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
        ]
        window.scrape_thread = MagicMock()
        window.scrape_thread.isRunning.return_value = False
        with patch("gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint.run_scrape") as mock_run:
            ping_feed(window, "nonexistent")

        mock_run.assert_not_called()
