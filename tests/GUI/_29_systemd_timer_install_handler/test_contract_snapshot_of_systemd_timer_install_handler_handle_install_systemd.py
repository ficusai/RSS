"""Contract snapshot: gui/_29_systemd_timer_install_handler/handle_install_systemd.py v1.0.0

Structural contract:
  - Function name: handle_install_systemd
  - Signature: (window) -> None
  - Source imports: PyQt6.QtWidgets.QMessageBox,
                   features.feature_systemd_scheduler.implementation.scheduler.install_systemd_timer,
                   gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message,
                   gui._28_systemd_status_refresh_daemon.refresh_systemd_status.refresh_systemd_status
  - Side effects: install_systemd_timer(), QMessageBox.information OR QMessageBox.critical,
                  append_log_message, refresh_systemd_status
"""
# ==============================================================================
# WHAT: Verifies the handle_install_systemd GUI contract — installation call,
#       result dialog, log message, and status badge refresh on success/failure.
#
# OPTIONS:
#   window: MainWindow stub.
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: Success → info dialog + log + refresh; Failure → critical dialog + log + refresh.
#
# ERRORS/EDGE CASES: install_systemd_timer returns False on non-systemd or permission denied.
#
# HOW TO TEST: handle_install_systemd(window)
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



def _make_window():
    """Build a minimal WindowStub."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert handle_install_systemd(window) -> None."""
        import inspect
        from gui._29_systemd_timer_install_handler.handle_install_systemd import (
            handle_install_systemd,
        )
        sig = inspect.signature(handle_install_systemd)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import QMessageBox, install_systemd_timer, append_log_message, refresh_systemd_status."""
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._29_systemd_timer_install_handler.handle_install_systemd"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {
                "PyQt6.QtWidgets",
                "features.feature_systemd_scheduler.implementation.scheduler",
                "gui._10_log_append_timestamped_message.append_timestamped_log",
                "gui._28_systemd_status_refresh_daemon.refresh_systemd_status",
            },
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real function."""

    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.refresh_systemd_status")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.append_log_message")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.QMessageBox.information")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.install_systemd_timer")
    def test_success_path(self, mock_install, mock_info, mock_log, mock_refresh, qapp):
        """install_systemd_timer returns True → info dialog + log + refresh called."""
        from gui._29_systemd_timer_install_handler.handle_install_systemd import (
            handle_install_systemd,
        )
        mock_install.return_value = True
        w = _make_window()
        handle_install_systemd(w)
        mock_install.assert_called_once()
        mock_info.assert_called_once()
        mock_log.assert_called_once_with(w, "Successfully installed and launched systemd user timer (rss-scraper.timer).")
        mock_refresh.assert_called_once_with(w)

    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.refresh_systemd_status")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.append_log_message")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.QMessageBox.critical")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.install_systemd_timer")
    def test_failure_path(self, mock_install, mock_critical, mock_log, mock_refresh, qapp):
        """install_systemd_timer returns False → critical dialog + log + refresh called."""
        from gui._29_systemd_timer_install_handler.handle_install_systemd import (
            handle_install_systemd,
        )
        mock_install.return_value = False
        w = _make_window()
        handle_install_systemd(w)
        mock_install.assert_called_once()
        mock_critical.assert_called_once()
        mock_log.assert_called_once_with(w, "Failed to install systemd user timer.")
        mock_refresh.assert_called_once_with(w)
