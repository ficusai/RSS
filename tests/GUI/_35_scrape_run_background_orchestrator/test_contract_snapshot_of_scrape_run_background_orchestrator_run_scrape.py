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
    """Build a minimal WindowStub for run_scrape."""
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
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert run_scrape(window, feeds) -> None."""
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
        """Source must import append_log_message, on_scrape_done, ScrapeThread."""
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
    """Behavioral smoke tests against the real function."""

    @patch("gui._35_scrape_run_background_orchestrator.run_scrape_background.ScrapeThread")
    def test_creates_thread_and_wires_signals(self, MockScrapeThread, qapp):
        """Btn disabled, progress shown, thread constructed once, started, signals wired."""
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
