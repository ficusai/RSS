"""Contract snapshot: gui/_35_scrape_run_background_orchestrator/run_scrape_background.py v1.0.0

Structural contract:
  - Function name: run_scrape
  - Signature: (window, feeds) -> None
  - Source imports: gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message,
                   gui._36_scrape_finished_signal_handler.on_scrape_done.on_scrape_done,
                   gui._02_background_scrape_thread_worker.scrape_thread_worker.ScrapeThread
  - Side effects: btn_sync.setEnabled(False), setText("⏳ Syncing..."), progress.setVisible,
                  progress.setRange(0,0), ScrapeThread(feeds), .start(), signal.connect
"""
# ==============================================================================
# WHAT: Verifies the run_scrape GUI contract — creates ScrapeThread, wires
#       signals, disables button, shows progress bar, and starts the thread.
#
# LAYER BREAKDOWN:
#   Layer 1 (Structural):  test_signature, test_source_imports
#   Layer 2 (Behavioral): test_creates_thread_and_wires_signals
#
# LAYER WHAT EACH TEST CHECKS:
#   test_signature          — function params (window, feeds), kind, default, return annotation
#   test_source_imports     — required modules imported via AST
#   test_creates_thread_and_wires_signals — button disabled, progress shown, thread started, signals wired
#
# OPTIONS:
#   window: MainWindow stub with btn_sync, progress, and other required attrs.
#   feeds: list of feed dicts to scrape.
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: Background thread started; UI reflects running state.
#
# ERRORS/EDGE CASES: None expected.
#
# HOW TO TEST: run_scrape(window, [...])
# ==============================================================================
import importlib.util
import pytest
from unittest.mock import MagicMock, patch, call as mock_call

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



def _make_window():
    r"""Build a minimal WindowStub for run_scrape.

    WHAT: Constructs a stub window whose btn_sync, progress, and scrape_thread
          attributes are pre-mocked so run_scrape can manipulate them safely.

    OPTIONS:
      None — all attributes are auto-created with sensible defaults.

    DEFAULTS: btn_sync and progress are MagicMock instances; scrape_thread is None.

    OUTPUT/EFFECT: Returns a WindowStub ready for run_scrape tests.

    ERRORS/EDGE CASES: None — stub is intentionally minimal.

    HOW TO TEST: Inspect w.btn_sync, w.progress, w.scrape_thread after creation.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.btn_sync = MagicMock()
    w.progress = MagicMock()
    w.scrape_thread = None
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    r"""Structural / signature / import contract checks.

    WHAT: Verifies that the source module's public API matches the declared
          contract — function signature with two parameters, return type, and
          required imports — without executing any thread-creation logic.

    OPTIONS:
      None — purely static, no Qt event loop needed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Assertions pass if signature, imports, and callable contract hold.

    ERRORS/EDGE CASES: Any mismatch raises AssertionError indicating contract drift.

    HOW TO TEST: Run pytest on this class alone; all tests are fast and deterministic.
    """

    def test_signature(self):
        r"""WHAT: Confirm run_scrape accepts exactly two positional-or-keyword
                  parameters named 'window' and 'feeds', and annotates return as None.

        OPTIONS:
          None — inspects the real function object directly.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: params list and return_annotation asserted.

        ERRORS/EDGE CASES: Extra/missing params, wrong kind, or missing return annotation → fail.

        HOW TO TEST: Import the function and call inspect.signature on it.
        """
        import inspect
        from gui._35_scrape_run_background_orchestrator.run_scrape_background import run_scrape
        sig = inspect.signature(run_scrape)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [
            ("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
            ("feeds", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ]
        assert sig.return_annotation is None

    def test_source_imports(self):
        r"""WHAT: Ensure the source module imports append_log_message, on_scrape_done,
                  and ScrapeThread, confirming all three dependency contracts are
                  declared in the source AST.

        OPTIONS:
          None — uses assert_source_imports helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Assertion passes if all three module paths appear in source AST.

        ERRORS/EDGE CASES: Missing import → assert_source_imports raises AssertionError.

        HOW TO TEST: Run this test; it reads the .py file and walks the AST.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._35_scrape_run_background_orchestrator.run_scrape_background"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {
                "gui._10_log_append_timestamped_message.append_timestamped_log",
                "gui._36_scrape_finished_signal_handler.on_scrape_done",
                "gui._02_background_scrape_thread_worker.scrape_thread_worker",
            },
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    r"""Behavioral smoke tests against the real function.

    WHAT: Executes run_scrape with a mocked ScrapeThread and asserts that the
          function correctly disables the sync button, shows the progress bar,
          constructs and starts the thread exactly once, and wires both signals.

    OPTIONS:
      qapp fixture: provides a QApplication instance for PyQt6 widget tests.
      MockScrapeThread patch: controls ScrapeThread construction and returns a mock thread.
      _make_window(): provides stub with btn_sync, progress, scrape_thread = None.

    DEFAULTS: Uses _make_window() with one synthetic feed dict.

    OUTPUT/EFFECT: Button state changes, progress bar visible, thread started, signals connected.

    ERRORS/EDGE CASES: None expected — this is the primary orchestration scenario.

    HOW TO TEST: Run pytest on this class; all tests require the qapp fixture.
    """

    @patch("gui._35_scrape_run_background_orchestrator.run_scrape_background.ScrapeThread")
    def test_creates_thread_and_wires_signals(self, MockScrapeThread, qapp):
        r"""WHAT: run_scrape must disable the sync button, update its text to
                  indicate running state, show the progress bar, construct exactly
                  one ScrapeThread, start it, and connect both signals once each.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          MockScrapeThread: patched constructor returning a mock thread with log_signal
                            and finished_signal attributes.
          _make_window(): provides stub with btn_sync, progress, scrape_thread = None.
          feeds: single-element list with a synthetic feed dict.

        DEFAULTS: Button text becomes "⏳ Syncing..."; progress range set to (0, 0) (indeterminate).

        OUTPUT/EFFECT: All UI state changes and thread lifecycle calls verified.

        ERRORS/EDGE CASES: None — this is the primary success scenario.

        HOW TO TEST: Patch ScrapeThread, create window, call run_scrape(w, feeds), assert calls.
        """
        from gui._35_scrape_run_background_orchestrator.run_scrape_background import run_scrape

        mock_thread = MagicMock()
        mock_thread.log_signal = MagicMock()
        mock_thread.finished_signal = MagicMock()
        MockScrapeThread.return_value = mock_thread

        w = _make_window()
        feeds = [{"name": "A", "url": "https://a.com/feed"}]
        run_scrape(w, feeds)

        # Button state
        w.btn_sync.setEnabled.assert_called_once_with(False)
        w.btn_sync.setText.assert_called_once_with("⏳ Syncing...")

        # Progress bar
        w.progress.setVisible.assert_called_once_with(True)
        w.progress.setRange.assert_called_once_with(0, 0)

        # Thread construction and start
        MockScrapeThread.assert_called_once_with(feeds)
        mock_thread.start.assert_called_once_with()

        # Signal wiring (connect called once per signal)
        mock_thread.log_signal.connect.assert_called_once()
        mock_thread.finished_signal.connect.assert_called_once()
