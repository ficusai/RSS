"""Refresh the subscriptions table and rebuild its category dropdown."""
# WHAT: Rebuilds window.table_feeds rows from window.feeds, filtered by search/category.
#       Also rebuilds window.cb_cat_filter with unique categories (blockSignals guard).
# OPTIONS: window — MainWindow instance.
# DEFAULTS: Uses window.in_filter text and window.cb_cat_filter currentText as filters.
# OUTPUT/EFFECT: Table rows + category dropdown updated.
# ERRORS/EDGE CASES: None expected.
# HOW TO TEST: refresh_subscriptions_table(window)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QComboBox, QCheckBox, QHBoxLayout, QPushButton, QTableWidgetItem, QWidget

from features.feature_gui_reader_pro.implementation.reader_pro_components import get_category_color
from gui._09_feed_identifier_generate_from_name.generate_feed_id import generate_feed_id
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds
from gui._20_feed_delete_subscription.delete_feed_subscription import delete_feed
from gui._21_feed_toggle_enabled_state.toggle_feed_state import toggle_feed
from gui._22_feed_update_interval_frequency.set_feed_frequency import set_feed_frequency
from gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint import ping_feed


def refresh_subscriptions_table(window) -> None:
    """Rebuild the subscriptions table with current filter state."""
    window.table_feeds.setRowCount(0)
    search = window.in_filter.text().lower()
    cat_f = window.cb_cat_filter.currentText()

    cats = sorted({f.get("category", "General") for f in window.feeds})
    cur = window.cb_cat_filter.currentText()
    window.cb_cat_filter.blockSignals(True)
    window.cb_cat_filter.clear()
    window.cb_cat_filter.addItem("All Categories")
    for c in cats:
        window.cb_cat_filter.addItem(c)
    if cur in cats:
        window.cb_cat_filter.setCurrentText(cur)
    window.cb_cat_filter.blockSignals(False)

    freq_map = {1: 0, 3: 1, 6: 2, 12: 3, 24: 4}
    row = 0
    for feed in window.feeds:
        name = feed.get("name", "")
        cat = feed.get("category", "General")
        url = feed.get("url", "")
        fid = feed.get("id") or generate_feed_id(name, row)
        feed["id"] = fid

        if search and not any(search in v.lower() for v in [name, cat, url]):
            continue
        if cat_f != "All Categories" and cat != cat_f:
            continue

        window.table_feeds.insertRow(row)

        name_item = QTableWidgetItem(name)
        name_item.setFont(QFont("", 16, QFont.Weight.Bold))
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        window.table_feeds.setItem(row, 0, name_item)

        url_item = QTableWidgetItem(url)
        url_item.setForeground(QColor("#8b949e"))
        url_item.setToolTip(url)
        url_item.setFlags(url_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        window.table_feeds.setItem(row, 1, url_item)

        cat_item = QTableWidgetItem(cat)
        cat_item.setForeground(QColor(get_category_color(cat)))
        cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        window.table_feeds.setItem(row, 2, cat_item)

        freq_cb = QComboBox()
        freq_cb.addItems(["1h", "3h", "6h", "12h", "24h"])
        h = feed.get("fetch_interval_hours", 12)
        freq_cb.setCurrentIndex(freq_map.get(h, 3))
        freq_cb.currentIndexChanged.connect(lambda i, fid=fid: set_feed_frequency(window, fid, [1, 3, 6, 12, 24][i]))
        freq_cb.setMinimumHeight(38)
        freq_cb.setMaximumWidth(90)
        window.table_feeds.setCellWidget(row, 3, freq_cb)

        cb_w = QWidget()
        cb_l = QHBoxLayout(cb_w)
        cb_l.setContentsMargins(0, 0, 0, 0)
        cb_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cb = QCheckBox()
        cb.setChecked(feed.get("enabled", True))
        cb.toggled.connect(lambda on, fid=fid: toggle_feed(window, fid, on))
        cb.setMinimumHeight(38)
        cb_l.addWidget(cb)
        window.table_feeds.setCellWidget(row, 4, cb_w)

        act_w = QWidget()
        act_l = QHBoxLayout(act_w)
        act_l.setContentsMargins(2, 2, 2, 2)
        act_l.setSpacing(6)
        pbtn = QPushButton("Ping")
        pbtn.setObjectName("accent")
        pbtn.setMinimumHeight(38)
        pbtn.clicked.connect(lambda _, fid=fid: ping_feed(window, fid))

        dbtn = QPushButton("Delete")
        dbtn.setObjectName("danger")
        dbtn.setMinimumHeight(38)
        dbtn.clicked.connect(lambda _, fid=fid: delete_feed(window, fid))

        act_l.addWidget(pbtn)
        act_l.addWidget(dbtn)
        window.table_feeds.setCellWidget(row, 5, act_w)
        row += 1
