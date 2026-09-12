"""Contract-drift tests for gui/_23_feed_ping_endpoint_single_scrape/ping_feed_endpoint.py

CONTRACT SNAPSHOT
  module   : gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint
  function : ping_feed(window, fid: str) -> None
  imports  : gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
            , gui._35_scrape_run_background_orchestrator.run_scrape_background.run_scrape
  effects  : starts single-feed scrape via run_scrape
  errors   : Silently returns if feed not found or scrape already running
"""
# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the recorded CONTRACT of
# gui/_23_feed_ping_endpoint_single_scrape/ping_feed_endpoint.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   If window.scrape_thread.isRunning() is True, return immediately (a scrape
#   is already in progress — do not start another).
#   Otherwise search window.feeds for the first feed whose "id" equals fid.
#   If found: call run_scrape(window, [target_feed]).
#   If NOT found: return quietly (silent no-op by contract).
#
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 — Structural: shape-of-the-code checks to catch refactor drift.
# Layer 2 — Behavioral Smoke: fake-window smoke tests that verify the happy
#                              path (scrape started for a known feed), the
#                              thread-running guard (no scrape when a thread
#                              is already active), and the no-op path (unknown
#                              fid, nothing happens).
#
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================
# Layer 1 — Structural:
#   test_signature       - exactly two params: "window" and "fid"
#                          (both positional-or-keyword, no default), returns
#                          None.
#   test_source_imports  - module-level imports include append_log_message
#                          and run_scrape.
#   test_callables       - module exposes ONLY the public symbol
#                          "ping_feed".
# Layer 2 — Behavioral Smoke:
#   test_runs_scrape_when_thread_not_running - known fid + thread idle ->
#                                              run_scrape called once with
#                                              window and [target_feed].
#   test_no_op_when_thread_running           - thread active -> run_scrape
#                                              NOT called (guard honoured).
#   test_unknown_fid_is_noop                          - unknown fid ->
#                                                       run_scrape NOT called.
# ===========================================================================
# WHAT: Verifies the ping_feed contract survives refactor drift.
# OPTIONS: window with feeds list and scrape_thread; fid — feed ID
# DEFAULTS: Returns without action if thread running or feed not found
# OUTPUT/EFFECT: run_scrape(window, [target_feed]) called
# ERRORS/EDGE CASES: Thread running -> no-op; unknown fid -> no-op
# HOW TO TEST: ping_feed(window, "fid"); verify run_scrape called

# sys = runtime controls; plants fake PyQt6 modules and extends import path.
import sys
# inspect = reads a function's declared parameters without running it.
import inspect
# Path = readable file-system paths.
from pathlib import Path
# MagicMock = fake call-recording object; patch = swap a name temporarily.
from unittest.mock import MagicMock, patch

# pytest = the test runner.
import pytest

# Ensure offscreen platform for headless Qt rendering
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

