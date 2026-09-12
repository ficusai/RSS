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
    """Build a minimal WindowStub with feeds and optional running scrape_thread."""
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
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert start_scrape(window) -> None."""
        import inspect
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        sig = inspect.signature(start_scrape)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import QMessageBox and run_scrape."""
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
    """Behavioral smoke tests against the real function."""

    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.run_scrape")
    def test_no_op_when_scrape_running(self, mock_run, qapp):
        """Already running scrape → returns without calling run_scrape."""
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        w = _make_window(feeds=[{"name": "A", "enabled": True}], thread_running=True)
        start_scrape(w)
        mock_run.assert_not_called()

    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.run_scrape")
    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.QMessageBox.information")
    def test_shows_dialog_when_no_enabled_feeds(self, mock_info, mock_run, qapp):
        """No enabled feeds → info dialog shown, run_scrape not called."""
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        w = _make_window(feeds=[])
        start_scrape(w)
        mock_info.assert_called_once_with(
            w, "No Active Subscriptions", "Please enable at least one feed to sync."
        )
        mock_run.assert_not_called()

    @patch("gui._34_scrape_start_enabled_feeds.start_scrape.run_scrape")
    def test_calls_run_scrape_with_enabled_feeds(self, mock_run, qapp):
        """Enabled feeds present → run_scrape called with full feeds list."""
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
