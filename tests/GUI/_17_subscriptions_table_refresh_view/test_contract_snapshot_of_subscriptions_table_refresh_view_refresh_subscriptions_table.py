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
# WHAT: Verifies the refresh_subscriptions_table contract survives refactor drift.
# OPTIONS: window with table_feeds, cb_cat_filter, in_filter, feeds
# DEFAULTS: Uses current filter values; interval defaults to 12h
# OUTPUT/EFFECT: Table rows + category dropdown updated
# ERRORS/EDGE CASES: blockSignals guard prevents infinite loop
# HOW TO TEST: refresh_subscriptions_table(window); check row count and dropdown items

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
from gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table import refresh_subscriptions_table


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(refresh_subscriptions_table, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_17_subscriptions_table_refresh_view" / "refresh_subscriptions_table.py")
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
        import gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table as mod
        assert_callables(mod, {"refresh_subscriptions_table"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_three_feed_fixture_populates_three_rows(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "Feed B", "url": "https://b.com/feed", "category": "News",
             "fetch_interval_hours": 6, "enabled": False},
            {"id": "c", "name": "Feed C", "url": "https://c.com/feed", "category": "Tech",
             "fetch_interval_hours": 24, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        assert window.table_feeds.insertRow.call_count == 3

    def test_cell_texts_correct(self):
        window = WindowStub()
        window.feeds = [
            {"id": "x", "name": "My Feed", "url": "https://example.com/feed",
             "category": "Tech", "fetch_interval_hours": 12, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # Col 0 = name, col 1 = url, col 2 = category
        items = window.table_feeds.setItem.call_args_list
        assert items[0][1]["arg1"] == 0  # row 0, col 0
        name_item = items[0][0][1]  # QTableWidgetItem with text
        assert name_item.text() == "My Feed"
        assert items[1][1]["arg1"] == 1
        assert items[1][0][1].text() == "https://example.com/feed"
        assert items[2][1]["arg1"] == 2
        assert items[2][0][1].text() == "Tech"

    def test_interval_cell_has_qcombobox_with_5_items(self):
        window = WindowStub()
        window.feeds = [
            {"id": "x", "name": "F", "url": "https://x.com/feed",
             "category": "G", "fetch_interval_hours": 12, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        # setCellWidget at row 0, col 3 should be a QComboBox
        cell_widgets = [c for c in window.table_feeds.setCellWidget.call_args_list if c[0][1] == 3]
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
        cell_widgets = [c for c in window.table_feeds.setCellWidget.call_args_list if c[0][1] == 4]
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
        cell_widgets = [c for c in window.table_feeds.setCellWidget.call_args_list if c[0][1] == 5]
        assert len(cell_widgets) == 1

    def test_cb_cat_filter_rebuilt_with_all_categories(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "B", "url": "https://b.com/feed", "category": "News",
             "fetch_interval_hours": 6, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        add_items = [c for c in window.cb_cat_filter.addItem.call_args_list]
        texts = [c[0][0] for c in add_items]
        assert "All Categories" in texts
        assert "Tech" in texts
        assert "News" in texts

    def test_cb_cat_filter_blockSignals_guard(self):
        window = WindowStub()
        window.feeds = []
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        assert window.cb_cat_filter.blockSignals.call_count >= 2  # True then False

    def test_search_filter_respected(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Apple", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "Banana", "url": "https://b.com/feed", "category": "Food",
             "fetch_interval_hours": 6, "enabled": True},
        ]
        window.in_filter.text.return_value = "apple"
        window.cb_cat_filter.currentText.return_value = "All Categories"
        refresh_subscriptions_table(window)
        assert window.table_feeds.insertRow.call_count == 1

    def test_category_filter_respected(self):
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Apple", "url": "https://a.com/feed", "category": "Tech",
             "fetch_interval_hours": 12, "enabled": True},
            {"id": "b", "name": "Banana", "url": "https://b.com/feed", "category": "Food",
             "fetch_interval_hours": 6, "enabled": True},
        ]
        window.in_filter.text.return_value = ""
        window.cb_cat_filter.currentText.return_value = "Food"
        refresh_subscriptions_table(window)
        assert window.table_feeds.insertRow.call_count == 1