# PROJECT_ROOT: three folders up from here = the RSS project root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Put the root on Python's import search path (once).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Shared helpers from conftest.py: structural assertions + the fake WindowStub.
from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
from gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint import ping_feed


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the source module's public shape (signature, imports,
         callable set) has not drifted from the recorded contract.
    OPTIONS: None — these are purely structural invariants.
    DEFAULTS: N/A
    OUTPUT/EFFECT: No runtime effect; raises AssertionError on drift.
    ERRORS/EDGE CASES: None — these are static invariants.
    HOW TO TEST: Run this class in isolation; all three tests must pass.
    """

    def test_signature(self):
        """WHAT: Verify ping_feed accepts exactly two parameters.

        OPTIONS: None — contract is fixed at two parameters: 'window' and
                 'fid' (both positional-or-keyword, no defaults), returning
                 None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts the signature matches (window, fid) -> None.
        ERRORS/EDGE CASES: If the source gains or loses parameters the test
                           fails, flagging refactor drift.
        HOW TO TEST: assert_signature(ping_feed, [("window", 1, inspect.Parameter.empty),
                                                   ("fid", 1, inspect.Parameter.empty)], None)
        """
        assert_signature(ping_feed, [("window", 1, inspect.Parameter.empty),
                                      ("fid", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verify the source file imports required modules on disk.

        OPTIONS: None — the import set is a hard contract.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts AST-parsed source contains append_log_message
                       and run_scrape.
        ERRORS/EDGE CASES: Renaming or removing either import causes failure.
        HOW TO TEST: assert_source_imports(module_path, expected_import_set)
        """
        module_path = str(Path(__file__).resolve().parents[3]
                          / "gui" / "_23_feed_ping_endpoint_single_scrape" / "ping_feed_endpoint.py")
        assert_source_imports(module_path, {
            "gui._10_log_append_timestamped_message.append_timestamped_log",
            "gui._35_scrape_run_background_orchestrator.run_scrape_background",
        })

    def test_callables(self):
        """WHAT: Verify the module exposes exactly one public callable.

        OPTIONS: None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts dir(mod) contains only "ping_feed" among
                       user-defined callables.
        ERRORS/EDGE CASES: Extra or missing callables indicate drift.
        HOW TO TEST: assert_callables(mod, {"ping_feed"})
        """
        import gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint as mod
        assert_callables(mod, {"ping_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:
    """Layer 2 — Behavioral smoke tests against a fake window.

    WHAT: Verifies the observable behaviour of ping_feed: starting a scrape
         for a known feed when the thread is idle, respecting the thread-
         running guard, and the no-op path when the fid is unknown.
    OPTIONS: window with feeds list and scrape_thread; fid — feed ID.
    DEFAULTS: Returns without action if thread running or feed not found.
    OUTPUT/EFFECT: run_scrape(window, [target_feed]) called.
    ERRORS/EDGE CASES: Thread running -> no-op; unknown fid -> no-op.
    HOW TO TEST: ping_feed(window, "fid"); verify run_scrape called.
    """

    def test_runs_scrape_when_thread_not_running(self):
        """WHAT: Verify run_scrape is called for a known feed when idle.

        OPTIONS: window.feeds has two feeds ("a" and "b");
                 window.scrape_thread.isRunning() = False; fid = "b".
        DEFAULTS: The scrape thread is explicitly set to NOT running.
        OUTPUT/EFFECT: run_scrape called exactly once with (window,
                       [window.feeds[1]]).
        ERRORS/EDGE CASES: If the source calls run_scrape with wrong args or
                           skips it the assertion fails.
        HOW TO TEST: Patch run_scrape and append_log_message; call ping_feed;
                     assert mock_run.assert_called_once_with(window, [window.feeds[1]]).
        """
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
        """WHAT: Verify run_scrape is NOT called when a scrape is active.

        OPTIONS: window.feeds has one feed ("a");
                 window.scrape_thread.isRunning() = True; fid = "a".
        DEFAULTS: The scrape thread is explicitly set to RUNNING.
        OUTPUT/EFFECT: run_scrape NOT called (the guard fires first).
        ERRORS/EDGE CASES: If the source ignores the guard and starts a
                           second scrape the test fails.
        HOW TO TEST: Patch run_scrape; call ping_feed; assert
                     mock_run.assert_not_called().
        """
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
        """WHAT: Verify an unknown fid causes no scrape to start.

        OPTIONS: window.feeds has one feed ("a");
                 window.scrape_thread.isRunning() = False; fid = "nonexistent".
        DEFAULTS: The thread is explicitly set to NOT running (so the guard
                  does NOT block — only the missing fid should).
        OUTPUT/EFFECT: run_scrape NOT called (no matching feed found).
        ERRORS/EDGE CASES: If the source calls run_scrape with an empty list
                           or skips the fid lookup the test fails.
        HOW TO TEST: Patch run_scrape; call ping_feed; assert
                     mock_run.assert_not_called().
        """
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
        ]
        window.scrape_thread = MagicMock()
        window.scrape_thread.isRunning.return_value = False
        with patch("gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint.run_scrape") as mock_run:
            ping_feed(window, "nonexistent")

        mock_run.assert_not_called()
