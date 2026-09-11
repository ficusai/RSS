"""
PyQt6 Modern Dark Dashboard for RSS Feed Manager & Scraper.
Features unified 16px typography, touch-friendly tactile controls, live metadata badges,
category color coding, article reading time estimation, clipboard sharing, and diagnostics console.
"""

import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import Qt, QThread, QUrl, pyqtSignal
from PyQt6.QtGui import QColor, QDesktopServices, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.fetcher import fetch_all_feeds
from core.storage import get_stats, load_articles, save_articles

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "feeds.json"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Modern minimal high-contrast dark theme with consistent 16px visual hierarchy
STYLESHEET = """
QMainWindow { background-color: #090d16; color: #e6edf3; }
QWidget { font-family: "Segoe UI", system-ui, -apple-system, sans-serif; font-size: 16px; color: #e6edf3; }

/* Tabs */
QTabWidget::pane { border: 1px solid #21262d; border-radius: 8px; background: #0d1117; top: 0; }
QTabBar::tab {
    background: #161b22; color: #8b949e;
    border: 1px solid #21262d; border-bottom: none;
    border-top-left-radius: 8px; border-top-right-radius: 8px;
    padding: 12px 24px; font-size: 16px; font-weight: 600;
    min-height: 44px; margin-right: 4px;
}
QTabBar::tab:selected { background: #0d1117; color: #58a6ff; border-top: 3px solid #58a6ff; }
QTabBar::tab:hover { background: #1c2128; color: #c9d1d9; }

/* Cards & Containers */
QFrame#card {
    background-color: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
}

/* Input Controls */
QLineEdit {
    background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
    padding: 10px 14px; color: #e6edf3; font-size: 16px;
    min-height: 44px;
}
QLineEdit:focus { border-color: #58a6ff; background: #11161d; }
QLineEdit::placeholder { color: #6e7681; }

/* Buttons */
QPushButton {
    background: #21262d; color: #e6edf3; border: 1px solid #363b42;
    border-radius: 6px; padding: 10px 20px; font-size: 16px; font-weight: 600;
    min-height: 44px; min-width: 90px;
}
QPushButton:hover { background: #30363d; border-color: #58a6ff; color: #ffffff; }
QPushButton:pressed { background: #1f6feb; color: #ffffff; }
QPushButton:disabled { background: #161b22; color: #484f58; border-color: #21262d; }

QPushButton#accent {
    background: #1a5a2e; color: #3fb950; border: 1px solid #238636;
    min-height: 44px; font-weight: 600;
}
QPushButton#accent:hover { background: #216e39; color: #56d364; border-color: #3fb950; }

QPushButton#primary_blue {
    background: #1f6feb; color: #ffffff; border: 1px solid #388bfd;
    min-height: 44px; font-weight: 600;
}
QPushButton#primary_blue:hover { background: #388bfd; border-color: #58a6ff; }

QPushButton#danger {
    background: #3d1818; color: #f85149; border: 1px solid #da3633;
    min-height: 44px; font-weight: 600;
}
QPushButton#danger:hover { background: #4e2020; color: #ff7b72; border-color: #f85149; }

/* Tables */
QTableWidget {
    background: #0d1117; alternate-background-color: #121720;
    border: 1px solid #21262d; border-radius: 8px;
    color: #e6edf3; gridline-color: #21262d; font-size: 16px;
    selection-background-color: #1f6feb44; selection-color: #ffffff;
}
QHeaderView::section {
    background: #161b22; color: #8b949e; border: none;
    border-bottom: 2px solid #21262d; padding: 10px 14px;
    font-weight: 700; font-size: 16px; min-height: 46px;
}
QTableWidget::item { padding: 10px 14px; min-height: 46px; }

/* Text Editors */
QTextEdit {
    background: #0d1117; border: 1px solid #21262d; border-radius: 8px;
    color: #e6edf3; font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    font-size: 16px; padding: 14px; line-height: 1.6;
    min-height: 120px;
}

QTextEdit#log_console {
    background: #010409; border: 1px solid #21262d; border-radius: 6px;
    color: #7ee787; font-family: "Cascadia Code", "Fira Code", monospace;
    font-size: 15px; padding: 12px; line-height: 1.4;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #21262d; border-radius: 6px; text-align: center;
    background: #161b22; height: 8px;
}
QProgressBar::chunk { background: #1f6feb; border-radius: 4px; }

/* Dropdowns */
QComboBox {
    background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
    padding: 10px 14px; color: #e6edf3; font-size: 16px;
    min-height: 44px; max-height: 48px;
}
QComboBox::drop-down { border: none; width: 32px; }
QComboBox QAbstractItemView {
    background: #161b22; color: #e6edf3; border: 1px solid #30363d;
    selection-background-color: #1f6feb44; font-size: 16px;
    min-height: 44px; padding: 6px;
}
QComboBox QAbstractItemView::item {
    min-height: 44px; padding: 10px;
}

/* Scrollbars */
QScrollBar:vertical { background: #0d1117; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #30363d; border-radius: 5px; min-height: 28px; }
QScrollBar::handle:vertical:hover { background: #484f58; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }

QScrollBar:horizontal { background: #0d1117; height: 10px; border-radius: 5px; }
QScrollBar::handle:horizontal { background: #30363d; border-radius: 5px; min-width: 28px; }
QScrollBar::handle:horizontal:hover { background: #484f58; }

/* Checkboxes */
QCheckBox { spacing: 10px; color: #e6edf3; font-size: 16px; min-height: 44px; padding: 4px; }
QCheckBox::indicator { width: 22px; height: 22px; border: 2px solid #30363d; border-radius: 5px; background: #0d1117; }
QCheckBox::indicator:checked { background: #1f6feb; border-color: #1f6feb; }
"""


class ScrapeThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int, int, list)

    def __init__(self, feeds, parent=None):
        super().__init__(parent)
        self.feeds = copy.deepcopy(feeds)

    def run(self):
        try:
            self.log_signal.emit("Initializing parallel feed scrape process...")
            articles, errors = fetch_all_feeds(self.feeds, progress_callback=self.log_signal.emit)
            new, total = save_articles(articles)
            self.finished_signal.emit(new, total, errors)
        except Exception as e:
            self.log_signal.emit(f"Scrape Error: {e}")
            self.finished_signal.emit(0, 0, [{"feed_name": "System", "error": str(e)}])


def get_category_color(category_name: str) -> str:
    """Returns hex color code badge for a category."""
    cat = (category_name or "").lower()
    if "tech" in cat:
        return "#58a6ff"
    elif "finan" in cat or "econ" in cat or "bank" in cat:
        return "#3fb950"
    elif "news" in cat or "world" in cat:
        return "#d29922"
    return "#a371f7"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSS Feed Tracker & Scraping Dashboard")
        self.resize(1280, 840)
        self.setMinimumSize(980, 700)

        self.config_path = CONFIG_PATH
        self.feeds = []
        self.scrape_thread = None
        self.current_articles = []

        logo_path = ASSETS_DIR / "ficus.png"
        if logo_path.exists():
            self.setWindowIcon(QIcon(str(logo_path)))

        self.setStyleSheet(STYLESHEET)
        self._build_ui()
        self.load_feeds()
        self.refresh()
        self._log("RSS Engine initialized and ready.")

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Minimal Top Header Bar
        hdr = QFrame()
        hdr.setObjectName("card")
        hdr_layout = QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(16, 10, 16, 10)

        brand_box = QHBoxLayout()
        brand_box.setSpacing(10)
        title_badge = QLabel("⚡ RSS ENGINE")
        title_badge.setFont(QFont("", 16, QFont.Weight.Bold))
        title_badge.setStyleSheet(
            "color: #ffffff; background: #1f6feb; padding: 4px 12px; border-radius: 6px; font-weight: bold;"
        )
        subtitle_lbl = QLabel("Feed Tracker & Scraper Pro")
        subtitle_lbl.setFont(QFont("", 16, QFont.Weight.Bold))
        subtitle_lbl.setStyleSheet("color: #e6edf3; font-weight: bold;")
        brand_box.addWidget(title_badge)
        brand_box.addWidget(subtitle_lbl)

        hdr_layout.addLayout(brand_box)
        hdr_layout.addStretch()

        # Stats Badges
        self.lbl_articles_stat = QLabel("0 Articles")
        self.lbl_articles_stat.setStyleSheet(
            "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 4px 14px; color: #58a6ff; font-weight: 600;"
        )
        self.lbl_feeds_stat = QLabel("0 Feeds")
        self.lbl_feeds_stat.setStyleSheet(
            "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 4px 14px; color: #a371f7; font-weight: 600;"
        )

        hdr_layout.addWidget(self.lbl_articles_stat)
        hdr_layout.addWidget(self.lbl_feeds_stat)
        hdr_layout.addSpacing(10)

        self.btn_sync = QPushButton("🔄 Sync All Feeds")
        self.btn_sync.setObjectName("accent")
        self.btn_sync.clicked.connect(self.start_scrape)
        hdr_layout.addWidget(self.btn_sync)

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        layout.addWidget(self.progress, 0, Qt.AlignmentFlag.AlignRight)

        layout.addWidget(hdr)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # -------------------------------------------------------------
        # Tab 1: Articles Explorer (Reader Dashboard)
        # -------------------------------------------------------------
        tab_art = QWidget()
        art_l = QVBoxLayout(tab_art)
        art_l.setContentsMargins(10, 10, 10, 10)
        art_l.setSpacing(10)

        # Filter & Search Action Bar
        art_filter = QHBoxLayout()
        art_filter.setSpacing(10)

        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("🔍 Search by title, text body, author, or feed name...")
        self.input_search.textChanged.connect(self.refresh_articles)

        self.combo_cat = QComboBox()
        self.combo_cat.addItem("All Categories")
        self.combo_cat.setMinimumWidth(220)
        self.combo_cat.currentIndexChanged.connect(self.refresh_articles)

        self.btn_refresh_view = QPushButton("🔄 Refresh View")
        self.btn_refresh_view.clicked.connect(self.refresh)

        art_filter.addWidget(self.input_search, 1)
        art_filter.addWidget(self.combo_cat)
        art_filter.addWidget(self.btn_refresh_view)
        art_l.addLayout(art_filter)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Table of Contents (Articles List Table)
        self.table_articles = QTableWidget()
        self.table_articles.setColumnCount(4)
        self.table_articles.setHorizontalHeaderLabels(["Article Title", "Source Feed", "Category", "Date"])
        self.table_articles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_articles.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.verticalHeader().setVisible(False)
        self.table_articles.verticalHeader().setDefaultSectionSize(50)
        self.table_articles.setAlternatingRowColors(True)
        self.table_articles.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_articles.itemSelectionChanged.connect(self.on_article_sel)

        # Article Reader Card Pane
        reader_box = QFrame()
        reader_box.setObjectName("card")
        reader_l = QVBoxLayout(reader_box)
        reader_l.setContentsMargins(14, 14, 14, 14)
        reader_l.setSpacing(10)

        self.lbl_reader_title = QLabel("Select an article to view details")
        self.lbl_reader_title.setWordWrap(True)
        self.lbl_reader_title.setStyleSheet("color: #58a6ff; font-size: 18px; font-weight: bold;")

        self.lbl_reader_meta = QLabel("")
        self.lbl_reader_meta.setStyleSheet("color: #8b949e; font-size: 15px; font-weight: 500;")

        self.txt_reader = QTextEdit()
        self.txt_reader.setReadOnly(True)

        reader_btn_box = QHBoxLayout()
        reader_btn_box.setSpacing(10)

        self.btn_copy_link = QPushButton("📋 Copy Link")
        self.btn_copy_link.setEnabled(False)
        self.btn_copy_link.clicked.connect(self.copy_article_link)

        self.btn_open = QPushButton("🌐 Open in Browser")
        self.btn_open.setObjectName("primary_blue")
        self.btn_open.setEnabled(False)
        self.btn_open.clicked.connect(self.open_browser)

        reader_btn_box.addWidget(self.btn_copy_link)
        reader_btn_box.addStretch()
        reader_btn_box.addWidget(self.btn_open)

        reader_l.addWidget(self.lbl_reader_title)
        reader_l.addWidget(self.lbl_reader_meta)
        reader_l.addWidget(self.txt_reader, 1)
        reader_l.addLayout(reader_btn_box)

        splitter.addWidget(self.table_articles)
        splitter.addWidget(reader_box)
        splitter.setSizes([720, 480])
        art_l.addWidget(splitter, 1)
        self.tabs.addTab(tab_art, "Articles Explorer")

        # -------------------------------------------------------------
        # Tab 2: Feeds & Operations Hub (Reworked Minimal & Accurate)
        # -------------------------------------------------------------
        tab_feed = QWidget()
        feed_l = QVBoxLayout(tab_feed)
        feed_l.setContentsMargins(10, 10, 10, 10)
        feed_l.setSpacing(10)

        # Minimal Add Feed Bar Card
        add_box = QFrame()
        add_box.setObjectName("card")
        add_v = QVBoxLayout(add_box)
        add_v.setContentsMargins(12, 12, 12, 12)
        add_v.setSpacing(8)

        add_top = QHBoxLayout()
        add_top.setSpacing(10)

        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("Feed Name (e.g. TechCrunch)")
        self.in_url = QLineEdit()
        self.in_url.setPlaceholderText("RSS URL (e.g. https://techcrunch.com/feed/)")
        self.in_cat = QLineEdit()
        self.in_cat.setText("General")
        self.in_cat.setPlaceholderText("Category")
        self.in_cat.setMaximumWidth(180)

        self.cb_freq = QComboBox()
        self.cb_freq.addItems(["1h", "3h", "6h", "12h", "24h"])
        self.cb_freq.setCurrentIndex(3)
        self.cb_freq.setMaximumWidth(110)

        self.btn_add = QPushButton("➕ Add Feed")
        self.btn_add.setObjectName("accent")
        self.btn_add.clicked.connect(self.add_feed)

        add_top.addWidget(self.in_name, 1)
        add_top.addWidget(self.in_url, 2)
        add_top.addWidget(self.in_cat)
        add_top.addWidget(self.cb_freq)
        add_top.addWidget(self.btn_add)
        add_v.addLayout(add_top)

        feed_l.addWidget(add_box)

        # Minimal Filter Header & Table Section
        catalog_header = QHBoxLayout()
        catalog_header.setSpacing(10)

        catalog_title = QLabel("📡 Subscriptions Catalog")
        catalog_title.setStyleSheet("color: #e6edf3; font-size: 16px; font-weight: bold;")

        self.in_filter = QLineEdit()
        self.in_filter.setPlaceholderText("Filter feeds by name or URL...")
        self.in_filter.textChanged.connect(self.refresh_table)

        self.cb_cat_filter = QComboBox()
        self.cb_cat_filter.addItem("All Categories")
        self.cb_cat_filter.setMinimumWidth(180)
        self.cb_cat_filter.currentIndexChanged.connect(self.refresh_table)

        catalog_header.addWidget(catalog_title)
        catalog_header.addStretch()
        catalog_header.addWidget(self.in_filter, 1)
        catalog_header.addWidget(self.cb_cat_filter)
        feed_l.addLayout(catalog_header)

        # Reworked Table with 6 Accurate Columns & Proportional Sizing
        self.table_feeds = QTableWidget()
        self.table_feeds.setColumnCount(6)
        self.table_feeds.setHorizontalHeaderLabels(["Name", "RSS Endpoint URL", "Category", "Interval", "Active", "Actions"])
        
        # Accurate column sizing
        header = self.table_feeds.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table_feeds.setColumnWidth(0, 190)
        self.table_feeds.verticalHeader().setVisible(False)
        self.table_feeds.verticalHeader().setDefaultSectionSize(48)
        self.table_feeds.setAlternatingRowColors(True)
        feed_l.addWidget(self.table_feeds, 1)

        # Minimal Operations & Console Section
        ops_box = QFrame()
        ops_box.setObjectName("card")
        ops_l = QVBoxLayout(ops_box)
        ops_l.setContentsMargins(12, 10, 12, 10)
        ops_l.setSpacing(8)

        sched_l = QHBoxLayout()
        sched_l.setSpacing(10)

        ops_title = QLabel("⚙️ Operations Log")
        ops_title.setStyleSheet("color: #8b949e; font-size: 15px; font-weight: bold;")

        self.btn_clear = QPushButton("🧹 Clear Log")
        self.btn_clear.clicked.connect(self.clear_log)

        sched_l.addWidget(ops_title)
        sched_l.addStretch()
        sched_l.addWidget(self.btn_clear)
        ops_l.addLayout(sched_l)

        self.log_box = QTextEdit()
        self.log_box.setObjectName("log_console")
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(120)
        ops_l.addWidget(self.log_box)

        feed_l.addWidget(ops_box)

        self.tabs.addTab(tab_feed, "Feeds & Operations Hub")

        # -------------------------------------------------------------
        # Tab 3: Feed Presets Library
        # -------------------------------------------------------------
        tab_presets = QWidget()
        presets_l = QVBoxLayout(tab_presets)
        presets_l.setContentsMargins(10, 10, 10, 10)
        presets_l.setSpacing(10)

        presets_header = QHBoxLayout()
        presets_header.setSpacing(10)

        presets_title = QLabel("📚 Feed Presets Library")
        presets_title.setStyleSheet("color: #e6edf3; font-size: 16px; font-weight: bold;")

        self.preset_combo_cat = QComboBox()
        self.preset_combo_cat.setMinimumWidth(220)
        self.preset_combo_cat.currentIndexChanged.connect(self.refresh_presets_table)

        self.in_preset_search = QLineEdit()
        self.in_preset_search.setPlaceholderText("Search presets by name, URL, or category...")
        self.in_preset_search.textChanged.connect(self.refresh_presets_table)

        self.btn_add_all_presets = QPushButton("➕ Add All Presets")
        self.btn_add_all_presets.setObjectName("accent")
        self.btn_add_all_presets.clicked.connect(self.add_all_presets)

        presets_header.addWidget(presets_title)
        presets_header.addWidget(self.preset_combo_cat)
        presets_header.addWidget(self.in_preset_search, 1)
        presets_header.addWidget(self.btn_add_all_presets)
        presets_l.addLayout(presets_header)

        self.table_presets = QTableWidget()
        self.table_presets.setColumnCount(5)
        self.table_presets.setHorizontalHeaderLabels(["Name", "RSS Endpoint URL", "Category", "Status", "Actions"])
        pres_header = self.table_presets.horizontalHeader()
        pres_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        pres_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        pres_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        pres_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        pres_header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table_presets.setColumnWidth(0, 200)
        self.table_presets.verticalHeader().setVisible(False)
        self.table_presets.verticalHeader().setDefaultSectionSize(48)
        self.table_presets.setAlternatingRowColors(True)
        self.table_presets.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        presets_l.addWidget(self.table_presets, 1)

        presets_note = QLabel(
            "Preset feeds are curated one-click subscriptions from the feature/feed-presets-library branch. "
            "Click Add to subscribe a feed, or Add All Presets to bulk-import the whole catalog."
        )
        presets_note.setWordWrap(True)
        presets_note.setStyleSheet("color: #8b949e; font-size: 14px; padding: 4px 8px;")
        presets_l.addWidget(presets_note)

        self.tabs.addTab(tab_presets, "Feed Presets Library")
        self.load_preset_categories()
        self.refresh_presets_table()

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.append(f"[{ts}] {msg}")
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

    def clear_log(self):
        self.log_box.clear()

    def load_feeds(self):
        if not self.config_path.exists():
            self.feeds = []
            return
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.feeds = data.get("feeds", data) if isinstance(data, dict) else data
        except Exception:
            self.feeds = []

    def save_feeds(self):
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"feeds": self.feeds}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self._log(f"Save error: {e}")

    def refresh(self):
        self.refresh_table()
        self.refresh_articles()
        self.update_stats()

    def update_stats(self):
        try:
            stats = get_stats()
            arts = stats.get("total_articles", 0)
            total = len(self.feeds)
            active = sum(1 for f in self.feeds if f.get("enabled", True))

            self.lbl_articles_stat.setText(f"📰 {arts} Articles")
            self.lbl_feeds_stat.setText(f"📡 {active}/{total} Feeds Active")
        except Exception:
            pass

    def refresh_table(self):
        self.table_feeds.setRowCount(0)
        search = self.in_filter.text().lower()
        cat_f = self.cb_cat_filter.currentText()

        cats = sorted({f.get("category", "General") for f in self.feeds})
        cur = self.cb_cat_filter.currentText()
        self.cb_cat_filter.blockSignals(True)
        self.cb_cat_filter.clear()
        self.cb_cat_filter.addItem("All Categories")
        for c in cats:
            self.cb_cat_filter.addItem(c)
        if cur in cats:
            self.cb_cat_filter.setCurrentText(cur)
        self.cb_cat_filter.blockSignals(False)

        freq_map = {1: 0, 3: 1, 6: 2, 12: 3, 24: 4}
        row = 0
        for feed in self.feeds:
            name = feed.get("name", "")
            cat = feed.get("category", "General")
            url = feed.get("url", "")
            fid = feed.get("id") or re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"f{row}"
            feed["id"] = fid

            if search and not any(search in v.lower() for v in [name, cat, url]):
                continue
            if cat_f != "All Categories" and cat != cat_f:
                continue

            self.table_feeds.insertRow(row)

            # Column 0: Feed Name
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("", 16, QFont.Weight.Bold))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_feeds.setItem(row, 0, name_item)

            # Column 1: RSS Endpoint URL
            url_item = QTableWidgetItem(url)
            url_item.setForeground(QColor("#8b949e"))
            url_item.setToolTip(url)
            url_item.setFlags(url_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_feeds.setItem(row, 1, url_item)

            # Column 2: Category Badging
            cat_item = QTableWidgetItem(cat)
            cat_item.setForeground(QColor(get_category_color(cat)))
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_feeds.setItem(row, 2, cat_item)

            # Column 3: Interval Dropdown
            freq_cb = QComboBox()
            freq_cb.addItems(["1h", "3h", "6h", "12h", "24h"])
            h = feed.get("fetch_interval_hours", 12)
            freq_cb.setCurrentIndex(freq_map.get(h, 3))
            freq_cb.currentIndexChanged.connect(lambda i, fid=fid: self.set_freq(fid, [1, 3, 6, 12, 24][i]))
            freq_cb.setMinimumHeight(38)
            freq_cb.setMaximumWidth(90)
            self.table_feeds.setCellWidget(row, 3, freq_cb)

            # Column 4: Active Checkbox
            cb_w = QWidget()
            cb_l = QHBoxLayout(cb_w)
            cb_l.setContentsMargins(0, 0, 0, 0)
            cb_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cb = QCheckBox()
            cb.setChecked(feed.get("enabled", True))
            cb.toggled.connect(lambda on, fid=fid: self.toggle(fid, on))
            cb.setMinimumHeight(38)
            cb_l.addWidget(cb)
            self.table_feeds.setCellWidget(row, 4, cb_w)

            # Column 5: Action Buttons (Ping & Delete)
            act_w = QWidget()
            act_l = QHBoxLayout(act_w)
            act_l.setContentsMargins(2, 2, 2, 2)
            act_l.setSpacing(6)
            pbtn = QPushButton("Ping")
            pbtn.setObjectName("accent")
            pbtn.setMinimumHeight(38)
            pbtn.clicked.connect(lambda _, fid=fid: self.ping(fid))

            dbtn = QPushButton("Delete")
            dbtn.setObjectName("danger")
            dbtn.setMinimumHeight(38)
            dbtn.clicked.connect(lambda _, fid=fid: self.delete_feed(fid))

            act_l.addWidget(pbtn)
            act_l.addWidget(dbtn)
            self.table_feeds.setCellWidget(row, 5, act_w)
            row += 1

    def refresh_articles(self):
        q = self.input_search.text()
        cat = self.combo_cat.currentText()

        arts = load_articles(limit=300, category=cat if cat != "All Categories" else "", search_query=q)
        self.current_articles = arts

        all_cats = sorted({a.get("category", "General") for a in load_articles(limit=1000) if a.get("category")})
        cur = self.combo_cat.currentText()
        self.combo_cat.blockSignals(True)
        self.combo_cat.clear()
        self.combo_cat.addItem("All Categories")
        for c in all_cats:
            self.combo_cat.addItem(c)
        if cur in all_cats:
            self.combo_cat.setCurrentText(cur)
        self.combo_cat.blockSignals(False)

        self.table_articles.setRowCount(0)
        for i, a in enumerate(arts):
            self.table_articles.insertRow(i)
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
                self.table_articles.setItem(i, col, item)

    def on_article_sel(self):
        rows = self.table_articles.selectedIndexes()
        if not rows:
            return
        row_idx = rows[0].row()
        if row_idx >= len(self.current_articles):
            return
        a = self.current_articles[row_idx]

        self.lbl_reader_title.setText(a.get("title", "Untitled"))
        meta = []
        if a.get("feed_name"):
            meta.append(f"📡 {a['feed_name']}")
        if a.get("author"):
            meta.append(f"👤 {a['author']}")
        if a.get("published_at_iso"):
            meta.append(f"📅 {a['published_at_iso'][:10]}")

        preview_text = a.get("preview") or ""
        full_text = a.get("full_text_clean") or a.get("text_clean") or a.get("summary_raw") or "No article content available."

        if preview_text and preview_text != full_text and len(full_text) > len(preview_text) + 50:
            body = f"📌 PREVIEW SUMMARY:\n{preview_text}\n\n{'=' * 45}\n📖 FULL ARTICLE CONTENT:\n{full_text}"
        else:
            body = full_text

        word_count = len(body.split())
        read_time = max(1, round(word_count / 200))
        meta.append(f"⏱️ ~{read_time} min read")

        self.lbl_reader_meta.setText("   •   ".join(meta))
        self.txt_reader.setPlainText(body)

        url = a.get("url")
        self.btn_open.setEnabled(bool(url))
        self.btn_copy_link.setEnabled(bool(url))
        if url:
            self.btn_open.setProperty("url", url)
            self.btn_copy_link.setProperty("url", url)

    def open_browser(self):
        url = self.btn_open.property("url")
        if url:
            QDesktopServices.openUrl(QUrl(url))

    def copy_article_link(self):
        url = self.btn_copy_link.property("url")
        if url:
            QApplication.clipboard().setText(url)
            self._log(f"Copied URL to clipboard: {url}")
            QMessageBox.information(self, "Link Copied", "Article URL copied to clipboard!")

    def set_freq(self, fid, hours):
        for f in self.feeds:
            if f.get("id") == fid:
                f["fetch_interval_hours"] = hours
                self.save_feeds()
                break

    def toggle(self, fid, on):
        for f in self.feeds:
            if f.get("id") == fid:
                f["enabled"] = on
                self.save_feeds()
                self.update_stats()
                break

    def ping(self, fid):
        target = next((f for f in self.feeds if f.get("id") == fid), None)
        if not target:
            return
        if self.scrape_thread and self.scrape_thread.isRunning():
            return
        self._log(f"Pinging RSS feed endpoint: {target['name']} ({target['url']})")
        self._run_scrape([target])

    def add_feed(self):
        name = self.in_name.text().strip()
        url = self.in_url.text().strip()
        cat = self.in_cat.text().strip() or "General"
        h = [1, 3, 6, 12, 24][self.cb_freq.currentIndex()]

        if not name or not url:
            QMessageBox.warning(self, "Missing Fields", "Both Feed Name and Feed URL are required.")
            return
        if not url.startswith("http"):
            url = "https://" + url

        fid = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"f{len(self.feeds)}"
        self.feeds.append({"id": fid, "name": name, "url": url, "category": cat, "fetch_interval_hours": h, "enabled": True})
        self.save_feeds()
        self.refresh()
        self._log(f"Successfully subscribed to feed: {name}")
        self.in_name.clear()
        self.in_url.clear()

    def delete_feed(self, fid):
        for i, f in enumerate(self.feeds):
            if f.get("id") == fid:
                removed_name = f.get('name')
                self.feeds.pop(i)
                self.save_feeds()
                self.refresh()
                self._log(f"Unsubscribed feed: {removed_name}")
                return

    def load_preset_categories(self):
        try:
            from features.feature_feed_presets_library.implementation.feeds_presets import (
                get_preset_categories,
            )
            cats = ["All Categories"] + get_preset_categories()
        except Exception:
            cats = ["All Categories"]

        cur = self.preset_combo_cat.currentText()
        self.preset_combo_cat.blockSignals(True)
        self.preset_combo_cat.clear()
        self.preset_combo_cat.addItems(cats)
        if cur in cats:
            self.preset_combo_cat.setCurrentText(cur)
        self.preset_combo_cat.blockSignals(False)

    def refresh_presets_table(self):
        try:
            from features.feature_feed_presets_library.implementation.feeds_presets import (
                get_presets_by_category,
                search_presets,
                feed_already_present,
            )
        except Exception:
            return

        cat = self.preset_combo_cat.currentText()
        q = self.in_preset_search.text().strip()
        presets = search_presets(q) if q else get_presets_by_category(cat)

        self.table_presets.setRowCount(0)
        row = 0
        for preset in presets:
            name = preset.get("name", "")
            url = preset.get("url", "")
            cat_val = preset.get("category", "General")
            present = feed_already_present(preset, self.feeds)

            self.table_presets.insertRow(row)

            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("", 16, QFont.Weight.Bold))
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_presets.setItem(row, 0, name_item)

            url_item = QTableWidgetItem(url)
            url_item.setForeground(QColor("#8b949e"))
            url_item.setToolTip(url)
            url_item.setFlags(url_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_presets.setItem(row, 1, url_item)

            cat_item = QTableWidgetItem(cat_val)
            cat_item.setForeground(QColor(get_category_color(cat_val)))
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_presets.setItem(row, 2, cat_item)

            status_item = QTableWidgetItem("Subscribed" if present else "Available")
            status_item.setForeground(QColor("#3fb950") if present else QColor("#8b949e"))
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_presets.setItem(row, 3, status_item)

            act_w = QWidget()
            act_l = QHBoxLayout(act_w)
            act_l.setContentsMargins(2, 2, 2, 2)
            act_l.setSpacing(6)
            add_btn = QPushButton("Add")
            add_btn.setObjectName("accent")
            add_btn.setMinimumHeight(38)
            add_btn.setEnabled(not present)
            add_btn.clicked.connect(lambda _, p=preset: self.add_preset_feed(p))
            act_l.addWidget(add_btn)
            self.table_presets.setCellWidget(row, 4, act_w)
            row += 1

    def add_preset_feed(self, preset):
        from features.feature_feed_presets_library.implementation.feeds_presets import (
            feed_already_present,
        )
        if feed_already_present(preset, self.feeds):
            self._log(f"Preset already subscribed: {preset.get('name')}")
            return
        name = (preset.get("name") or "").strip()
        url = (preset.get("url") or "").strip()
        cat = (preset.get("category") or "General").strip()
        if not name or not url:
            return
        fid = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"f{len(self.feeds)}"
        self.feeds.append(
            {"id": fid, "name": name, "url": url, "category": cat, "fetch_interval_hours": 12, "enabled": True}
        )
        self.save_feeds()
        self.refresh()
        self.refresh_presets_table()
        self._log(f"Subscribed preset feed: {name}")

    def add_all_presets(self):
        from features.feature_feed_presets_library.implementation.feeds_presets import (
            get_preset_feeds,
            feed_already_present,
        )
        added = 0
        for preset in get_preset_feeds():
            if feed_already_present(preset, self.feeds):
                continue
            name = (preset.get("name") or "").strip()
            url = (preset.get("url") or "").strip()
            cat = (preset.get("category") or "General").strip()
            if not name or not url:
                continue
            fid = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"f{len(self.feeds)}"
            self.feeds.append(
                {"id": fid, "name": name, "url": url, "category": cat, "fetch_interval_hours": 12, "enabled": True}
            )
            added += 1
        if added:
            self.save_feeds()
            self.refresh()
            self.refresh_presets_table()
        self._log(f"Preset import complete: {added} new feed(s) added.")
        QMessageBox.information(self, "Presets Imported", f"Added {added} preset feed(s) to your subscriptions.")

    def start_scrape(self):
        if self.scrape_thread and self.scrape_thread.isRunning():
            return
        enabled = [f for f in self.feeds if f.get("enabled")]
        if not enabled:
            QMessageBox.information(self, "No Active Subscriptions", "Please enable at least one feed to sync.")
            return
        self._run_scrape(self.feeds)

    def _run_scrape(self, feeds):
        self.btn_sync.setEnabled(False)
        self.btn_sync.setText("⏳ Syncing...")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.scrape_thread = ScrapeThread(feeds)
        self.scrape_thread.log_signal.connect(self._log)
        self.scrape_thread.finished_signal.connect(self.on_done)
        self.scrape_thread.start()

    def on_done(self, new, total, errors):
        self.btn_sync.setEnabled(True)
        self.btn_sync.setText("🔄 Sync All Feeds")
        self.progress.setVisible(False)
        self._log(f"Scrape job complete: +{new} new article(s) added. Total database count: {total}.")
        if errors:
            self._log(f"Encountered {len(errors)} feed fetching issue(s).")
        self.update_stats()
        self.refresh_articles()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
