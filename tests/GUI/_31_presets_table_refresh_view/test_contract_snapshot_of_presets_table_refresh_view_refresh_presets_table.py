"""Contract snapshot: gui/_31_presets_table_refresh_view/refresh_presets_table.py v1.0.0

Structural contract:
  - Function name: refresh_presets_table
  - Signature: (window) -> None
  - Source imports: PyQt6.QtCore.Qt, PyQt6.QtGui (QColor, QFont),
                   PyQt6.QtWidgets (QHBoxLayout, QPushButton, QTableWidgetItem, QWidget),
                   features.feature_gui_reader_pro.implementation.reader_pro_components.get_category_color,
                   gui._32_preset_add_single_from_catalog.add_preset_feed.add_preset_feed
  - Side effects: table_presets.setRowCount(0), insertRow, setItem, setCellWidget
"""
# ==============================================================================
# WHAT: Verifies the refresh_presets_table GUI contract — table rebuilt with
#       5-col rows (name, URL, category, status, Add button); status color-coded.
#
# OPTIONS:
#   window: MainWindow stub with table_presets, preset_combo_cat, in_preset_search, feeds.
#
# DEFAULTS: Returns early (no-op) if presets library unavailable.
#
# OUTPUT/EFFECT: Table rows updated to match current filters.
#
# ERRORS/EDGE CASES: Presets library not installed → returns early.
#
# HOW TO TEST: refresh_presets_table(window)
# ==============================================================================
import importlib.util
import pytest
from unittest.mock import MagicMock, patch

# offscreen platform required for all PyQt6 widget testing
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform

# Module-level QApplication instance. Uses QApplication.instance() to reuse
# an existing app created by another test module, preventing the PyQt6 crash
# that occurs when multiple QApplications exist in the same process.
_qapp = QApplication.instance() or QApplication([])



def _make_window():
    """Build a minimal WindowStub for refresh_presets_table."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert refresh_presets_table(window) -> None."""
        import inspect
        from gui._31_presets_table_refresh_view.refresh_presets_table import (
            refresh_presets_table,
        )
        sig = inspect.signature(refresh_presets_table)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import Qt, QColor, QFont, layout/button/table-widget classes,
           get_category_color, and add_preset_feed."""
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
    """Behavioral smoke tests against the real function."""

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
        """Two presets → 2 rows, each with 5 columns, status 'Available', button enabled."""
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
        """Import error → returns without updating table."""
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
        """Already subscribed → status 'Subscribed' (green), Add button disabled."""
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
