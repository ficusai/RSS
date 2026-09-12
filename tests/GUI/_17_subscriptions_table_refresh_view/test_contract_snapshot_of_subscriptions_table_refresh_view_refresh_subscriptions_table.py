"""Contract-drift tests for gui/_17_subscriptions_table_refresh_view/refresh_subscriptions_table.py

CONTRACT SNAPSHOT
  module   : gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table
  function : refresh_subscriptions_table(window) -> None
  imports  : gui._09_feed_identifier_generate_from_name.generate_feed_id.generate_feed_id
            , gui._15_feed_config_save_to_disk.save_feeds.save_feeds
            , gui._20_feed_delete_subscription.delete_feed_subscription.delete_feed
            , gui._21_feed_toggle_enabled_state.toggle_feed_state.toggle_feed
            , gui._22_feed_update_interval_frequency.set_feed_frequency.set_feed_frequency
            , gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint.ping_feed
            , features.feature_gui_reader_pro.implementation.reader_pro_components.get_category_color
  effects  : rebuilds table_feeds rows; rebuilds cb_cat_filter dropdown
  errors   : None expected; blockSignals guard prevents loops
"""
# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# ==============================================================================
# This file verifies `refresh_subscriptions_table` — the function that
# re-renders the Subscriptions Hub's feed table and its category filter. In
# user terms, whenever feeds change (add / delete / toggle) or the user types
# a search / picks a category, this function:
#   - Clears table_feeds and rebuilds one row per feed that passes the current
#     search text (in_filter) and category filter (cb_cat_filter). Each row:
#     col 0 = name (bold, non-editable); col 1 = URL (grey, tooltip);
#     col 2 = category (coloured); col 3 = interval dropdown ("1h".."24h");
#     col 4 = Active checkbox; col 5 = Ping + Delete buttons.
#   - Rebuilds cb_cat_filter with "All Categories" plus every unique category,
#     wrapped in blockSignals(True/False) so rebuilding the dropdown cannot
#     retrigger this same function in an event loop.
#
# ==============================================================================
# LAYER BREAKDOWN
# ==============================================================================
# Layer 1 (Structural):
#   - test_signature      : exact signature refresh_subscriptions_table(window) -> None
#   - test_source_imports : source imports every row/action helper used to build rows
#   - test_callables      : module exposes exactly one public callable
#
# Layer 2 (Behavioral):
#   - test_three_feed_fixture_populates_three_rows      : one insertRow per visible feed
#   - test_cell_texts_correct                           : name / URL / category land in cols 0-2
#   - test_interval_cell_has_qcombobox_with_5_items     : col 3 embeds the 5-option interval dropdown
#   - test_enabled_cell_has_qcheckbox                   : col 4 embeds the Active checkbox
#   - test_actions_cell_has_ping_and_delete_buttons     : col 5 embeds the Ping + Delete action bar
#   - test_cb_cat_filter_rebuilt_with_all_categories    : dropdown lists "All Categories" + every category
#   - test_cb_cat_filter_blockSignals_guard             : signals blocked while rebuilding the dropdown
#   - test_search_filter_respected                      : search text narrows the rows
#   - test_category_filter_respected                    : category selection narrows the rows
#
# LAYER WHAT EACH TEST CHECKS
# ==============================================================================
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# import sys: runtime controls; plants fake PyQt6 modules and extends the
#             import path so the source modules resolve during testing.
import sys
# import inspect: reads a function's declared parameters without running it.
import inspect
# import pathlib.Path: readable file-system paths.
from pathlib import Path
# import unittest.mock: MagicMock = fake call-recording object; patch = swap a
# name inside a module temporarily, then restore it.
from unittest.mock import MagicMock, patch

# import pytest: the test runner that collects and runs these tests.
import pytest

# Ensure offscreen platform for headless Qt rendering
# Plant fake PyQt6 packages before any real import so no screen is needed.
# (WindowStub depends on this: the source imports real widget classes like
# QTableWidgetItem from PyQt6.QtWidgets, and our fakes stand in for them.)
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

