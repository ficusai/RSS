"""Build the Feed Presets Library tab (Tab 4)."""
# WHAT: Creates the presets catalog table, category dropdown, search bar, and "Add All" button.
#       Calls load_preset_categories and refresh_presets_table at the end.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: tab_presets widget created and added to window.tabs.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: build_presets_tab(window); assert window.tabs.count() == 4
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QVBoxLayout,
    QWidget,
    QSizePolicy,      # size policy for expanding widgets
)

from gui._30_preset_categories_load_dropdown.load_preset_categories import load_preset_categories
from gui._31_presets_table_refresh_view.refresh_presets_table import refresh_presets_table


def build_presets_tab(window) -> None:
    """Build and add the Feed Presets Library tab."""
    tab_presets = QWidget()
    presets_l = QVBoxLayout(tab_presets)
    presets_l.setContentsMargins(10, 10, 10, 10)
    presets_l.setSpacing(10)

    presets_header = QHBoxLayout()
    presets_header.setSpacing(10)

    presets_title = QLabel("📚 Feed Presets Library")
    presets_title.setStyleSheet("color: #e6edf3; font-size: 16px; font-weight: bold;")

    window.preset_combo_cat = QComboBox()
    window.preset_combo_cat.setMinimumWidth(220)
    window.preset_combo_cat.currentIndexChanged.connect(window.refresh_presets_table)

    window.in_preset_search = QLineEdit()
    window.in_preset_search.setPlaceholderText("Search presets by name, URL, or category...")
    window.in_preset_search.textChanged.connect(window.refresh_presets_table)

    window.btn_add_all_presets = QPushButton("➕ Add All Presets")
    window.btn_add_all_presets.setObjectName("accent")
    window.btn_add_all_presets.clicked.connect(window.add_all_presets)

    presets_header.addWidget(presets_title)
    presets_header.addWidget(window.preset_combo_cat)
    presets_header.addWidget(window.in_preset_search, 1)
    presets_header.addWidget(window.btn_add_all_presets)
    presets_l.addLayout(presets_header)

    window.table_presets = QTableWidget()
    window.table_presets.setColumnCount(5)
    window.table_presets.setHorizontalHeaderLabels(["Name", "RSS Endpoint URL", "Category", "Status", "Actions"])
    pres_header = window.table_presets.horizontalHeader()
    pres_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
    pres_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    pres_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    pres_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    pres_header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
    window.table_presets.setColumnWidth(0, 200)
    window.table_presets.verticalHeader().setVisible(False)
    window.table_presets.verticalHeader().setDefaultSectionSize(48)
    window.table_presets.setAlternatingRowColors(True)
    window.table_presets.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    presets_l.addWidget(window.table_presets, 1)

    presets_note = QLabel(
        "Preset feeds are curated one-click subscriptions from the feature/feed-presets-library branch. "
        "Click Add to subscribe a feed, or Add All Presets to bulk-import the whole catalog."
    )
    presets_note.setWordWrap(True)
    presets_note.setStyleSheet("color: #8b949e; font-size: 14px; padding: 4px 8px;")
    presets_l.addWidget(presets_note)

    window.tabs.addTab(tab_presets, "📚 Feed Presets Library")
    tab_presets.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    load_preset_categories(window)
    refresh_presets_table(window)
