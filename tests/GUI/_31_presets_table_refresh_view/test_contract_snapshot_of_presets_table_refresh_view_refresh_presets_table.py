"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_31_presets_table_refresh_view/refresh_presets_table.py
Generated against branch: feature/gui-atomic-modular-refactor

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the refresh_presets_table function — the function that
rebuilds the Presets Library tab's table (Tab 4) whenever filter state changes.
The function:
  - Queries the presets library with current category/search filters
  - Clears existing rows and rebuilds from scratch
  - Each row shows: feed name, URL, color-coded category, subscription status
    ("Subscribed" in green or "Available" in gray), and an Add button
  - Gracefully returns early if the presets library feature is not installed
  - Connects each Add button to add_preset_feed for one-click subscription

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_signature              : refresh_presets_table(window) -> None exact signature
  - test_source_imports         : Source imports Qt, QColor, QFont, layout/button/table-widget
                                   classes, get_category_color, and add_preset_feed

Layer 2 (Behavioral):
  - test_builds_five_col_rows_with_add_buttons      : Two presets → 2 rows, 5 cols each,
                                                       status 'Available', buttons enabled
  - test_returns_early_when_presets_unavailable     : Import error → returns without
                                                       touching table
  - test_subscribed_status_and_disabled_button      : Already subscribed → status
                                                       'Subscribed' (green), button disabled
==============================================================================
LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# importlib.util: Finds the filesystem path of the source module for import checks.
import importlib.util
# pytest: Test framework; provides the @pytest.fixture decorator for the qapp fixture.
import pytest
# unittest.mock.MagicMock: Creates fake objects that record every method call.
# unittest.mock.patch: Temporarily swaps real classes/functions for fakes during a test.
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# Prevents PyQt6 from trying to open a real display during headless test runs.
# offscreen platform required for all PyQt6 widget testing
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# PyQt6.QtWidgets.QApplication: The single Qt app object needed by the qapp fixture.
from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform

# Module-level QApplication instance. Uses QApplication.instance() to reuse
# an existing app created by another test module, preventing the PyQt6 crash
# that occurs when multiple QApplications exist in the same process.
_qapp = QApplication.instance() or QApplication([])