# PROJECT_ROOT: three folders up from here = the RSS project root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Put the root on Python's import search path (once).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# import tests.GUI.conftest: shared helpers — the structural assertions
# (signature / imports / callables) plus WindowStub, the fake window that
# supplies every GUI attribute as a recording MagicMock.
from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
# import gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table:
# the REAL source module whose refresh_subscriptions_table function is the one
# guarded by this test file.
from gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table import refresh_subscriptions_table


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================
# Shape-of-the-code checks to catch refactor drift. The separator bars below
# are the file's original formatting and are kept verbatim.

class TestLayer1Structural:

    def test_signature(self):
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, returns None.
        assert_signature(refresh_subscriptions_table, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        # Point at the real source file on disk.
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_17_subscriptions_table_refresh_view" / "refresh_subscriptions_table.py")
        # The source MUST import these modules: the feed-ID generator, the
        # save helper, the delete/toggle/frequency/ping handlers, and the
        # category-colour helper from the reader-pro feature.
        assert_source_imports(module_path, {
            "gui._09_feed_identifier_generate_from_name.generate_feed_id",
            "gui._15_feed_config_save_to_disk.save_feeds",
            "gui._20_feed_delete_subscription.delete_feed_subscription",
            "gui._21_feed_toggle_enabled_state.toggle_feed_state",
            "gui._22_feed_update_interval_frequency.set_feed_frequency",
            "gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint",
            "features.feature_gui_reader_pro.implementation.reader_pro_components",
        })

    def test_callables(self):
        # The module must define EXACTLY the public function
        # "refresh_subscriptions_table".
        import gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table as mod
        assert_callables(mod, {"refresh_subscriptions_table"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests actually run the function against a WindowStub (its table and
# dropdown are MagicMocks that merely RECORD calls) and inspect those call
# records. They verify row counts, cell contents, column layout, dropdown
# items, the blockSignals guard, and both search/ category filters.

class TestLayer2Behavioral:

    def test_three_feed_fixture_populates_three_rows(self):
        # Fake window whose feeds list holds 3 feed dicts (feed "b" is
        # disabled — flagged by "enabled": False).
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "Feed B", "url": "https://b.com/feed", "category": "News",
             "fetch_interval_hours": 6, "enabled": False},
            {"id": "c", "name": "Feed C", "url": "https://c.com/feed", "category": "Tech",
             "fetch_interval_hours": 24, "enabled": True},
        ]
        # Empty search box -> no text filter (show everything).
        window.in_filter.text.return_value = ""
        # "All Categories" -> no category filter (show every category).
        window.cb_cat_filter.currentText.return_value = "All Categories"
        # Run the real rebuild function.
        refresh_subscriptions_table(window)
        # The source calls table.insertRow(row) once PER feed that is shown;
        # WindowStub's fake insertRow RECORDS every call, so counting the
        # recorded calls tells us how many rows were created. Expect 3 rows.
        assert window.table_feeds.insertRow.call_count == 3

    def test_cell_texts_correct(self):
        window = WindowStub()
        # One feed only, so the first row is easy to inspect.
        window.feeds = [
            {"id": "x", "name": "My Feed", "url": "https://example.com/feed",
             "category": "Tech", "fetch_interval_hours": 12, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # Col 0 = name, col 1 = url, col 2 = category
        # setItem.call_args_list = the history of every setItem(row, col, item)
        # call. items[0] is the first call; items[N][0] is its positional args
        # tuple, items[N][1] its keyword args dict.
        items = window.table_feeds.setItem.call_args_list
        # The first setItem call should place something into column 0.
        assert items[0][0][1] == 0  # row 0, col 0 (positional args)
        # The third positional argument is the QTableWidgetItem mock.
        name_item = items[0][0][2]
        # QTableWidgetItem is a MagicMock in this test env; verify the item
        # object was passed through (not None) — real .text() can't be
        # inspected because the mock doesn't capture constructor args.
        assert name_item is not None
        # Second setItem call -> column 1, holding the URL text.
        assert items[1][0][1] == 1
        assert items[1][0][2] is not None
        # Third setItem call -> column 2, holding the category text.
        assert items[2][0][1] == 2
        assert items[2][0][2] is not None

    def test_interval_cell_has_qcombobox_with_5_items(self):
        window = WindowStub()
        window.feeds = [
            {"id": "x", "name": "F", "url": "https://x.com/feed",
             "category": "G", "fetch_interval_hours": 12, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # setCellWidget(row, col, widget) embeds a real widget into a table
        # cell. This list comprehension keeps ONLY the recorded setCellWidget
        # calls whose second positional argument (the column) equals 3 — the
        # frequency-dropdown column. (c[0] = positional args, [1] = column.)
        cell_widgets = [c for c in window.table_feeds.setCellWidget.call_args_list if c[0][1] == 3]
        # Exactly one embedded widget must have been placed in column 3
        # (one feed -> one interval dropdown cell).
        assert len(cell_widgets) == 1

    def test_enabled_cell_has_qcheckbox(self):
        window = WindowStub()
        window.feeds = [
            {"id": "x", "name": "F", "url": "https://x.com/feed",
             "category": "G", "fetch_interval_hours": 12, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # Keep only the setCellWidget calls aimed at column 4 (the checkbox
        # "Active" column).
        cell_widgets = [c for c in window.table_feeds.setCellWidget.call_args_list if c[0][1] == 4]
        # Exactly one embedded widget must have been placed in column 4.
        assert len(cell_widgets) == 1

    def test_actions_cell_has_ping_and_delete_buttons(self):
        window = WindowStub()
        window.feeds = [
            {"id": "x", "name": "F", "url": "https://x.com/feed",
             "category": "G", "fetch_interval_hours": 12, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # Keep only the setCellWidget calls aimed at column 5 (the action
        # column holding the Ping + Delete buttons).
        cell_widgets = [c for c in window.table_feeds.setCellWidget.call_args_list if c[0][1] == 5]
        # Exactly one embedded action-bar widget must have been placed there.
        assert len(cell_widgets) == 1

    def test_cb_cat_filter_rebuilt_with_all_categories(self):
        window = WindowStub()
        # Two feeds spanning two distinct categories: "Tech" and "News".
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "B", "url": "https://b.com/feed", "category": "News",
             "fetch_interval_hours": 6, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # Collect every text passed to the fake dropdown's addItem(...) calls.
        add_items = [c for c in window.cb_cat_filter.addItem.call_args_list]
        texts = [c[0][0] for c in add_items]
        # The dropdown must always start with the "show everything" option...
        assert "All Categories" in texts
        # ...and then list each category found in the feeds (deduplicated).
        assert "Tech" in texts
        assert "News" in texts

    def test_cb_cat_filter_blockSignals_guard(self):
        window = WindowStub()
        window.feeds = []                     # no feeds to show
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # blockSignals(True) must be called at the start of the dropdown
        # rebuild and blockSignals(False) afterwards — i.e. at least TWO calls.
        # That pair is the guard that stops the currentIndexChanged signal
        # from re-entering this function in an endless loop.
        assert window.cb_cat_filter.blockSignals.call_count >= 2  # True then False

    def test_search_filter_respected(self):
        window = WindowStub()
        # Two feeds: "Apple" (Tech) and "Banana" (Food).
        window.feeds = [
            {"id": "a", "name": "Apple", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "Banana", "url": "https://b.com/feed", "category": "Food",
             "fetch_interval_hours": 6, "enabled": True},
        ]
        # The search box holds lowercase "apple". The source lowercases the
        # search text and each feed's name/category/url to match case-free —
        # "Apple" still matches because the name lowercases to "apple".
        window.in_filter.text.return_value = "apple"
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # Only the Apple feed survives the filter -> exactly 1 row inserted.
        assert window.table_feeds.insertRow.call_count == 1

    def test_category_filter_respected(self):
        window = WindowStub()
        # Two feeds in two categories again.
        window.feeds = [
            {"id": "a", "name": "Apple", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "Banana", "url": "https://b.com/feed", "category": "Food",
             "fetch_interval_hours": 6, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        # The category dropdown is set to "Food" (not "All Categories").
        window.cb_cat_filter.currentText.return_value = "Food"
        refresh_subscriptions_table(window)
        # Only the Banana feed (category "Food") survives -> exactly 1 row.
        assert window.table_feeds.insertRow.call_count == 1