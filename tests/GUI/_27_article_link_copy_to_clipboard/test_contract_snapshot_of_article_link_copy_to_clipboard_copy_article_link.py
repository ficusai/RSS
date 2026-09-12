"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_27_article_link_copy_to_clipboard/copy_article_link.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the copy_article_link function — the GUI handler that
copies the currently selected article's URL to the system clipboard when the
user clicks the "Copy Link" button. It reads the "url" Qt property from
window.btn_copy_link (set by on_article_selected when an article row was
chosen), writes it to the OS clipboard via QApplication.clipboard().setText(),
appends a timestamped log message to the operations console, and shows an
information dialog ("Article URL copied to clipboard!") to give the user
immediate visual confirmation. If the button has no URL property, the
function is a safe no-op: nothing is written, logged, or displayed.

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_signature              : copy_article_link(window) -> None exact signature
  - test_source_imports         : Module imports QApplication/QMessageBox from PyQt6
                                 and append_log_message

Layer 2 (Behavioral):
  - test_copies_clipboard_and_logs_and_shows_dialog : All three side effects occur
  - test_no_op_when_url_missing                         : No side effects when URL absent

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# importlib.util: Finds the filesystem path of the source module for AST-based
#                 import verification in the structural tests.
import importlib.util

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

# pytest: The test runner that discovers and executes these tests.
import pytest
# unittest.mock.MagicMock: Creates fake objects that record every method call.
# unittest.mock.patch:     Temporarily replaces module attributes with mocks so
#                          we can verify calls without running real code.
from unittest.mock import MagicMock, patch

# os: Reads and writes environment variables.
# The two lines below set QT_QPA_PLATFORM=offscreen BEFORE any PyQt6 widget
# is instantiated, preventing the test process from trying to open a real X11
# or Wayland display during headless CI runs.
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# PyQt6.QtWidgets.QApplication: The Qt application object required before any
# Qt widget can be created. We import it here (after the offscreen env var)
# so the real PyQt6 library loads in offscreen mode.
from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform

# Module-level QApplication instance. Uses QApplication.instance() to reuse
# an existing app created by another test module, preventing the PyQt6 crash
# that occurs when multiple QApplications exist in the same process.
_qapp = QApplication.instance() or QApplication([])



