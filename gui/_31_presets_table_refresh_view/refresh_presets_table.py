"""Refresh the presets catalog table with current filter state."""
# WHAT: Rebuilds window.table_presets rows from the presets library, filtered by category/search.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: Falls back gracefully if presets library is unavailable.
# OUTPUT/EFFECT: Presets table rows updated.
# ERRORS/EDGE CASES: Presets library may not be installed.
# HOW TO TEST: refresh_presets_table(window)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QTableWidgetItem, QWidget

from features.feature_gui_reader_pro.implementation.reader_pro_components import get_category_color
from gui._32_preset_add_single_from_catalog.add_preset_feed import add_preset_feed


def refresh_presets_table(window) -> None:
    """Rebuild the presets catalog table with current filters."""
    try:
        from features.feature_feed_presets_library.implementation.feeds_presets import (
            get_presets_by_category,
            search_presets,
            feed_already_present,
        )
    except Exception:
        return

    cat = window.preset_combo_cat.currentText()
    q = window.in_preset_search.text().strip()
    presets = search_presets(q) if q else get_presets_by_category(cat)

    window.table_presets.setRowCount(0)
    row = 0
    for preset in presets:
        name = preset.get("name", "")
        url = preset.get("url", "")
        cat_val = preset.get("category", "General")
        present = feed_already_present(preset, window.feeds)

        window.table_presets.insertRow(row)

        name_item = QTableWidgetItem(name)
        name_item.setFont(QFont("", 16, QFont.Weight.Bold))
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        window.table_presets.setItem(row, 0, name_item)

        url_item = QTableWidgetItem(url)
        url_item.setForeground(QColor("#8b949e"))
        url_item.setToolTip(url)
        url_item.setFlags(url_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        window.table_presets.setItem(row, 1, url_item)

        cat_item = QTableWidgetItem(cat_val)
        cat_item.setForeground(QColor(get_category_color(cat_val)))
        cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        window.table_presets.setItem(row, 2, cat_item)

        status_item = QTableWidgetItem("Subscribed" if present else "Available")
        status_item.setForeground(QColor("#3fb950") if present else QColor("#8b949e"))
        status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        window.table_presets.setItem(row, 3, status_item)

        act_w = QWidget()
        act_l = QHBoxLayout(act_w)
        act_l.setContentsMargins(2, 2, 2, 2)
        act_l.setSpacing(6)
        add_btn = QPushButton("Add")
        add_btn.setObjectName("accent")
        add_btn.setMinimumHeight(38)
        add_btn.setEnabled(not present)
        add_btn.clicked.connect(lambda _, p=preset: add_preset_feed(window, p))
        act_l.addWidget(add_btn)
        window.table_presets.setCellWidget(row, 4, act_w)
        row += 1
