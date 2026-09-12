"""Contract-drift tests for gui/_18_articles_table_refresh_view/refresh_articles_table.py

CONTRACT SNAPSHOT
  module   : gui._18_articles_table_refresh_view.refresh_articles_table
  function : refresh_articles_table(window) -> None
  imports  : core.storage.load_articles
            , features.feature_gui_reader_pro.implementation.reader_pro_components.get_category_color
  effects  : reloads articles from storage; rebuilds combo_cat dropdown
  errors   : None expected; blockSignals guard prevents loops
"""
# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the recorded CONTRACT of
# gui/_18_articles_table_refresh_view/refresh_articles_table.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Reads the current filter values (input_search text, combo_cat category),
#   queries the article database via core.storage.load_articles(...) with
#   limit=300, category and search_query, stores the question result in
#   window.current_articles, rebuilds the articles table (4 columns: Title,
#   Source Feed, Category, Date), and rebuilds the combo_cat category dropdown
#   ("All Categories" + every unique category) using a blockSignals pair to
#   stop infinite signal loops.
#
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 — Structural: shape-of-the-code checks to catch refactor drift.
# Layer 2 — Behavioral Smoke: fake-window smoke tests that verify observable
#                              outcomes when core.storage.load_articles is
#                              replaced with a deterministic recorder.
#
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================
# Layer 1 — Structural:
#   test_signature       - exactly one param "window" (positional-or-keyword),
#                          no default, returns None.
#   test_source_imports  - module-level imports include core.storage and
#                          reader_pro_components.
#   test_callables       - module exposes ONLY the public symbol
#                          "refresh_articles_table".
# Layer 2 — Behavioral Smoke:
#   test_load_articles_called_with_filters         - verifies load_articles
#                                                    receives limit=300, the
#                                                    correct category string,
#                                                    and search_query.
#   test_current_articles_set                      - verifies window.current_
#                                                    articles receives the
#                                                    exact returned list.
#   test_table_populated_with_four_col_rows        - verifies insertRow is
#                                                    called once per article.
#   test_combo_cat_rebuilt_with_categories         - verifies the dropdown
#                                                    lists "All Categories"
#                                                    plus every unique
#                                                    category from fixtures.
#   test_combo_cat_blockSignals_guard              - verifies at least two
#                                                    blockSignals calls (the
#                                                    pair that prevents loops).
# ===========================================================================
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
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
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the source module's public shape (signature, imports,
         callable set) has not drifted from the recorded contract.
    OPTIONS: None — these are purely structural invariants.
    DEFAULTS: N/A
    OUTPUT/EFFECT: No runtime effect; raises AssertionError on drift.
    ERRORS/EDGE CASES: None — these are static invariants.
    HOW TO TEST: Run this class in isolation; all three tests must pass.
    """

    def test_signature(self):
        """WHAT: Verify refresh_articles_table accepts exactly one parameter.

        OPTIONS: None — contract is fixed at one parameter named 'window'.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts the signature is
                       (window: POSITIONAL_OR_KEYWORD, no default) -> None.
        ERRORS/EDGE CASES: If the source gains or loses parameters the test
                           fails, flagging refactor drift.
        HOW TO TEST: assert_signature(refresh_articles_table, [("window", 1, inspect.Parameter.empty)], None)
        """
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, returns None.
        assert_signature(refresh_articles_table, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verify the source file imports required modules on disk.

        OPTIONS: None — the import set is a hard contract.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts AST-parsed source contains both
                       core.storage and reader_pro_components.
        ERRORS/EDGE CASES: Renaming or removing either import causes failure.
        HOW TO TEST: assert_source_imports(module_path, {"core.storage", "features.feature_gui_reader_pro.implementation.reader_pro_components"})
        """
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
        """WHAT: Verify the module exposes exactly one public callable.

        OPTIONS: None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts dir(mod) contains only "refresh_articles_table"
                       among user-defined callables.
        ERRORS/EDGE CASES: Extra or missing callables indicate drift.
        HOW TO TEST: assert_callables(mod, {"refresh_articles_table"})
        """
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
    """Layer 2 — Behavioral smoke tests against a fake window.

    WHAT: Verifies the observable behaviour of refresh_articles_table when
         core.storage.load_articles is patched with deterministic fake data.
    OPTIONS: window must expose table_articles, combo_cat, input_search,
             and current_articles.
    DEFAULTS: category "All Categories" translates to "" (unfiltered query).
    OUTPUT/EFFECT: window.current_articles set; table rows inserted;
                   dropdown rebuilt; blockSignals pair exercised.
    ERRORS/EDGE CASES: blockSignals guard prevents infinite currentIndexChanged
                       loops during dropdown rebuild.
    HOW TO TEST: refresh_articles_table(window); inspect table rows and dropdown.
    """

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
        """WHAT: Verify load_articles is called with correct filter kwargs.

        OPTIONS: window.input_search.text() = "test"; window.combo_cat.
                 currentText() = "Tech".
        DEFAULTS: None — both inputs are explicitly set in this test.
        OUTPUT/EFFECT: Mock load_articles records a call with limit=300,
                       category="Tech", search_query="test".
        ERRORS/EDGE CASES: If the source drops a filter param or changes
                           the limit cap this assertion fails.
        HOW TO TEST: Call refresh_articles_table(window) and inspect
                     mock_load.call_args_list for the first call's kwargs.
        """
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
        """WHAT: Verify window.current_articles receives the fake result list.

        OPTIONS: window.input_search.text() = ""; window.combo_cat.
                 currentText() = "All Categories" (unfiltered).
        DEFAULTS: "All Categories" maps to category="" (no filter).
        OUTPUT/EFFECT: window.current_articles is set to the first two
                       fixture articles.
        ERRORS/EDGE CASES: If the source stores the result under a different
                           attribute name this test fails.
        HOW TO TEST: Call refresh_articles_table(window); assert
                     window.current_articles == FIXTURE_ARTICLES[:2].
        """
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
        """WHAT: Verify table_articles.insertRow is called once per article.

        OPTIONS: window.input_search.text() = ""; window.combo_cat.
                 currentText() = "All Categories".
        DEFAULTS: All four fixture articles returned from the fake.
        OUTPUT/EFFECT: table.insertRow called exactly 4 times (one per
                       fixture article).
        ERRORS/EDGE CASES: If the source skips rows or calls insertRow a
                           different number of times the assertion fails.
        HOW TO TEST: Call refresh_articles_table(window); assert
                     window.table_articles.insertRow.call_count == 4.
        """
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
        """WHAT: Verify combo_cat dropdown lists all unique categories.

        OPTIONS: window.input_search.text() = ""; window.combo_cat.
                 currentText() = "All Categories".
        DEFAULTS: "All Categories" as the first item; unique categories from
                  the article list follow.
        OUTPUT/EFFECT: combo_cat.addItem called with "All Categories",
                       "Tech", "News", and "Science".
        ERRORS/EDGE CASES: Missing a category or extra items indicate drift.
        HOW TO TEST: Collect all addItem text args and assert presence of
                     "All Categories", "Tech", "News", "Science".
        """
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
        """WHAT: Verify blockSignals is called at least twice during rebuild.

        OPTIONS: window.input_search.text() = ""; window.combo_cat.
                 currentText() = "All Categories".
        DEFAULTS: Empty article list (no real data to render).
        OUTPUT/EFFECT: combo_cat.blockSignals called >= 2 times (the guard
                       pair that prevents currentIndexChanged loops).
        ERRORS/EDGE CASES: Fewer than 2 calls means the guard was dropped,
                           risking an infinite signal loop at runtime.
        HOW TO TEST: Call refresh_articles_table(window); assert
                     window.combo_cat.blockSignals.call_count >= 2.
        """
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
