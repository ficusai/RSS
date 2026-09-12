"""Contract snapshot: gui/_27_article_link_copy_to_clipboard/copy_article_link.py v1.0.0

Structural contract:
  - Function name: copy_article_link
  - Signature: (window) -> None
  - Source imports: PyQt6.QtWidgets (QApplication, QMessageBox),
                   gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
  - Side effects: QApplication.clipboard().setText(url),
                  append_log_message(window, ...),
                  QMessageBox.information(window, ...)
"""
# ==============================================================================
# WHAT: Verifies the copy_article_link GUI contract — clipboard copy, log
#       append, and info dialog shown when a URL property is present on the button.
#
# OPTIONS:
#   window: MainWindow stub with btn_copy_link.url property set.
#
# DEFAULTS: No-op when url property is missing.
#
# OUTPUT/EFFECT: Clipboard updated; log appended; info dialog shown.
#
# ERRORS/EDGE CASES: None — clipboard operations handled by the OS.
#
# HOW TO TEST: copy_article_link(window) after selecting an article
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
    """Build a minimal WindowStub with btn_copy_link.url property set."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.btn_copy_link.property = MagicMock(return_value="https://example.com/article")
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert copy_article_link(window) -> None."""
        import inspect
        from gui._27_article_link_copy_to_clipboard.copy_article_link import (
            copy_article_link,
        )
        sig = inspect.signature(copy_article_link)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import QApplication, QMessageBox and append_log_message."""
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
    """Behavioral smoke tests against the real function."""

    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.QMessageBox.information")
    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.append_log_message")
    def test_copies_clipboard_and_logs_and_shows_dialog(self, mock_log, mock_info, qapp):
        """URL property present → clipboard updated, log appended, dialog shown."""
        from gui._27_article_link_copy_to_clipboard.copy_article_link import (
            copy_article_link,
        )
        w = _make_window()
        copy_article_link(w)
        url = "https://example.com/article"
        QApplication.clipboard().setText.assert_called_once_with(url)
        mock_log.assert_called_once_with(w, f"Copied URL to clipboard: {url}")
        mock_info.assert_called_once_with(w, "Link Copied", "Article URL copied to clipboard!")

    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.QMessageBox.information")
    @patch("gui._27_article_link_copy_to_clipboard.copy_article_link.append_log_message")
    def test_no_op_when_url_missing(self, mock_log, mock_info, qapp):
        """No url property → clipboard not touched, dialog not shown."""
        from gui._27_article_link_copy_to_clipboard.copy_article_link import (
            copy_article_link,
        )
        w = _make_window()
        w.btn_copy_link.property = MagicMock(return_value=None)
        copy_article_link(w)
        QApplication.clipboard().setText.assert_not_called()
        mock_log.assert_not_called()
        mock_info.assert_not_called()
