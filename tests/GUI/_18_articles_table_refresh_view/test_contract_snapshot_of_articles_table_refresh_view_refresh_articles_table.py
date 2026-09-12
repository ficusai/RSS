"""Contract-drift tests for gui/_18_articles_table_refresh_view/refresh_articles_table.py

CONTRACT SNAPSHOT
  module   : gui._18_articles_table_refresh_view.refresh_articles_table
  function : refresh_articles_table(window) -> None
  imports  : core.storage.load_articles
            , features.feature_gui_reader_pro.implementation.reader_pro_components.get_category_color
  effects  : reloads articles from storage; rebuilds combo_cat dropdown
  errors   : None expected; blockSignals guard prevents loops
"""
# WHAT: Verifies the refresh_articles_table contract survives refactor drift.
# OPTIONS: window with table_articles, combo_cat, input_search, current_articles
# DEFAULTS: Uses current filter values from UI
# OUTPUT/EFFECT: window.current_articles set; table rebuilt; combo_cat updated
# ERRORS/EDGE CASES: blockSignals guard prevents infinite loop
# HOW TO TEST: refresh_articles_table(window); verify table rows and dropdown

import sys
import inspect
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure offscreen platform for headless Qt rendering
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
from gui._18_articles_table_refresh_view.refresh_articles_table import refresh_articles_table


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(refresh_articles_table, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_18_articles_table_refresh_view" / "refresh_articles_table.py")
        assert_source_imports(module_path, {
            "core.storage",
            "features.feature_gui_reader_pro.implementation.reader_pro_components",
        })

    def test_callables(self):
        import gui._18_articles_table_refresh_view.refresh_articles_table as mod
        assert_callables(mod, {"refresh_articles_table"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    FIXTURE_ARTICLES = [
        {
            "title": "Article One",
            "feed_name": "Feed A",
            "category": "Tech",
            "published_at_iso": "2026-01-15T10:00:00Z",
        },
        {
            "title": "Article Two",
            "feed_name": "Feed B",
            "category": "News",
            "scraped_at_iso": "2026-02-20T12:00:00Z",
        },
        {
            "title": "Article Three",
            "feed_name": "Feed A",
            "category": "Tech",
            "published_at_iso": "",
            "scraped_at_iso": "",
        },
        {
            "title": "Article Four",
            "feed_name": "Feed C",
            "category": "Science",
            "published_at_iso": "2026-03-01T08:00:00Z",
        },
    ]

    def test_load_articles_called_with_filters(self):
        window = WindowStub()
        window.input_search.text.return_value = "test"
        window.combo_cat.currentText.return_value = "Tech"
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=[]) as mock_load:
            refresh_articles_table(window)
        mock_load.assert_called()
        calls = mock_load.call_args_list
        # First call: with filters
        assert calls[0][1].get("limit") == 300
        assert calls[0][1].get("category") == "Tech"
        assert calls[0][1].get("search_query") == "test"

    def test_current_articles_set(self):
        window = WindowStub()
        window.input_search.text.return_value = ""
        window.combo_cat.currentText.return_value = "All Categories"
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=self.FIXTURE_ARTICLES[:2]):
            refresh_articles_table(window)
        assert window.current_articles == self.FIXTURE_ARTICLES[:2]

    def test_table_populated_with_four_col_rows(self):
        window = WindowStub()
        window.input_search.text.return_value = ""
        window.combo_cat.currentText.return_value = "All Categories"
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=self.FIXTURE_ARTICLES):
            refresh_articles_table(window)
        assert window.table_articles.insertRow.call_count == 4

    def test_combo_cat_rebuilt_with_categories(self):
        window = WindowStub()
        window.input_search.text.return_value = ""
        window.combo_cat.currentText.return_value = "All Categories"
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=self.FIXTURE_ARTICLES):
            refresh_articles_table(window)
        add_items = [c for c in window.combo_cat.addItem.call_args_list]
        texts = [c[0][0] for c in add_items]
        assert "All Categories" in texts
        assert "Tech" in texts
        assert "News" in texts
        assert "Science" in texts

    def test_combo_cat_blockSignals_guard(self):
        window = WindowStub()
        window.input_search.text.return_value = ""
        window.combo_cat.currentText.return_value = "All Categories"
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=[]):
            refresh_articles_table(window)
        assert window.combo_cat.blockSignals.call_count >= 2
