"""Contract snapshot: gui/_34_scrape_start_enabled_feeds/start_scrape.py v1.0.0

Structural contract:
  - Function name: start_scrape
  - Signature: (window) -> None
  - Source imports: PyQt6.QtWidgets.QMessageBox,
                   gui._35_scrape_run_background_orchestrator.run_scrape_background.run_scrape
  - Side effects: run_scrape(window, feeds), QMessageBox.information
"""
# ==============================================================================
# WHAT: Verifies the start_scrape GUI contract — validates running state and
#       enabled feeds before launching background scrape.
#
# LAYER BREAKDOWN:
#   Layer 1 (Structural):  test_signature, test_source_imports
#   Layer 2 (Behavioral): test_no_op_when_scrape_running,
#                         test_shows_dialog_when_no_enabled_feeds,
#                         test_calls_run_scrape_with_enabled_feeds
#
# LAYER WHAT EACH TEST CHECKS:
#   test_signature                     — function param name, kind, default, return annotation
#   test_source_imports                — required modules imported via AST
#   test_no_op_when_scrape_running     — already running → run_scrape not called
#   test_shows_dialog_when_no_enabled_feeds — empty feeds → info dialog, no run_scrape
#   test_calls_run_scrape_with_enabled_feeds  — feeds present → run_scrape called with list
#
# OPTIONS:
#   window: MainWindow stub with scrape_thread, feeds list.
#
# DEFAULTS: No-op if scrape already running or no enabled feeds.
#
# OUTPUT/EFFECT: Background scrape launched; button state updated.
#
# ERRORS/EDGE CASES: Shows QMessageBox if no enabled feeds.
#
# HOW TO TEST: start_scrape(window)
# ==============================================================================
import importlib.util
import pytest
from unittest.mock import MagicMock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


# offscreen platform required for all PyQt6 widget testing
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform


@pytest.fixture(scope="module")
def qapp():
    """Create a single QApplication instance for the module."""
    app = QApplication([])
    yield app



