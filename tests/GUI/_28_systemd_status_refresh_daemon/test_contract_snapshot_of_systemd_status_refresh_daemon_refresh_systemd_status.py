"""Contract snapshot: gui/_28_systemd_status_refresh_daemon/refresh_systemd_status.py v1.0.0

Structural contract:
  - Function name: refresh_systemd_status
  - Signature: (window) -> None
  - Source imports: features.feature_systemd_scheduler.implementation.scheduler.get_timer_status,
                   gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
  - Side effects: lbl_sys_service / lbl_sys_timer / lbl_sys_enabled setText + setStyleSheet
"""
# ==============================================================================
# WHAT: Verifies the refresh_systemd_status GUI contract — badge text and colors
#       update based on get_timer_status() return value.
#
# OPTIONS:
#   window: MainWindow stub with three status label widgets.
#
# DEFAULTS: On exception, logs error and leaves badges unchanged.
#
# OUTPUT/EFFECT: Three status badges updated with text and color styles.
#
# ERRORS/EDGE CASES: get_timer_status may raise → caught, logged, badges unchanged.
#
# HOW TO TEST: refresh_systemd_status(window)
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



_GREEN = "background: #0d1117; border: 1px solid #238636; border-radius: 6px; padding: 8px 14px; color: #3fb950; font-weight: 600;"
_RED = "background: #0d1117; border: 1px solid #da3633; border-radius: 6px; padding: 8px 14px; color: #f85149; font-weight: 600;"
_GRAY = "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 14px; color: #8b949e; font-weight: 600;"


def _make_window():
    """Build a minimal WindowStub with status labels."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert refresh_systemd_status(window) -> None."""
        import inspect
        from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import (
            refresh_systemd_status,
        )
        sig = inspect.signature(refresh_systemd_status)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import get_timer_status and append_log_message."""
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._28_systemd_status_refresh_daemon.refresh_systemd_status"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"features.feature_systemd_scheduler.implementation.scheduler",
             "gui._10_log_append_timestamped_message.append_timestamped_log"},
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real function."""

    @patch("gui._28_systemd_status_refresh_daemon.refresh_systemd_status.get_timer_status")
    def test_all_true_sets_green_badges(self, mock_status, qapp):
        """installed/active/enabled all True → green badges."""
        from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import (
            refresh_systemd_status,
        )
        mock_status.return_value = {"installed": True, "active": True, "enabled": True}
        w = _make_window()
        refresh_systemd_status(w)

        w.lbl_sys_service.setText.assert_called_once_with("Service Unit: Installed")
        w.lbl_sys_service.setStyleSheet.assert_called_once_with(_GREEN)
        w.lbl_sys_timer.setText.assert_called_once_with("Timer Status: Active")
        w.lbl_sys_timer.setStyleSheet.assert_called_once_with(_GREEN)
        w.lbl_sys_enabled.setText.assert_called_once_with("Systemd Auto-Start: Enabled")
        w.lbl_sys_enabled.setStyleSheet.assert_called_once_with(_GREEN)

    @patch("gui._28_systemd_status_refresh_daemon.refresh_systemd_status.get_timer_status")
    def test_all_false_sets_red_gray_badges(self, mock_status, qapp):
        """installed=False → red; active/enabled=False → gray badges."""
        from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import (
            refresh_systemd_status,
        )
        mock_status.return_value = {"installed": False, "active": False, "enabled": False}
        w = _make_window()
        refresh_systemd_status(w)

        w.lbl_sys_service.setText.assert_called_once_with("Service Unit: Not Installed")
        w.lbl_sys_service.setStyleSheet.assert_called_once_with(_RED)
        w.lbl_sys_timer.setText.assert_called_once_with("Timer Status: Inactive")
        w.lbl_sys_timer.setStyleSheet.assert_called_once_with(_GRAY)
        w.lbl_sys_enabled.setText.assert_called_once_with("Systemd Auto-Start: Disabled")
        w.lbl_sys_enabled.setStyleSheet.assert_called_once_with(_GRAY)

    @patch("gui._28_systemd_status_refresh_daemon.refresh_systemd_status.get_timer_status")
    def test_exception_logs_and_preserves_badges(self, mock_status, qapp):
        """get_timer_status raises → append_log_message called, badges unchanged."""
        from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import (
            refresh_systemd_status,
        )
        mock_status.side_effect = RuntimeError("no systemd")
        w = _make_window()
        refresh_systemd_status(w)
        assert w.lbl_sys_service.setText.call_count == 0
        assert w.lbl_sys_timer.setText.call_count == 0
        assert w.lbl_sys_enabled.setText.call_count == 0
