"""Contract-drift tests for gui/_18_articles_table_refresh_view/refresh_articles_table.py

CONTRACT SNAPSHOT
  module   : gui._18_articles_table_refresh_view.refresh_articles_table
  function : refresh_articles_table(window) -> None
  imports  : core.storage.load_articles
            , features.feature_gui_reader_pro.implementation.reader_pro_components.get_category_color
  effects  : reloads articles from storage; rebuilds combo_cat dropdown
  errors   : None expected; blockSignals guard prevents loops
"""
# WHAT: This file protects the recorded CONTRACT of
# gui/_18_articles_table_refresh_view/refresh_articles_table.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Reads the current filter values (input_search text, combo_cat category),
#   queries the article database via core.storage.load_articles(...) with
#   limit=300, category and search_query, stores the question result in
#   window.current_articles, rebuilds the articles table (4 columns: Title,
#   Source Feed, Category, Date), and rebuilds the combo_cat category dropdown
#   ("All Categories" + every unique category) using a blockSignals pair to
#   stop infinite signal loops.
# OPTIONS: window must expose table_articles, combo_cat, input_search and a
#            'current_articles' list attribute.
# DEFAULTS: category "All Categories" -> passed as "" (no filter), so the
#            source's first load_articles call is unfiltered by category.
# OUTPUT/EFFECT: current_articles set, table rows rebuilt, dropdown rebuilt.
# ERRORS/EDGE CASES: blockSignals guard prevents an infinite loop when the
#            dropdown is repopulated (fires currentIndexChanged otherwise).
# HOW TO TEST: refresh_articles_table(window); inspect table rows and dropdown.

# sys = runtime controls; plants fake PyQt6 modules and extends import path.
import sys
# inspect = reads a function's declared parameters without running it.
import inspect
# Path = readable file-system paths.
from pathlib import Path
# MagicMock = fake call-recording object; patch = swap a name temporarily.
from unittest.mock import MagicMock, patch

# pytest = the test runner.
import pytest

# Ensure offscreen platform for headless Qt rendering
# Plant fake PyQt6 packages before any real import so no screen is needed.
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

# PROJECT_ROOT: three folders up from here = the RSS project root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Put the root on Python's import search path (once).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Shared helpers from conftest.py: structural assertions + the fake WindowStub.
from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
# Import the REAL source function being guarded.
from gui._18_articles_table_refresh_view.refresh_articles_table import refresh_articles_table


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================
# Shape-of-the-code checks to catch refactor drift. The separator bars below
# are the file's original formatting and are kept verbatim.

class TestLayer1Structural:

    def test_signature(self):
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, returns None.
        assert_signature(refresh_articles_table, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        # Point at the real source file on disk.
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_18_articles_table_refresh_view" / "refresh_articles_table.py")
        # The source MUST import core.storage (its load_articles query) and
        # the reader-pro components (which provides get_category_color).
        assert_source_imports(module_path, {
            "core.storage",
            "features.feature_gui_reader_pro.implementation.reader_pro_components",
        })

    def test_callables(self):
        # The module must define EXACTLY the public function
        # "refresh_articles_table".
        import gui._18_articles_table_refresh_view.refresh_articles_table as mod
        assert_callables(mod, {"refresh_articles_table"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests replace core.storage.load_articles with a FAKE (so no real
# database/tables exist), then run the function and inspect what ended up on
# the fake window: the stored query results, the built table rows, the
# dropdown items, and the blockSignals guard behaviour.

class TestLayer2Behavioral:

    # FIXTURE_ARTICLES = a class-level shared sample dataset used by several
    # tests below. These are FAKE database rows (article dicts) so the tests
    # don't need a real RSS database:
    #   - Article One:   has a published_at_iso date, category Tech
    #   - Article Two:   has only a scraped_at_iso date, category News
    #   - Article Three: has NO usable date at all (both ISO fields empty)
    #   - Article Four:  has a published_at_iso date, category Science
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
        # Fake window: search box holds "test", category dropdown holds "Tech".
        window = WindowStub()
        window.input_search.text.return_value = "test"
        window.combo_cat.currentText.return_value = "Tech"
        # Replace load_articles inside the source module with a fake that
        # records its arguments and returns an empty list (we don't want real
        # rows for this check).
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=[]) as mock_load:
            refresh_articles_table(window)
        # The fake WAS called at least once...
        mock_load.assert_called()
        # ...now inspect the recorded arguments of every call.
        calls = mock_load.call_args_list
        # First call: the filtered category query. It must have been passed
        # limit=300 (cap), category="Tech" (from the dropdown — only "All
        # Categories" is translated to an empty string, not "Tech"), and the
        # search query "test" straight from the search box.
        assert calls[0][1].get("limit") == 300
        assert calls[0][1].get("category") == "Tech"
        assert calls[0][1].get("search_query") == "test"

    def test_current_articles_set(self):
        window = WindowStub()
        # Unfiltered: empty search box, "All Categories" selected.
        window.input_search.text.return_value = ""
        window.combo_cat.currentText.return_value = "All Categories"
        # Fake load_articles returns only the first two fixture articles.
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=self.FIXTURE_ARTICLES[:2]):
            refresh_articles_table(window)
        # The source stores the filtered query result on the window in
        # window.current_articles (the reader pane later uses this list).
        # It must be exactly the two articles the fake returned.
        assert window.current_articles == self.FIXTURE_ARTICLES[:2]

    def test_table_populated_with_four_col_rows(self):
        window = WindowStub()
        window.input_search.text.return_value = ""
        window.combo_cat.currentText.return_value = "All Categories"
        # Fake load_articles returns ALL four fixture articles.
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=self.FIXTURE_ARTICLES):
            refresh_articles_table(window)
        # One table row must be inserted per article: 4 fixture articles ->
        # the fake table must RECORD exactly 4 insertRow calls.
        assert window.table_articles.insertRow.call_count == 4

    def test_combo_cat_rebuilt_with_categories(self):
        window = WindowStub()
        window.input_search.text.return_value = ""
        window.combo_cat.currentText.return_value = "All Categories"
        with patch("gui._18_articles_table_refresh_view.refresh_articles_table.load_articles",
                   return_value=self.FIXTURE_ARTICLES):
            refresh_articles_table(window)
        # Collect every text passed to the fake category dropdown's addItem().
        add_items = [c for c in window.combo_cat.addItem.call_args_list]
        texts = [c[0][0] for c in add_items]
        # The dropdown must always start with the "show everything" option...
        assert "All Categories" in texts
        # ...and then list each distinct category found across the articles.
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
        # blockSignals(True) at the start, blockSignals(False) at the end of
        # the dropdown rebuild -> at least 2 total calls. This pair stops the
        # combo box from firing currentIndexChanged loops.
        assert window.combo_cat.blockSignals.call_count >= 2