def _make_window(feeds=None, thread_running=False):
    r"""Build a minimal WindowStub with feeds and optional running scrape_thread.

    WHAT: Constructs a stub window whose feeds list and scrape_thread running
          state can be controlled for start_scrape behavioral tests.

    OPTIONS:
      feeds: list of feed dicts; defaults to [] if None.
      thread_running: if True, scrape_thread.isRunning() returns True.

    DEFAULTS: feeds = [], scrape_thread = None (not running).

    OUTPUT/EFFECT: Returns a WindowStub with w.feeds and w.scrape_thread set.

    ERRORS/EDGE CASES: None — stub is intentionally minimal.

    HOW TO TEST: Inspect w.feeds and w.scrape_thread.isRunning() mock.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.feeds = feeds if feeds is not None else []
    if thread_running:
        thread = MagicMock()
        thread.isRunning = MagicMock(return_value=True)
        w.scrape_thread = thread
    else:
        w.scrape_thread = None
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    r"""Structural / signature / import contract checks.

    WHAT: Verifies that the source module's public API matches the declared
          contract — function signature, return type, and required imports —
          without executing any scraping logic.

    OPTIONS:
      None — purely static, no Qt event loop needed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Assertions pass if signature, imports, and callable contract hold.

    ERRORS/EDGE CASES: Any mismatch raises AssertionError indicating contract drift.

    HOW TO TEST: Run pytest on this class alone; all tests are fast and deterministic.
    """

    def test_signature(self):
        r"""WHAT: Confirm start_scrape accepts exactly one positional-or-keyword
                  parameter named 'window' and annotates return as None.

        OPTIONS:
          None — inspects the real function object directly.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: params list and return_annotation asserted.

        ERRORS/EDGE CASES: Extra params, wrong kind, or missing return annotation → fail.

        HOW TO TEST: Import the function and call inspect.signature on it.
        """
        import inspect
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        sig = inspect.signature(start_scrape)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        r"""WHAT: Ensure the source module imports QMessageBox and run_scrape,
                  confirming both the dialog and background-scrape dependencies
                  are declared in the source AST.

        OPTIONS:
          None — uses assert_source_imports helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Assertion passes if both module paths appear in source AST.

        ERRORS/EDGE CASES: Missing import → assert_source_imports raises AssertionError.

        HOW TO TEST: Run this test; it reads the .py file and walks the AST.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._34_scrape_start_enabled_feeds.start_scrape"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"PyQt6.QtWidgets", "gui._35_scrape_run_background_orchestrator.run_scrape_background"},
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    r"""Behavioral smoke tests against the real function.

    WHAT: Executes start_scrape with controlled WindowStub states and asserts
          the correct guard behavior: no-op when running, dialog when empty,
          and launch when feeds are present.

    OPTIONS:
      qapp fixture: provides a QApplication instance for PyQt6 widget tests.
      mock_run patch: intercepts run_scrape to verify it is called correctly.
      mock_info patch: intercepts QMessageBox.information to verify dialog text.
      _make_window(): controls feeds list and scrape_thread running state.

    DEFAULTS: Uses _make_window() with default empty feeds and non-running thread.

    OUTPUT/EFFECT: run_scrape launched or skipped; dialog shown or skipped.

    ERRORS/EDGE CASES: Each sub-test covers a different pre-condition branch.

    HOW TO TEST: Run pytest on this class; all tests require the qapp fixture.
    """

    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.run_scrape")
    def test_no_op_when_scrape_running(self, mock_run, qapp):
        r"""WHAT: When scrape_thread.isRunning() is True, start_scrape must
                  return immediately without calling run_scrape.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_run: intercepted run_scrape call.
          _make_window(thread_running=True): simulates an already-running scrape.
          feeds=[{"name": "A", "enabled": True}]: valid feeds present.

        DEFAULTS: scrape_thread.isRunning() returns True.

        OUTPUT/EFFECT: mock_run never called; function exits early.

        ERRORS/EDGE CASES: None — double-start prevention is the expected behavior.

        HOW TO TEST: Create window with thread_running=True, call start_scrape, assert_not_called.
        """
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        w = _make_window(feeds=[{"name": "A", "enabled": True}], thread_running=True)
        start_scrape(w)
        mock_run.assert_not_called()

    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.run_scrape")
    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.QMessageBox.information")
    def test_shows_dialog_when_no_enabled_feeds(self, mock_info, mock_run, qapp):
        r"""WHAT: When no feeds are enabled, start_scrape must show an information
                  dialog explaining the issue and skip launching the background scrape.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_info: intercepted QMessageBox.information call.
          mock_run: intercepted run_scrape call.
          _make_window(feeds=[]): empty feeds list.

        DEFAULTS: Dialog title "No Active Subscriptions", message "Please enable at least one feed to sync."

        OUTPUT/EFFECT: Info dialog shown; run_scrape not called.

        ERRORS/EDGE CASES: None — empty feeds is a valid user-facing error condition.

        HOW TO TEST: Create window with empty feeds, call start_scrape, assert dialog args.
        """
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        w = _make_window(feeds=[])
        start_scrape(w)
        mock_info.assert_called_once_with(
            w, "No Active Subscriptions", "Please enable at least one feed to sync."
        )
        mock_run.assert_not_called()

    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.run_scrape")
    def test_calls_run_scrape_with_enabled_feeds(self, mock_run, qapp):
        r"""WHAT: When enabled feeds are present and the scraper is not running,
                  start_scrape must pass the full feeds list to run_scrape.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_run: intercepted run_scrape call.
          _make_window(feeds=...): mix of enabled and disabled feeds.

        DEFAULTS: Full feeds list (including disabled) is passed to run_scrape.

        OUTPUT/EFFECT: mock_run called once with (w, feeds).

        ERRORS/EDGE CASES: None — this is the primary success scenario.

        HOW TO TEST: Create window with mixed feeds, call start_scrape, assert call args.
        """
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        feeds = [
            {"name": "A", "enabled": True},
            {"name": "B", "enabled": False},
            {"name": "C", "enabled": True},
        ]
        w = _make_window(feeds=feeds)
        start_scrape(w)
        # run_scrape receives the full window.feeds list (includes disabled)
        mock_run.assert_called_once_with(w, feeds)
