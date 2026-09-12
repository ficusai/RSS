"""Contract snapshot: gui/_26_article_link_open_in_browser/open_article_in_browser.py v1.0.0

Structural contract:
  - Function name: open_article_in_browser
  - Signature: (window) -> None
  - Source imports: PyQt6.QtCore.QUrl, PyQt6.QtGui.QDesktopServices
  - Side effects: QDesktopServices.openUrl(QUrl(url)) called once when url property present
"""
# ==============================================================================
# WHAT: Verifies the open_article_in_browser GUI contract — browser URL opens
#       via QDesktopServices.openUrl when the button has a "url" property set.
#
# OPTIONS:
#   window: MainWindow stub with btn_open having a "url" Qt property.
#
# DEFAULTS: No-op when url property is missing.
#
# OUTPUT/EFFECT: System default browser opened with the article URL.
#
# ERRORS/EDGE CASES: None — QDesktopServices.openUrl() handles errors silently.
#
# HOW TO TEST: open_article_in_browser(window) after selecting an article
# ==============================================================================
import importlib.util
import pytest
from unittest.mock import MagicMock, patch

# offscreen platform required for all PyQt6 widget testing
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform
from PyQt6.QtCore import QUrl  # noqa: E402  # offscreen platform


@pytest.fixture(scope="module")
def qapp():
    """Create a single QApplication instance for the module."""
    app = QApplication([])
    yield app



def _make_window():
    """Build a minimal WindowStub with btn_open.url property set."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.btn_open.property = MagicMock(return_value="https://example.com/article")
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert open_article_in_browser(window) -> None."""
        import inspect
        from gui._26_article_link_open_in_browser.open_article_in_browser import (
            open_article_in_browser,
        )
        sig = inspect.signature(open_article_in_browser)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import QUrl and QDesktopServices from PyQt6."""
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._26_article_link_open_in_browser.open_article_in_browser"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"PyQt6.QtCore", "PyQt6.QtGui"},
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real function."""

    @patch("gui._26_article_link_open_in_browser.open_article_in_browser.QDesktopServices.openUrl")
    def test_opens_url_when_property_present(self, mock_open, qapp):
        """btn_open property url set → openUrl called once with QUrl(url)."""
        from gui._26_article_link_open_in_browser.open_article_in_browser import (
            open_article_in_browser,
        )
        w = _make_window()
        open_article_in_browser(w)
        mock_open.assert_called_once_with(QUrl("https://example.com/article"))

    @patch("gui._26_article_link_open_in_browser.open_article_in_browser.QDesktopServices.openUrl")
    def test_no_op_when_url_missing(self, mock_open, qapp):
        """No url property → QDesktopServices.openUrl not called."""
        from gui._26_article_link_open_in_browser.open_article_in_browser import (
            open_article_in_browser,
        )
        w = _make_window()
        w.btn_open.property = MagicMock(return_value=None)
        open_article_in_browser(w)
        mock_open.assert_not_called()
