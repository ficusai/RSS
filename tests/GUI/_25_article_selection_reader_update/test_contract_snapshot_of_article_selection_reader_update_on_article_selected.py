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
    """Build a minimal WindowStub matching what on_article_selected needs."""
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
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert on_article_selected(window) -> None."""
        import inspect
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        sig = inspect.signature(on_article_selected)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import calculate_reading_time_minutes."""
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._25_article_selection_reader_update.on_article_selected"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"features.feature_gui_reader_pro.implementation.reader_pro_components"},
        )

    def test_calculate_reading_time_minutes_callable(self):
        """calculate_reading_time_minutes must be importable and callable."""
        from features.feature_gui_reader_pro.implementation.reader_pro_components import (
            calculate_reading_time_minutes,
        )
        assert callable(calculate_reading_time_minutes)
        assert calculate_reading_time_minutes("hello world") == 1


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real function."""

    def test_populates_reader_pane_and_enables_buttons(self, qapp):
        """Real QTableWidget selection populates reader; buttons enabled with URL property."""
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
        """No selected rows → function returns without side effects."""
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        w = _make_window()
        w.table_articles.selectedIndexes = MagicMock(return_value=[])
        on_article_selected(w)
        w.lbl_reader_title.setText.assert_not_called()
        w.btn_open.setEnabled.assert_not_called()

    def test_out_of_range_row_returns_early(self, qapp):
        """Row index beyond current_articles → early return, no crash."""
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
        """Article without URL → buttons disabled, no property set."""
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
        """Metadata string includes estimated reading time."""
        from gui._25_article_selection_reader_update.on_article_selected import (
            on_article_selected,
        )
        w = _make_window()
        on_article_selected(w)
        meta = w.lbl_reader_meta.setText.call_args[0][0]
        assert "min read" in meta