def _make_window():
    """Build a minimal WindowStub with btn_copy_link.url property set.

    WHAT: Creates a WindowStub from conftest and configures btn_copy_link to
          return a realistic article URL when its property("url") method is
          called. This simulates the state left by on_article_selected after
          a row is selected.

    OPTIONS: None — the stub is constructed with a fixed shape.

    DEFAULTS: URL is "https://example.com/article".

    OUTPUT/EFFECT: Returns a WindowStub where:
      - btn_copy_link.property("url") returns "https://example.com/article"

    ERRORS/EDGE CASES:
      - WindowStub missing in conftest: ImportError
      - Missing btn_copy_link attribute: AttributeError at call time
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.btn_copy_link.property = MagicMock(return_value="https://example.com/article")
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks.

    WHAT: Verifies the surface-level contract of copy_article_link — its
          function signature and its required imports (QApplication for
          clipboard access, QMessageBox for the confirmation dialog, and
          append_log_message for logging). These are the safest tests: if
          the source file is renamed, relocated, or refactored, these checks
          catch the drift before any behavioral test runs.
    """

    def test_signature(self):
        """assert copy_article_link(window) -> None.

        WHAT: Verifies the function has exactly one required parameter named
              "window" and a return type annotation of None.

        WHY SIGNATURE MATTERS:
              Every caller uses: copy_article_link(window)
              If the parameter count or name changed, all callers break with TypeError.

        OPTIONS:
          - Parameter name: must be exactly "window"
          - Parameter kind: POSITIONAL_OR_KEYWORD
          - Default: none (required)
          - Return type: must be annotated as None

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes if signature matches exactly.

        ERRORS/EDGE CASES:
          - Wrong parameter name: params mismatch
          - Added default: default mismatch
          - Missing return annotation: return_annotation == inspect.Parameter.empty

        HOW TO TEST: Change parameter from "window" to "app" in source.
                     Run this test — it should fail with params mismatch.
        """
        import inspect
        from gui._27_article_link_copy_to_clipboard.copy_article_link import (
            copy_article_link,
        )
        sig = inspect.signature(copy_article_link)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import QApplication, QMessageBox and append_log_message.

        WHAT: Verifies the source file imports exactly two categories of
              dependencies:
              - PyQt6.QtWidgets (for QApplication.clipboard and
                QMessageBox.information)
              - gui._10_log_append_timestamped_message.append_timestamped_log
                (for appending a timestamped log entry)

        OPTIONS: The expected import set contains exactly those two module
                 paths. QMessageBox itself is accessed as an attribute of
                 PyQt6.QtWidgets, not imported separately.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes if the AST of the source file contains both
                       expected imports; otherwise lists missing or extra.

        ERRORS/EDGE CASES:
          - Import removed or renamed: assert_source_imports fails
          - Extra import added: assert_source_imports lists the unexpected name

        HOW TO TEST: Remove the PyQt6.QtWidgets import from source. Run this
                     test — it should fail with missing import.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._27_article_link_copy_to_clipboard.copy_article_link"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"PyQt6.QtWidgets", "gui._10_log_append_timestamped_message.append_timestamped_log"},
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real function.

    WHAT: Runs the REAL copy_article_link function against a WindowStub and
          replaces QApplication.clipboard, append_log_message, and
          QMessageBox.information with recording mocks. This lets us verify
          all three side effects occur in the correct order without actually
          touching the system clipboard or showing real dialogs.
    """

    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.QMessageBox.information")
    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.append_log_message")
    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.QApplication.clipboard")
    def test_copies_clipboard_and_logs_and_shows_dialog(self, mock_clipboard, mock_log, mock_info):
        """URL property present → clipboard updated, log appended, dialog shown.

        WHAT: Calls copy_article_link(w) on a window stub whose btn_copy_link
              has a "url" property set to "https://example.com/article".
              Passes only if all three side effects occurred:
              1. QApplication.clipboard().setText(url) — URL written to clipboard
              2. append_log_message(w, "Copied URL to clipboard: <url>") — log entry
              3. QMessageBox.information(w, "Link Copied", "Article URL copied to clipboard!") — confirmation dialog

        WHY ALL THREE:
              Copying to clipboard is an invisible operation from the user's
              perspective. The log entry provides an audit trail, and the
              information dialog gives immediate visual feedback so the user
              knows the action succeeded.

        OPTIONS:
          - window: WindowStub with btn_copy_link.property("url") → URL string

        DEFAULTS: N/A — explicit URL set in the stub.

        OUTPUT/EFFECT: Clipboard text set; log appended with formatted message;
                       info dialog shown with title and message.

        ERRORS/EDGE CASES:
          - Wrong URL in clipboard: setText assertion fails
          - Wrong log message format: assert_called_once_with fails
          - Dialog title or message wrong: assert_called_once_with fails
          - Any effect missing: assert_called_once fails (not called)
          - Extra calls: assert_called_once fails (called multiple times)

        HOW TO TEST: Call the function and inspect mock_clipboard, mock_log,
                     and mock_info.call_args. All three should match the
                     expected arguments exactly.
        """
        from gui._27_article_link_copy_to_clipboard.copy_article_link import (
            copy_article_link,
        )
        w = _make_window()
        copy_article_link(w)
        url = "https://example.com/article"
        mock_clipboard.return_value.setText.assert_called_once_with(url)
        mock_log.assert_called_once_with(w, f"Copied URL to clipboard: {url}")
        mock_info.assert_called_once_with(w, "Link Copied", "Article URL copied to clipboard!")

    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.QMessageBox.information")
    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.append_log_message")
    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.QApplication.clipboard")
    def test_no_op_when_url_missing(self, mock_clipboard, mock_log, mock_info):
        """No url property → clipboard not touched, dialog not shown.

        WHAT: Calls copy_article_link(w) on a window stub whose btn_copy_link
              has no "url" property (property returns None). Passes only if
              none of the three side effects occurred — the function treats a
              missing URL as "nothing to do" rather than an error.

        WHY NO-OP:
              If the user somehow triggers this function without having
              selected an article first (or if the article had no URL), the
              function should not crash, write garbage to the clipboard, or
              show a confusing dialog. It should silently do nothing.

        OPTIONS:
          - window: WindowStub with btn_copy_link.property("url") → None

        DEFAULTS: N/A.

        OUTPUT/EFFECT: All three mocks report zero calls.

        ERRORS/EDGE CASES:
          - Clipboard written with None: assertion fails
          - Dialog shown without URL: assertion fails
          - Function crashes: exception raised instead of graceful no-op

        HOW TO TEST: Set property return_value to None and call the function.
                     Verify all three mocks were never invoked.
        """
        from gui._27_article_link_copy_to_clipboard.copy_article_link import (
            copy_article_link,
        )
        w = _make_window()
        w.btn_copy_link.property = MagicMock(return_value=None)
        copy_article_link(w)
        mock_clipboard.return_value.setText.assert_not_called()
        mock_log.assert_not_called()
        mock_info.assert_not_called()
