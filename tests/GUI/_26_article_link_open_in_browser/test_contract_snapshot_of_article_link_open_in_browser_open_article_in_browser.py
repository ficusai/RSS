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
# LAYER BREAKDOWN:
#   Layer 1 (Structural):  test_signature, test_source_imports
#   Layer 2 (Behavioral): test_opens_url_when_property_present,
#                         test_no_op_when_url_missing
#
# LAYER WHAT EACH TEST CHECKS:
#   test_signature              — function param name, kind, default, return annotation
#   test_source_imports         — required PyQt6 imports via AST
#   test_opens_url_when_property_present — openUrl called once with QUrl(url)
#   test_no_op_when_url_missing                    — openUrl not called when property absent
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

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


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
    r"""Build a minimal WindowStub with btn_open.url property set.

    WHAT: Constructs a stub window where btn_open.property("url") returns
          a valid article URL, simulating a selected article's button state.

    OPTIONS:
      None — URL is hardcoded to https://example.com/article.

    DEFAULTS: btn_open.property("url") → "https://example.com/article".

    OUTPUT/EFFECT: Returns a WindowStub ready for open_article_in_browser tests.

    ERRORS/EDGE CASES: None — stub is intentionally minimal.

    HOW TO TEST: Inspect btn_open.property mock return value.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.btn_open.property = MagicMock(return_value="https://example.com/article")
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    r"""Structural / signature / import contract checks.

    WHAT: Verifies that the source module's public API matches the declared
          contract — function signature, return type, and required PyQt6 imports —
          without executing any browser-launching logic.

    OPTIONS:
      None — purely static, no Qt event loop needed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Assertions pass if signature, imports, and callable contract hold.

    ERRORS/EDGE CASES: Any mismatch raises AssertionError indicating contract drift.

    HOW TO TEST: Run pytest on this class alone; all tests are fast and deterministic.
    """

    def test_signature(self):
        r"""WHAT: Confirm open_article_in_browser accepts exactly one positional-or-keyword
                  parameter named 'window' and annotates return as None.

        OPTIONS:
          None — inspects the real function object directly.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: params list and return_annotation asserted.

        ERRORS/EDGE CASES: Extra params, wrong kind, or missing return annotation → fail.

        HOW TO TEST: Import the function and call inspect.signature on it.
        """
        import inspect
        from gui._26_article_link_open_in_browser.open_article_in_browser import (
            open_article_in_browser,
        )
        sig = inspect.signature(open_article_in_browser)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        r"""WHAT: Ensure the source module imports QUrl and QDesktopServices from
                  PyQt6, confirming the browser-launch dependency is declared.

        OPTIONS:
          None — uses assert_source_imports helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Assertion passes if both PyQt6 module paths appear in source AST.

        ERRORS/EDGE CASES: Missing import → assert_source_imports raises AssertionError.

        HOW TO TEST: Run this test; it reads the .py file and walks the AST.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._26_article_link_open_in_browser.open_article_in_browser"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"PyQt6.QtCore", "Py Qt6.QtGui"},
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    r"""Behavioral smoke tests against the real function.

    WHAT: Executes open_article_in_browser with a WindowStub whose btn_open
          carries a "url" Qt property, and asserts that QDesktopServices.openUrl
          is invoked exactly once with the correct QUrl — or not at all when
          the property is absent.

    OPTIONS:
      qapp fixture: provides a QApplication instance for PyQt6 widget tests.
      mock_open patch: intercepts QDesktopServices.openUrl to verify arguments.

    DEFAULTS: Uses _make_window() with a valid URL property.

    OUTPUT/EFFECT: Browser opened (mocked); no unexpected calls when URL missing.

    ERRORS/EDGE CASES: Each sub-test covers presence vs. absence of url property.

    HOW TO TEST: Run pytest on this class; all tests require the qapp fixture.
    """

    @patch("gui._26_article_link_open_in_browser.open_article_in_browser.QDesktopServices.openUrl")
    def test_opens_url_when_property_present(self, mock_open, qapp):
        r"""WHAT: When btn_open holds a "url" property, open_article_in_browser
                  must call QDesktopServices.openUrl exactly once with a QUrl wrapping that string.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_open: patched QDesktopServices.openUrl to capture the call.
          _make_window(): provides stub with btn_open.property("url") → valid URL.

        DEFAULTS: URL is "https://example.com/article".

        OUTPUT/EFFECT: mock_open called once with QUrl("https://example.com/article").

        ERRORS/EDGE CASES: None — this is the primary success scenario.

        HOW TO TEST: Call open_article_in_browser(w) then assert mock_open call args.
        """
        from gui._26_article_link_open_in_browser.open_article_in_browser import (
            open_article_in_browser,
        )
        w = _make_window()
        open_article_in_browser(w)
        mock_open.assert_called_once_with(QUrl("https://example.com/article"))

    @patch("gui._26_article_link_open_in_browser.open_article_in_browser.QDesktopServices.openUrl")
    def test_no_op_when_url_missing(self, mock_open, qapp):
        r"""WHAT: When btn_open has no "url" property (returns None),
                  open_article_in_browser must not attempt to open anything.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          mock_open: patched QDesktopServices.openUrl to verify it is never called.
          w.btn_open.property overridden to return None.

        DEFAULTS: _make_window() normally returns a valid URL; overridden here.

        OUTPUT/EFFECT: mock_open never called; function exits silently.

        ERRORS/EDGE CASES: None — missing URL is a valid no-op condition.

        HOW TO TEST: Override property to None, call function, assert_not_called.
        """
        from gui._26_article_link_open_in_browser.open_article_in_browser import (
            open_article_in_browser,
        )
        w = _make_window()
        w.btn_open.property = MagicMock(return_value=None)
        open_article_in_browser(w)
        mock_open.assert_not_called()