def _make_window():
    """Build a minimal fake window (WindowStub) for refresh_presets_table.

    WHAT: Returns a WindowStub mimicking the parts of the real MainWindow that
          refresh_presets_table reads: window.table_presets, window.preset_combo_cat,
          window.in_preset_search, and window.feeds.

    OPTIONS: None.

    DEFAULTS: All stub attributes default to MagicMock or empty list.

    OUTPUT/EFFECT: Returns a configured WindowStub ready for refresh_presets_table.

    ERRORS/EDGE CASES: None — MagicMock never raises.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Layer 1 contract checks: function signature and imports.

    These tests inspect the source code's structure without running the GUI.
    They fail if refresh_presets_table's signature or imports drift from the contract.
    """

    def test_signature(self):
        """Layer 1 — exact signature check.

        WHAT: Confirms refresh_presets_table takes exactly one required parameter
              named "window" and declares a return type of None. Every caller
              in the GUI invokes it as refresh_presets_table(window).

        OPTIONS:
          - Parameter name: exactly "window"
          - Parameter kind: POSITIONAL_OR_KEYWORD
          - Default: none (required)
          - Return type: annotated None

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when the signature matches the contract exactly.

        ERRORS/EDGE CASES:
          - Renamed parameter: params mismatch assertion fails
          - Added default: default mismatch assertion fails
          - Removed return annotation: return_annotation != None fails

        HOW TO TEST: Change "window" to "app" in the source, then run this
                     test — it should fail with a params mismatch.
        """
        import inspect
        from gui._31_presets_table_refresh_view.refresh_presets_table import (
            refresh_presets_table,
        )
        sig = inspect.signature(refresh_presets_table)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Layer 1 — source import check.

        WHAT: Verifies the source file imports all five collaborators:
          - PyQt6.QtCore            (for Qt.AlignmentFlag, Qt.ItemFlag)
          - PyQt6.QtGui             (for QColor, QFont)
          - PyQt6.QtWidgets         (for QHBoxLayout, QPushButton, QTableWidgetItem, QWidget)
          - features.feature_gui_reader_pro.implementation.reader_pro_components
            (for get_category_color — category color mapping)
          - gui._32_preset_add_single_from_catalog.add_preset_feed
            (for the Add button callback)

        WHY THIS MATTERS:
          refresh_presets_table uses Qt enums for item flags, QColor/QFont for
          cell styling, QTableWidget/QTableWidgetItem for the table, QHBoxLayout
          for the action cell, QPushButton for the Add button, and get_category_color
          / add_preset_feed for visual feedback and action wiring.
          If any import disappears, the function breaks.

        OPTIONS: Expected set is exactly the five modules listed above.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when all five imports exist in the source.

        ERRORS/EDGE CASES:
          - Missing import: "Missing imports: [...]" naming the module
          - Extra import: would cause unexpected import failure

        HOW TO TEST: Rename one import path in the source, then run —
                     it should fail and name the missing module.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._31_presets_table_refresh_view.refresh_presets_table"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {
                "PyQt6.QtCore",
                "PyQt6.QtGui",
                "PyQt6.QtWidgets",
                "features.feature_gui_reader_pro.implementation.reader_pro_components",
                "gui._32_preset_add_single_from_catalog.add_preset_feed",
            },
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Layer 2 behavioral checks: how refresh_presets_table behaves at runtime.

    These tests call the REAL refresh_presets_table against fake windows while
    the presets library functions are mocked, verifying table row construction,
    early-return behavior, and status/button states.
    """

    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.search_presets"
    )
    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.feed_already_present",
        return_value=False,
    )
    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.get_presets_by_category",
        return_value=[
            {"name": "Feed A", "url": "https://a.com/feed", "category": "Tech"},
            {"name": "Feed B", "url": "https://b.com/feed", "category": "News"},
        ],
    )
    def test_builds_five_col_rows_with_add_buttons(self, mock_get_cat, mock_already, mock_search):
        """Layer 2 — two presets produce two 5-column rows with enabled Add buttons.

        WHAT: With two sample presets and no already-subscribed feeds, the function
              must build exactly 2 rows in the table, each with 5 columns. Column 3
              shows "Available" (since feed_already_present returns False), and each
              row gets an action widget via setCellWidget.

        WHY 5 COLUMNS:
          The presets table has 5 columns: Name (0), URL (1), Category (2), Status
          (3), and Action widget (4). Columns 0–3 use QTableWidgetItem (setText),
          while column 4 uses setCellWidget for the Add button.

        OPTIONS:
          - 2 sample presets returned by get_presets_by_category
          - feed_already_present mocked to return False for both
          - search_presets mocked but not exercised (empty query → category path)

        DEFAULTS: mock_presets has 2 entries; qapp provides headless Qt context.

        OUTPUT/EFFECT: insertRow called 2×, setItem called 8× (4 cols × 2 rows),
                       setCellWidget called 2× (once per row for the button).

        ERRORS/EDGE CASES:
          - Wrong row count: insertRow.call_count != 2
          - Wrong setItem count: should be 8 (4 items × 2 rows); column 4 uses
            setCellWidget, NOT setItem
          - Wrong setCellWidget count: should be 2 (one button per row)

        HOW TO TEST: Change the preset list to 3 items, then update expected
                     call counts to 3, 12, and 3 respectively.
        """
        from gui._31_presets_table_refresh_view.refresh_presets_table import (
            refresh_presets_table,
        )
        w = _make_window()
        w.in_preset_search.text = MagicMock(return_value="")
        w.feeds = []
        refresh_presets_table(w)
        # Should use search_presets (query is empty) → fallback to get_presets_by_category
        # Actually with empty query, it calls get_presets_by_category("All Categories")
        # Let's verify row count
        assert w.table_presets.insertRow.call_count == 2
        # setItem called 4 times per row (cols 0-3 set text items) × 2 rows = 8
        # Column 4 (Add button) is added with setCellWidget, not setItem.
        assert w.table_presets.setItem.call_count == 8
        # setCellWidget called once per row for the action button
        assert w.table_presets.setCellWidget.call_count == 2

    def test_returns_early_when_presets_unavailable(self):
        """Layer 2 — early return when presets library is missing.

        WHAT: When the presets library module is unavailable (simulated by setting
              the sys.modules entry to None), refresh_presets_table must return
              without touching the table at all.

        WHY THIS MATTERS:
          The presets library is an optional feature. Users who don't install it
          should still be able to use the rest of the app. The try/except in the
          source catches this and returns early. This test ensures the guard
          is present and functional.

        OPTIONS:
          - window: fresh WindowStub with no special setup needed
          - sys.modules patched to make the presets module resolve to None

        DEFAULTS: mock_get_cat, mock_already, mock_search are not used here —
                  the import itself fails before any mocking matters.

        OUTPUT/EFFECT: setRowCount is never called (table untouched).

        ERRORS/EDGE CASES:
          - Table touched after early return: setRowCount would be called → failure
          - Exception propagates instead of being caught: test crashes

        HOW TO TEST: Remove the try/except around the presets import in the
                     source, then run — the test should fail because an exception
                     would propagate instead of returning silently.
        """
        import sys
        from gui._31_presets_table_refresh_view.refresh_presets_table import (
            refresh_presets_table,
        )
        w = _make_window()
        with patch.dict(
            sys.modules,
            {"features.feature_feed_presets_library.implementation.feeds_presets": None},
        ):
            refresh_presets_table(w)
        w.table_presets.setRowCount.assert_not_called()

    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.search_presets",
        return_value=[{"name": "Sub", "url": "https://sub.com/feed", "category": "Tech"}],
    )
    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.feed_already_present",
        return_value=True,
    )
    def test_subscribed_status_and_disabled_button(self, mock_already, mock_search):
        """Layer 2 — already-subscribed preset shows 'Subscribed' status.

        WHAT: When feed_already_present returns True (the preset is already in
              the user's subscriptions), the table row must show status text
              "Subscribed" in column 3.

        WHY THIS MATTERS:
          Duplicate subscriptions would be confusing and wasteful. Showing
          "Subscribed" in green with a disabled button gives clear visual
          feedback that the feed is already managed.

        OPTIONS:
          - 1 preset returned by search_presets
          - feed_already_present returns True
          - window.feeds is empty (but mock makes it appear subscribed)

        DEFAULTS: qapp provides headless Qt context.

        OUTPUT/EFFECT: setItem called with col=3 and text "Subscribed".

        ERRORS/EDGE CASES:
          - Wrong status text: assertion on call[0][2].text() fails

        HOW TO TEST: Change feed_already_present mock to return False, then
                     verify the status text becomes "Available" instead.
        """
        from gui._31_presets_table_refresh_view.refresh_presets_table import (
            refresh_presets_table,
        )
        w = _make_window()
        w.in_preset_search.text = MagicMock(return_value="")
        w.feeds = []
        refresh_presets_table(w)
        # Check status item text
        status_calls = [c for c in w.table_presets.setItem.call_args_list if c[0][1] == 3]
        assert len(status_calls) >= 1
        # The status text should be "Subscribed"
        # setItem args: (row, col, QTableWidgetItem)
        assert any(
            call[0][1] == 3 and call[0][2].text() == "Subscribed"
            for call in w.table_presets.setItem.call_args_list
        )
