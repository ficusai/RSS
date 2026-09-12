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
# LAYER BREAKDOWN:
#   Layer 1 (Structural):  test_signature, test_source_imports
#   Layer 2 (Behavioral): test_all_true_sets_green_badges,
#                         test_all_false_sets_red_gray_badges,
#                         test_exception_logs_and_preserves_badges
#
# LAYER WHAT EACH TEST CHECKS:
#   test_signature                  — function param name, kind, default, return annotation
#   test_source_imports             — required modules imported via AST
#   test_all_true_sets_green_badges — all True → green setText + setStyleSheet on 3 labels
#   test_all_false_sets_red_gray_badges — installed=False → red; active/enabled=False → gray
#   test_exception_logs_and_preserves_badges — exception → no label changes, error logged
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



_GREEN = "background: #0d1117; border: 1px solid #238636; border-radius: 6px; padding: 8px 14px; color: #3fb950; font-weight: 600;"
_RED = "background: #0d1117; border: 1px solid #da3633; border-radius: 6px; padding: 8px 14px; color: #f85149; font-weight: 600;"
_GRAY = "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 14px; color: #8b949e; font-weight: 600;"


def _make_window():
    r"""Build a minimal WindowStub with status labels.

    WHAT: Constructs a stub window that has the three systemd-status label
          widgets the real refresh_systemd_status function expects.

    OPTIONS:
      None — labels are created automatically by WindowStub.

    DEFAULTS: All three labels (lbl_sys_service, lbl_sys_timer, lbl_sys_enabled) exist.

    OUTPUT/EFFECT: Returns a WindowStub ready for refresh_systemd_status tests.

    ERRORS/EDGE CASES: None — stub is intentionally minimal.

    HOW TO TEST: Inspect returned object for lbl_sys_service, lbl_sys_timer, lbl_sys_enabled.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    r"""Structural / signature / import contract checks.

    WHAT: Verifies that the source module's public API matches the declared
          contract — function signature, return type, and required imports —
          without executing any systemd-status-refresh logic.

    OPTIONS:
      None — purely static, no Qt event loop needed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Assertions pass if signature, imports, and callable contract hold.

    ERRORS/EDGE CASES: Any mismatch raises AssertionError indicating contract drift.

    HOW TO TEST: Run pytest on this class alone; all tests are fast and deterministic.
    """

    def test_signature(self):
        r"""WHAT: Confirm refresh_systemd_status accepts exactly one positional-or-keyword
                  parameter named 'window' and annotates return as None.

        OPTIONS:
          None — inspects the real function object directly.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: params list and return_annotation asserted.

        ERRORS/EDGE CASES: Extra params, wrong kind, or missing return annotation → fail.

        HOW TO TEST: Import the function and call inspect.signature on it.
        """
        import inspect
        from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import (
            refresh_systemd_status,
        )
        sig = inspect.signature(refresh_systemd_status)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        r"""WHAT: Ensure the source module imports get_timer_status and append_log_message,
                  confirming both the systemd-status and logging dependencies are declared.

        OPTIONS:
          None — uses assert_source_imports helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Assertion passes if both module paths appear in source AST.

        ERRORS/EDGE CASES: Missing import → assert_source_imports raises AssertionError.

        HOW TO TEST: Run this test; it reads the .py file and walks the AST.
        """
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
    r"""Behavioral smoke tests against the real function.

    WHAT: Executes refresh_systemd_status with mocked get_timer_status return
          values and asserts that the three status labels receive the correct
          setText and setStyleSheet calls for each badge state.

    OPTIONS:
      qapp fixture: provides a QApplication instance for PyQt6 widget tests.
      mock_status patch: controls the return value of get_timer_status.

    DEFAULTS: Uses _make_window() with default WindowStub labels.

    OUTPUT/EFFECT: Badge text and color styles updated to reflect systemd state.

    ERRORS/EDGE CASES: Each sub-test covers a different get_timer_status outcome.

    HOW TO TEST: Run pytest on this class; all tests require the qapp fixture.
    """

    @patch("gui._28_systemd_status_refresh_daemon.refresh_systemd_status.get_timer_status")
    def test_all_true_sets_green_badges(self, mock_status, qapp):
        r"""WHAT: When installed, active, and enabled are all True, all three
                  status badges must show green styling with affirmative text.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_status: patched to return {"installed": True, "active": True, "enabled": True}.
          _make_window(): provides stub with lbl_sys_service, lbl_sys_timer, lbl_sys_enabled.

        DEFAULTS: _GREEN style string applied to all three labels.

        OUTPUT/EFFECT: Each label receives setText + setStyleSheet(_GREEN).

        ERRORS/EDGE CASES: None — this is the primary success scenario.

        HOW TO TEST: Call refresh_systemd_status(w) then assert call_args on each label.
        """
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
        r"""WHAT: When installed is False, the service badge turns red; when
                  active and enabled are False, their badges turn gray.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_status: patched to return {"installed": False, "active": False, "enabled": False}.
          _make_window(): provides stub with lbl_sys_service, lbl_sys_timer, lbl_sys_enabled.

        DEFAULTS: _RED for service label; _GRAY for timer and enabled labels.

        OUTPUT/EFFECT: Each label receives setText + setStyleSheet with appropriate color.

        ERRORS/EDGE CASES: None — this is the primary failure scenario.

        HOW TO TEST: Call refresh_systemd_status(w) then assert call_args on each label.
        """
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
        r"""WHAT: When get_timer_status raises an exception, the function must
                  catch it, log the error, and leave all badge widgets unchanged.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_status: patched to raise RuntimeError("no systemd").
          _make_window(): provides stub with lbl_sys_service, lbl_sys_timer, lbl_sys_enabled.

        DEFAULTS: Exception is caught internally; no label modifications occur.

        OUTPUT/EFFECT: append_log_message called with error; zero setText calls on badges.

        ERRORS/EDGE CASES: RuntimeError simulates systemd not being available.

        HOW TO TEST: Set side_effect = RuntimeError, call function, assert call_count == 0.
        """
        from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import (
            refresh_systemd_status,
        )
        mock_status.side_effect = RuntimeError("no systemd")
        w = _make_window()
        refresh_systemd_status(w)
        assert w.lbl_sys_service.setText.call_count == 0
        assert w.lbl_sys_timer.setText.call_count == 0
        assert w.lbl_sys_enabled.setText.call_count == 0
