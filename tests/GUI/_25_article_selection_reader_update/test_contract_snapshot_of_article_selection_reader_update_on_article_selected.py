"""Contract snapshot: gui/_25_article_selection_reader_update/on_article_selected.py v1.0.0

Structural contract:
  - Function name: on_article_selected
  - Signature: (window) -> None
  - Source import: features.feature_gui_reader_pro.implementation.reader_pro_components.calculate_reading_time_minutes
  - Side effects: window.lbl_reader_title.setText, window.lbl_reader_meta.setText,
                  window.txt_reader.setPlainText, window.btn_open.setEnabled,
                  window.btn_copy_link.setEnabled, window.btn_open.setProperty,
                  window.btn_copy_link.setProperty
"""
# ==============================================================================
# WHAT: Verifies the on_article_selected GUI contract — reader pane population
#       from the currently selected article, button enablement, and URL property
#       storage on btn_open / btn_copy_link.
#
# LAYER BREAKDOWN:
#   Layer 1 (Structural):  test_signature, test_source_imports,
#                          test_calculate_reading_time_minutes_callable
#   Layer 2 (Behavioral): test_populates_reader_pane_and_enables_buttons,
#                         test_empty_selection_returns_early,
#                         test_out_of_range_row_returns_early,
#                         test_no_url_disables_buttons,
#                         test_meta_includes_read_time
#
# LAYER WHAT EACH TEST CHECKS:
#   test_signature              — function param name, kind, default, return annotation
#   test_source_imports         — required module import via AST
#   test_calculate_reading_time_minutes_callable — imported func is callable & returns expected value
#   test_populates_reader_pane_and_enables_buttons — reader text/labels/buttons set correctly
#   test_empty_selection_returns_early                  — no side effects on empty selection
#   test_out_of_range_row_returns_early                 — no crash on bad row index
#   test_no_url_disables_buttons                        — buttons disabled when URL absent
#   test_meta_includes_read_time                        — reading time in metadata string
#
# OPTIONS:
#   window: MainWindow stub with table_articles, current_articles, reader widgets.
#
# DEFAULTS: Returns early if no selection or row out of bounds.
#
# OUTPUT/EFFECT: Reader pane populated; buttons enabled/disabled; URL stored.
#
# ERRORS/EDGE CASES: Empty selection or out-of-range row → no crash, early return.
#
# HOW TO TEST: on_article_selected(window) after selecting a row in table_articles
# ==============================================================================
import importlib.util
import pytest
from unittest.mock import MagicMock, call

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
    r"""Build a minimal WindowStub matching what on_article_selected needs.

    WHAT: Constructs a stub window object that mimics the attributes
          on_article_selected reads from a real MainWindow.

    OPTIONS:
      None — uses hardcoded test article data.

    DEFAULTS: table_articles.selectedIndexes() returns one index at row 0.

    OUTPUT/EFFECT: Returns a WindowStub with all required reader-pane attrs.

    ERRORS/EDGE CASES: None — stub is intentionally minimal.

    HOW TO TEST: Inspect returned object for lbl_reader_title, lbl_reader_meta,
                 txt_reader, btn_open, btn_copy_link, table_articles, current_articles.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    # table_articles.selectedIndexes() returns a list of mock QModelIndex objects
    idx = MagicMock()
    idx.row.return_value = 0
    w.table_articles.selectedIndexes = MagicMock(return_value=[idx])
    w.current_articles = [
        {
            "title": "Test Article",
            "feed_name": "Test Feed",
            "author": "Test Author",
            "published_at_iso": "2025-01-15T10:00:00Z",
            "url": "https://example.com/article",
            "preview": "Short preview text here.",
            "full_text_clean": "This is the full text of the test article.",
        }
    ]
    w.lbl_reader_title = MagicMock()
    w.lbl_reader_meta = MagicMock()
    w.txt_reader = MagicMock()
    w.btn_open = MagicMock()
    w.btn_copy_link = MagicMock()
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    r"""Structural / signature / import contract checks.

    WHAT: Verifies that the source module's public API matches the declared
          contract — function name, parameter signature, return type, and
          required imports — without executing any GUI logic.

    OPTIONS:
      None — purely static, no Qt event loop needed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Assertions pass if signature, imports, and callable contract hold.

    ERRORS/EDGE CASES: Any mismatch raises AssertionError indicating contract drift.

    HOW TO TEST: Run pytest on this class alone; all three tests are fast and deterministic.
    """

    def test_signature(self):
        r"""WHAT: Confirm on_article_selected accepts exactly one positional-or-keyword
                  parameter named 'window' and annotates return as None.

        OPTIONS:
          None — inspects the real function object directly.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: params list and return_annotation asserted.

        ERRORS/EDGE CASES: Extra params, wrong kind, or missing return annotation → fail.

        HOW TO TEST: Import the function and call inspect.signature on it.
        """
        import inspect
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        sig = inspect.signature(on_article_selected)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        r"""WHAT: Ensure the source module imports from the reader_pro_components
                  package, confirming the reading-time dependency is declared.

        OPTIONS:
          None — uses assert_source_imports helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Assertion passes if the expected module path appears in source AST.

        ERRORS/EDGE CASES: Missing import → assert_source_imports raises AssertionError.

        HOW TO TEST: Run this test; it reads the .py file and walks the AST.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._25_article_selection_reader_update.on_article_selected"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"features.feature_gui_reader_pro.implementation.reader_pro_components"},
        )

    def test_calculate_reading_time_minutes_callable(self):
        r"""WHAT: Verify calculate_reading_time_minutes is importable, callable,
                  and returns the expected integer for a known input string.

        OPTIONS:
          Input string: "hello world" (2 words → expected 1 minute).

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Confirms the utility function works as a black box.

        ERRORS/EDGE CASES: Non-callable import or wrong return value → fail.

        HOW TO TEST: Import and call calculate_reading_time_minutes("hello world").
        """
        from features.feature_gui_reader_pro.implementation.reader_pro_components import (
            calculate_reading_time_minutes,
        )
        assert callable(calculate_reading_time_minutes)
        assert calculate_reading_time_minutes("hello world") == 1


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    r"""Behavioral smoke tests against the real function.

    WHAT: Executes on_article_selected with a realistic WindowStub and
          asserts that reader-pane widgets receive the correct setText /
          setPlainText / setEnabled / setProperty calls.

    OPTIONS:
      qapp fixture: provides a QApplication instance for PyQt6 widget tests.

    DEFAULTS: Uses _make_window() with one test article and a selected row 0.

    OUTPUT/EFFECT: Reader pane populated; buttons state updated; no crash.

    ERRORS/EDGE CASES: Each sub-test covers a different edge condition.

    HOW TO TEST: Run pytest on this class; all tests require the qapp fixture.
    """

    def test_populates_reader_pane_and_enables_buttons(self, qapp):
        r"""WHAT: Full happy-path test — article selected, reader pane fields set,
                  both action buttons enabled, and URL property stored on each.

        OPTIONS:
          qapp: required for PyQt6 widget creation.
          _make_window(): provides a stub with one article and row 0 selected.

        DEFAULTS: Returns the first article from current_articles.

        OUTPUT/EFFECT: lbl_reader_title, lbl_reader_meta, txt_reader, btn_open,
                       btn_copy_link all receive their expected calls.

        ERRORS/EDGE CASES: None — this is the primary success scenario.

        HOW TO TEST: on_article_selected(w) then inspect mock call history.
        """
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )

        w = _make_window()
        on_article_selected(w)

        # Reader pane populated
        w.lbl_reader_title.setText.assert_called_once_with("Test Article")
        meta_text = w.lbl_reader_meta.setText.call_args[0][0]
        assert "Test Feed" in meta_text
        assert "Test Author" in meta_text
        assert "2025-01-15" in meta_text
        assert "min read" in meta_text
        w.txt_reader.setPlainText.assert_called_once()

        # Buttons enabled + URL property stored
        w.btn_open.setEnabled.assert_called_once_with(True)
        w.btn_copy_link.setEnabled.assert_called_once_with(True)
        assert w.btn_open.setProperty.call_args_list == [call("url", "https://example.com/article")]
        assert w.btn_copy_link.setProperty.call_args_list == [call("url", "https://example.com/article")]

    def test_empty_selection_returns_early(self, qapp):
        r"""WHAT: When no rows are selected in table_articles, the function must
                  return without touching any reader-pane widgets.

        OPTIONS:
          qapp: required fixture.
          w.table_articles.selectedIndexes = MagicMock(return_value=[]): zero selections.

        DEFAULTS: _make_window() still provides article data, but selection is empty.

        OUTPUT/EFFECT: No setText, setEnabled, or setProperty calls on any widget.

        ERRORS/EDGE CASES: Function must not crash or raise on empty selection.

        HOW TO TEST: Set selectedIndexes to [] then assert_not_called on key widgets.
        """
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        w = _make_window()
        w.table_articles.selectedIndexes = MagicMock(return_value=[])
        on_article_selected(w)
        w.lbl_reader_title.setText.assert_not_called()
        w.btn_open.setEnabled.assert_not_called()

    def test_out_of_range_row_returns_early(self, qapp):
        r"""WHAT: When the selected row index exceeds len(current_articles),
                  the function returns early without side effects.

        OPTIONS:
          qapp: required fixture.
          idx.row.return_value = 99: simulates a stale or invalid selection.
          w.current_articles = []: empty article list amplifies the out-of-range case.

        DEFAULTS: _make_window() normally has row 0 selected; overridden here.

        OUTPUT/EFFECT: No reader-pane widget calls; function exits cleanly.

        ERRORS/EDGE CASES: IndexError must be caught or guarded against.

        HOW TO TEST: Set row to 99 with empty articles, call function, assert no calls.
        """
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        w = _make_window()
        idx = MagicMock()
        idx.row.return_value = 99
        w.table_articles.selectedIndexes = MagicMock(return_value=[idx])
        w.current_articles = []
        on_article_selected(w)
        w.lbl_reader_title.setText.assert_not_called()

    def test_no_url_disables_buttons(self, qapp):
        r"""WHAT: An article that lacks a 'url' key must cause both action buttons
                  to be disabled, with no URL property stored on either.

        OPTIONS:
          qapp: required fixture.
          w.current_articles overridden to contain an article with no 'url' key.

        DEFAULTS: _make_window() normally provides a full article with URL.

        OUTPUT/EFFECT: btn_open.setEnabled(False), btn_copy_link.setEnabled(False),
                       no setProperty calls.

        ERRORS/EDGE CASES: Article with missing URL should not crash.

        HOW TO TEST: Replace current_articles with URL-less article, call function.
        """
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        w = _make_window()
        w.current_articles = [{"title": "No URL", "full_text_clean": "content"}]
        on_article_selected(w)
        w.btn_open.setEnabled.assert_called_once_with(False)
        w.btn_copy_link.setEnabled.assert_called_once_with(False)
        w.btn_open.setProperty.assert_not_called()
        w.btn_copy_link.setProperty.assert_not_called()

    def test_meta_includes_read_time(self, qapp):
        r"""WHAT: The metadata string rendered by lbl_reader_meta.setText must
                  contain the estimated reading time (e.g. 'min read').

        OPTIONS:
          qapp: required fixture.
          _make_window() with normal article data including full_text_clean.

        DEFAULTS: Reading time is computed from full_text_clean word count.

        OUTPUT/EFFECT: meta_text contains the substring "min read".

        ERRORS/EDGE CASES: If calculate_reading_time_minutes returns 0, string may differ.

        HOW TO TEST: Call on_article_selected, extract first arg of setText, check substring.
        """
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        w = _make_window()
        on_article_selected(w)
        meta = w.lbl_reader_meta.setText.call_args[0][0]
        assert "min read" in meta
