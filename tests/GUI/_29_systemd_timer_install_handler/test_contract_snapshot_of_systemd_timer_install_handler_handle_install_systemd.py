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
# LAYER BREAKDOWN:
#   Layer 1 (Structural):  test_signature, test_source_imports
#   Layer 2 (Behavioral): test_success_path, test_failure_path
#
# LAYER WHAT EACH TEST CHECKS:
#   test_signature          — function param name, kind, default, return annotation
#   test_source_imports     — required modules imported via AST
#   test_success_path       — True result → info dialog + log + refresh called
#   test_failure_path       — False result → critical dialog + log + refresh called
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
    r"""Build a minimal WindowStub.

    WHAT: Constructs a stub window that satisfies the minimal attribute
          requirements of handle_install_systemd.

    OPTIONS:
      None — WindowStub provides all default mock attributes.

    DEFAULTS: All expected widgets and attributes are auto-mocked by WindowStub.

    OUTPUT/EFFECT: Returns a WindowStub ready for handle_install_systemd tests.

    ERRORS/EDGE CASES: None — stub is intentionally minimal.

    HOW TO TEST: Inspect returned object for any attributes the source function accesses.
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
          without executing any installation logic.

    OPTIONS:
      None — purely static, no Qt event loop needed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Assertions pass if signature, imports, and callable contract hold.

    ERRORS/EDGE CASES: Any mismatch raises AssertionError indicating contract drift.

    HOW TO TEST: Run pytest on this class alone; all tests are fast and deterministic.
    """

    def test_signature(self):
        r"""WHAT: Confirm handle_install_systemd accepts exactly one positional-or-keyword
                  parameter named 'window' and annotates return as None.

        OPTIONS:
          None — inspects the real function object directly.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: params list and return_annotation asserted.

        ERRORS/EDGE CASES: Extra params, wrong kind, or missing return annotation → fail.

        HOW TO TEST: Import the function and call inspect.signature on it.
        """
        import inspect
        from gui._29_systemd_timer_install_handler.handle_install_systemd import (
            handle_install_systemd,
        )
        sig = inspect.signature(handle_install_systemd)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        r"""WHAT: Ensure the source module imports QMessageBox, install_systemd_timer,
                  append_log_message, and refresh_systemd_status, confirming all
                  four dependency contracts are declared in the source AST.

        OPTIONS:
          None — uses assert_source_imports helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Assertion passes if all four module paths appear in source AST.

        ERRORS/EDGE CASES: Missing import → assert_source_imports raises AssertionError.

        HOW TO TEST: Run this test; it reads the .py file and walks the AST.
        """
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
    r"""Behavioral smoke tests against the real function.

    WHAT: Executes handle_install_systemd with mocked dependencies and asserts
          the correct combination of dialog, log, and status-refresh calls for
          both the success and failure installation paths.

    OPTIONS:
      qapp fixture: provides a QApplication instance for PyQt6 widget tests.
      mock_install patch: controls the return value of install_systemd_timer.
      mock_info / mock_critical patches: intercept QMessageBox class methods.
      mock_log patch: intercepts append_log_message.
      mock_refresh patch: intercepts refresh_systemd_status.

    DEFAULTS: Uses _make_window() with default WindowStub attributes.

    OUTPUT/EFFECT: Dialog shown, log written, status refreshed — all mocked.

    ERRORS/EDGE CASES: Each sub-test covers success vs. failure return path.

    HOW TO TEST: Run pytest on this class; all tests require the qapp fixture.
    """

    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.refresh_systemd_status")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.append_log_message")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.QMessageBox.information")
    @patch("gui._29_systemd_timer_install_handler.handle_install_systemd.install_systemd_timer")
    def test_success_path(self, mock_install, mock_info, mock_log, mock_refresh, qapp):
        r"""WHAT: When install_systemd_timer returns True, the handler must show
                  an information dialog, write a success log, and refresh status badges.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_install: patched to return True (simulating successful installation).
          mock_info: intercepted QMessageBox.information call.
          mock_log: intercepted append_log_message call.
          mock_refresh: intercepted refresh_systemd_status call.
          _make_window(): provides stub window.

        DEFAULTS: Success log message: "Successfully installed and launched systemd user timer (rss-scraper.timer)."

        OUTPUT/EFFECT: All four mocks called exactly once with expected args.

        ERRORS/EDGE CASES: None — this is the primary success scenario.

        HOW TO TEST: Set mock_install.return_value = True, call function, assert each mock.
        """
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
        r"""WHAT: When install_systemd_timer returns False, the handler must show
                  a critical dialog, write a failure log, and refresh status badges.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_install: patched to return False (simulating failed installation).
          mock_critical: intercepted QMessageBox.critical call.
          mock_log: intercepted append_log_message call.
          mock_refresh: intercepted refresh_systemd_status call.
          _make_window(): provides stub window.

        DEFAULTS: Failure log message: "Failed to install systemd user timer."

        OUTPUT/EFFECT: All four mocks called exactly once with expected args.

        ERRORS/EDGE CASES: None — this is the primary failure scenario.

        HOW TO TEST: Set mock_install.return_value = False, call function, assert each mock.
        """
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
