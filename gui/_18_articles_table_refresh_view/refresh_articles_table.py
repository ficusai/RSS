"""Refresh the articles table with current search/category filters."""
# WHAT: Reloads articles from storage and rebuilds window.table_articles rows.
#       Also rebuilds window.combo_cat with unique categories (blockSignals guard).
# OPTIONS: window — MainWindow instance.
# DEFAULTS: Uses window.input_search text and window.combo_cat currentText.
# OUTPUT/EFFECT: Articles table + category dropdown updated.
# ERRORS/EDGE CASES: None expected.
# HOW TO TEST: refresh_articles_table(window)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem

from core.storage import load_articles
from features.feature_gui_reader_pro.implementation.reader_pro_components import get_category_color


def refresh_articles_table(window) -> None:
    """Reload and render the articles table with current filters."""
    q = window.input_search.text()
    cat = window.combo_cat.currentText()

    arts = load_articles(limit=300, category=cat if cat != "All Categories" else "", search_query=q)
    window.current_articles = arts

    all_cats = sorted({a.get("category", "General") for a in load_articles(limit=1000) if a.get("category")})
    cur = window.combo_cat.currentText()
    window.combo_cat.blockSignals(True)
    window.combo_cat.clear()
    window.combo_cat.addItem("All Categories")
    for c in all_cats:
        window.combo_cat.addItem(c)
    if cur in all_cats:
        window.combo_cat.setCurrentText(cur)
    window.combo_cat.blockSignals(False)

    window.table_articles.setRowCount(0)
    for i, a in enumerate(arts):
        window.table_articles.insertRow(i)
        title = a.get("title", "Untitled")
        src = a.get("feed_name", "-")
        cat_val = a.get("category", "General")
        dt = (a.get("published_at_iso") or a.get("scraped_at_iso") or "")[:10]

        title_item = QTableWidgetItem(title)
        src_item = QTableWidgetItem(src)
        cat_item = QTableWidgetItem(cat_val)
        dt_item = QTableWidgetItem(dt)
        cat_item.setForeground(QColor(get_category_color(cat_val)))

        for col, item in enumerate([title_item, src_item, cat_item, dt_item]):
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            window.table_articles.setItem(i, col, item)
