"""
PyQt6 Main Window and GUI components for RSS Feed Manager & Scraper.
Features a clean, modern Deep Slate design with simplified 2-option navigation.
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
    QGroupBox,
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
from core.scheduler import get_timer_status, install_systemd_timer
from core.storage import get_stats, load_articles, save_articles

CONFIG_PATH = Path("/home/ficus-pro/Documents/RSS/config/feeds.json")
ASSETS_DIR = Path("/home/ficus-pro/Documents/RSS/assets")

# Deep Slate Modern Theme QSS
STYLESHEET = """
QMainWindow {
    background-color: #0f172a;
    color: #f8fafc;
}
QWidget {
    font-family: "Segoe UI", "Ubuntu", "Inter", sans-serif;
    color: #f8fafc;
}
QTabWidget::pane {
    border: 1px solid #334155;
    border-radius: 8px;
    background-color: #0f172a;
    top: -1px;
}
QTabBar::tab {
    background-color: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 22px;
    font-weight: bold;
    font-size: 13px;
    margin-right: 6px;
}
QTabBar::tab:selected {
    background-color: #0f172a;
    color: #38bdf8;
    border-bottom: 2px solid #38bdf8;
}
QTabBar::tab:hover {
    background-color: #334155;
    color: #f8fafc;
}
QFrame.card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
}
QGroupBox {
    font-weight: bold;
    font-size: 13px;
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 14px;
    background-color: #1e293b;
    color: #38bdf8;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}
QLineEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 12px;
    color: #f8fafc;
    font-size: 13px;
}
QLineEdit:focus {
    border: 1px solid #38bdf8;
}
QPushButton {
    background-color: #38bdf8;
    color: #0f172a;
    font-weight: bold;
    font-size: 12px;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #7dd3fc;
}
QPushButton:pressed {
    background-color: #0284c7;
}
QPushButton:disabled {
    background-color: #334155;
    color: #64748b;
}
QPushButton#dangerBtn {
    background-color: #f87171;
    color: #0f172a;
    padding: 5px 12px;
    font-size: 11px;
}
QPushButton#dangerBtn:hover {
    background-color: #fca5a5;
}
QPushButton#accentBtn {
    background-color: #34d399;
    color: #0f172a;
    padding: 5px 12px;
    font-size: 11px;
}
QPushButton#accentBtn:hover {
    background-color: #6ee7b7;
}
QPushButton#secondaryBtn {
    background-color: #334155;
    color: #f8fafc;
    font-size: 12px;
}
QPushButton#secondaryBtn:hover {
    background-color: #475569;
}
QTableWidget {
    background-color: #0f172a;
    border: 1px solid #334155;
    gridline-color: #1e293b;
    border-radius: 6px;
    color: #f8fafc;
    selection-background-color: #334155;
    selection-color: #f8fafc;
}
QHeaderView::section {
    background-color: #1e293b;
    color: #38bdf8;
    padding: 8px;
    font-weight: bold;
    border: none;
    border-bottom: 1px solid #334155;
}
QTextEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    font-family: "Cascadia Code", "Consolas", "Monospace", monospace;
    font-size: 12px;
}
QProgressBar {
    border: 1px solid #334155;
    border-radius: 6px;
    text-align: center;
    background-color: #1e293b;
    color: #f8fafc;
}
QProgressBar::chunk {
    background-color: #38bdf8;
    border-radius: 5px;
}
QComboBox {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    color: #f8fafc;
    font-size: 12px;
}
QComboBox QAbstractItemView {
    background-color: #1e293b;
    color: #f8fafc;
    selection-background-color: #334155;
    border: 1px solid #334155;
}
QScrollBar:vertical, QScrollBar:horizontal {
    background-color: #0f172a;
    width: 10px;
    height: 10px;
    border: none;
    border-radius: 4px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background-color: #334155;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:hover {
    background-color: #475569;
}
QScrollBar::add-line, QScrollBar::sub-line {
    width: 0px;
    height: 0px;
}
"""

PRESET_FEEDS = [
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"},
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss", "category": "Tech News"},
    {"name": "Federal Reserve Press", "url": "https://www.federalreserve.gov/feeds/press_all.xml", "category": "Finance"},
    {"name": "BBC News - World", "url": "http://feeds.bbci.co.uk/news/rss.xml", "category": "World News"},
    {"name": "Ars Technica", "url": "http://feeds.arstechnica.com/arstechnica/index", "category": "Technology"},
]


class ScrapeThread(QThread):
    """Background worker thread for non-blocking RSS scraping."""

    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int, int, list)  # (new_articles, total_articles, errors)

    def __init__(self, feeds: List[Dict[str, Any]], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.feeds = copy.deepcopy(feeds)

    def run(self) -> None:
        try:
            self.log_signal.emit("Starting background feed scraping worker...")
            articles, errors = fetch_all_feeds(self.feeds)
            self.log_signal.emit(f"Fetch completed. Processing {len(articles)} raw article(s)...")
            new_count, total_count = save_articles(articles)
            self.finished_signal.emit(new_count, total_count, errors)
        except Exception as e:
            self.log_signal.emit(f"Critical error during feed scraping: {e}")
            self.finished_signal.emit(0, 0, [{"feed_name": "System", "error": str(e)}])


class MainWindow(QMainWindow):
    """Main application window for RSS Feed Manager & Scraper."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RSS Reader & Scraper")
        self.resize(1100, 780)

        self.config_path = CONFIG_PATH
        self.feeds: List[Dict[str, Any]] = []
        self.scrape_thread: Optional[ScrapeThread] = None
        self.current_articles: List[Dict[str, Any]] = []

        logo_path = ASSETS_DIR / "ficus.png"
        if logo_path.exists():
            self.setWindowIcon(QIcon(str(logo_path)))

        self.setStyleSheet(STYLESHEET)
        self._init_ui()
        self.load_feeds()
        self.update_table()
        self.update_stats()
        self.refresh_articles_view()
        self.log("Application started. Ready.")

    def _init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # 1. Main Header Dashboard Card
        header_card = QFrame()
        header_card.setProperty("class", "card")
        header_card.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 8px;")
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(16, 12, 16, 12)

        # Logo & App Title Container
        title_box = QHBoxLayout()
        title_box.setSpacing(12)

        logo_path = ASSETS_DIR / "ficus.png"
        if logo_path.exists():
            lbl_logo = QLabel()
            pix = QPixmap(str(logo_path))
            lbl_logo.setPixmap(pix.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            title_box.addWidget(lbl_logo)

        text_title_box = QVBoxLayout()
        text_title_box.setSpacing(2)
        title_label = QLabel("RSS Reader & Scraper")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #38bdf8;")

        subtitle_label = QLabel("Automated Feed Aggregator & Background Scheduler")
        subtitle_label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        text_title_box.addWidget(title_label)
        text_title_box.addWidget(subtitle_label)

        title_box.addLayout(text_title_box)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        # Stats Cards Layout
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        self.lbl_stat_articles = QLabel("0")
        self.card_articles = self._create_stat_card("Total Articles", self.lbl_stat_articles, "#818cf8")
        stats_layout.addWidget(self.card_articles)

        self.lbl_stat_feeds = QLabel("0")
        self.card_feeds = self._create_stat_card("Active Feeds", self.lbl_stat_feeds, "#38bdf8")
        stats_layout.addWidget(self.card_feeds)

        self.lbl_stat_timer = QLabel("Checking...")
        self.card_timer = self._create_stat_card("Auto-Sync Status", self.lbl_stat_timer, "#34d399")
        stats_layout.addWidget(self.card_timer)

        header_layout.addLayout(stats_layout)

        # Quick Sync Button & Progress Bar in Header
        sync_container = QVBoxLayout()
        sync_container.setSpacing(4)
        self.btn_scrape = QPushButton("⚡ Sync Now")
        self.btn_scrape.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_scrape.clicked.connect(self.start_scraping)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)

        sync_container.addWidget(self.btn_scrape)
        sync_container.addWidget(self.progress_bar)

        header_layout.addLayout(sync_container)
        main_layout.addWidget(header_card)

        # 2. Main Tabbed Workspace (2 Main Options)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # ----------------------------------------------------
        # OPTION 1: 📰 Articles Library & Reader (Default Home)
        # ----------------------------------------------------
        tab_articles = QWidget()
        tab_articles_layout = QVBoxLayout(tab_articles)
        tab_articles_layout.setContentsMargins(10, 12, 10, 10)
        tab_articles_layout.setSpacing(10)

        # Search & Filter Toolbar
        art_toolbar = QFrame()
        art_toolbar.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 8px;")
        art_toolbar_layout = QHBoxLayout(art_toolbar)
        art_toolbar_layout.setContentsMargins(10, 8, 10, 8)
        art_toolbar_layout.setSpacing(8)

        self.input_art_search = QLineEdit()
        self.input_art_search.setPlaceholderText("🔍 Search articles by keyword, title, author...")
        self.input_art_search.textChanged.connect(self.refresh_articles_view)

        self.combo_art_cat = QComboBox()
        self.combo_art_cat.addItem("All Categories")
        self.combo_art_cat.currentIndexChanged.connect(self.refresh_articles_view)

        self.btn_refresh_arts = QPushButton("🔄 Refresh")
        self.btn_refresh_arts.setObjectName("secondaryBtn")
        self.btn_refresh_arts.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh_arts.clicked.connect(self.refresh_articles_view)

        art_toolbar_layout.addWidget(self.input_art_search, 4)
        art_toolbar_layout.addWidget(self.combo_art_cat, 2)
        art_toolbar_layout.addWidget(self.btn_refresh_arts, 1)

        tab_articles_layout.addWidget(art_toolbar)

        # Splitter: Left Article List | Right Reader Preview
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Table
        self.table_articles = QTableWidget()
        self.table_articles.setColumnCount(4)
        self.table_articles.setHorizontalHeaderLabels(["Title", "Feed Source", "Category", "Date"])
        self.table_articles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_articles.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table_articles.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        self.table_articles.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        self.table_articles.setAlternatingRowColors(True)
        self.table_articles.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_articles.itemSelectionChanged.connect(self._on_article_selected)

        splitter.addWidget(self.table_articles)

        # Right Reader Preview Box
        reader_box = QGroupBox("Article Preview Reader")
        reader_layout = QVBoxLayout(reader_box)
        reader_layout.setContentsMargins(12, 14, 12, 12)
        reader_layout.setSpacing(8)

        self.lbl_reader_title = QLabel("Select an article from the list to preview")
        self.lbl_reader_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.lbl_reader_title.setWordWrap(True)
        self.lbl_reader_title.setStyleSheet("color: #38bdf8;")

        self.lbl_reader_meta = QLabel("")
        self.lbl_reader_meta.setStyleSheet("color: #94a3b8; font-size: 11px;")
        self.lbl_reader_meta.setWordWrap(True)

        self.txt_reader_body = QTextEdit()
        self.txt_reader_body.setReadOnly(True)
        self.txt_reader_body.setStyleSheet("background-color: #0f172a; color: #f8fafc; font-size: 13px; border: 1px solid #334155;")

        self.btn_open_browser = QPushButton("🌐 Open Article in Web Browser")
        self.btn_open_browser.setObjectName("accentBtn")
        self.btn_open_browser.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_open_browser.setEnabled(False)
        self.btn_open_browser.clicked.connect(self.open_article_in_browser)

        reader_layout.addWidget(self.lbl_reader_title)
        reader_layout.addWidget(self.lbl_reader_meta)
        reader_layout.addWidget(self.txt_reader_body, 1)
        reader_layout.addWidget(self.btn_open_browser)

        splitter.addWidget(reader_box)
        splitter.setSizes([620, 460])

        tab_articles_layout.addWidget(splitter, 1)
        self.tabs.addTab(tab_articles, "📰 Articles")

        # ----------------------------------------------------
        # OPTION 2: ⚙️ Feeds & Settings
        # ----------------------------------------------------
        tab_feeds = QWidget()
        tab_feeds_layout = QVBoxLayout(tab_feeds)
        tab_feeds_layout.setContentsMargins(10, 12, 10, 10)
        tab_feeds_layout.setSpacing(12)

        # Add New Feed Box + Presets
        add_box = QGroupBox("Add RSS Feed")
        add_layout = QHBoxLayout(add_box)
        add_layout.setSpacing(8)
        add_layout.setContentsMargins(12, 14, 12, 12)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Feed Name (e.g. TechCrunch)")

        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("RSS Feed URL (https://...)")

        self.input_cat = QLineEdit()
        self.input_cat.setPlaceholderText("Category")
        self.input_cat.setText("General")

        self.combo_add_freq = QComboBox()
        self.combo_add_freq.addItems(["Ping: 1h", "Ping: 3h", "Ping: 6h", "Ping: 12h", "Ping: 24h"])
        self.combo_add_freq.setCurrentIndex(3)

        self.combo_presets = QComboBox()
        self.combo_presets.addItem("⚡ Quick Presets...")
        for pf in PRESET_FEEDS:
            self.combo_presets.addItem(f"{pf['name']} ({pf['category']})")
        self.combo_presets.currentIndexChanged.connect(self._on_preset_selected)

        self.btn_add_feed = QPushButton("➕ Add Feed")
        self.btn_add_feed.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_feed.clicked.connect(self.add_feed)

        add_layout.addWidget(self.input_name, 2)
        add_layout.addWidget(self.input_url, 3)
        add_layout.addWidget(self.input_cat, 2)
        add_layout.addWidget(self.combo_add_freq, 2)
        add_layout.addWidget(self.combo_presets, 2)
        add_layout.addWidget(self.btn_add_feed, 2)

        tab_feeds_layout.addWidget(add_box)

        # Tracked Feeds Table Box
        table_box = QGroupBox("Tracked RSS Feeds Catalog")
        table_layout = QVBoxLayout(table_box)
        table_layout.setContentsMargins(12, 14, 12, 12)
        table_layout.setSpacing(8)

        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        self.input_feed_search = QLineEdit()
        self.input_feed_search.setPlaceholderText("🔍 Filter feeds by name, category, or URL...")
        self.input_feed_search.textChanged.connect(self.update_table)

        self.combo_cat_filter = QComboBox()
        self.combo_cat_filter.addItem("All Categories")
        self.combo_cat_filter.currentIndexChanged.connect(self.update_table)

        filter_layout.addWidget(self.input_feed_search, 4)
        filter_layout.addWidget(self.combo_cat_filter, 2)
        table_layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "URL", "Ping Frequency", "Enabled", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 140)
        self.table.setColumnWidth(4, 75)
        self.table.setColumnWidth(5, 170)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        table_layout.addWidget(self.table)
        tab_feeds_layout.addWidget(table_box, 3)

        # Scheduler Settings & Log Box
        sched_box = QGroupBox("Background Auto-Sync Scheduler & Console")
        sched_layout = QVBoxLayout(sched_box)
        sched_layout.setContentsMargins(12, 14, 12, 12)
        sched_layout.setSpacing(8)

        sched_top = QHBoxLayout()
        self.btn_timer = QPushButton("⚙ Enable 12-Hour Background Scraping")
        self.btn_timer.setObjectName("accentBtn")
        self.btn_timer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_timer.clicked.connect(self.enable_timer)

        self.btn_clear_log = QPushButton("Clear Log")
        self.btn_clear_log.setObjectName("secondaryBtn")
        self.btn_clear_log.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear_log.clicked.connect(self.clear_log)

        sched_top.addWidget(self.btn_timer)
        sched_top.addStretch()
        sched_top.addWidget(self.btn_clear_log)
        sched_layout.addLayout(sched_top)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        sched_layout.addWidget(self.log_console, 1)

        tab_feeds_layout.addWidget(sched_box, 2)
        self.tabs.addTab(tab_feeds, "⚙️ Feeds & Settings")

    def _create_stat_card(self, title: str, val_lbl: QLabel, color_hex: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            "QFrame { background-color: #0f172a; border: 1px solid #334155; border-radius: 6px; min-width: 130px; }"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #94a3b8; font-size: 10px; font-weight: bold;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        val_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        val_lbl.setStyleSheet(f"color: {color_hex}; font-size: 13px;")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)
        return card

    def log(self, message: str) -> None:
        """Appends a timestamped log message to the console with auto-scroll."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        self.log_console.append(formatted)
        self.log_console.verticalScrollBar().setValue(self.log_console.verticalScrollBar().maximum())

    def clear_log(self) -> None:
        """Clears log console text."""
        self.log_console.clear()

    def load_feeds(self) -> List[Dict[str, Any]]:
        """Loads feeds from config/feeds.json."""
        if not self.config_path.exists():
            self.feeds = []
            return self.feeds

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "feeds" in data:
                    self.feeds = data["feeds"]
                elif isinstance(data, list):
                    self.feeds = data
                else:
                    self.feeds = []
        except Exception as e:
            self.log(f"Error loading feeds config: {e}")
            self.feeds = []

        return self.feeds

    def save_feeds(self) -> None:
        """Saves feed list to config/feeds.json."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"feeds": self.feeds}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Failed to save feeds config: {e}")

    def update_table(self) -> None:
        """Populates the QTableWidget with tracked feeds."""
        self.table.setRowCount(0)

        search_txt = self.input_feed_search.text().strip().lower()
        selected_cat = self.combo_cat_filter.currentText()

        categories = sorted(list({f.get("category", "General") for f in self.feeds if f.get("category")}))
        current_cat_sel = self.combo_cat_filter.currentText()
        self.combo_cat_filter.blockSignals(True)
        self.combo_cat_filter.clear()
        self.combo_cat_filter.addItem("All Categories")
        for c in categories:
            self.combo_cat_filter.addItem(c)
        if current_cat_sel in categories:
            self.combo_cat_filter.setCurrentText(current_cat_sel)
        self.combo_cat_filter.blockSignals(False)

        freq_map = {1: 0, 3: 1, 6: 2, 12: 3, 24: 4}

        row_count = 0
        for feed in self.feeds:
            name = feed.get("name", "")
            cat = feed.get("category", "General")
            url = feed.get("url", "")
            feed_id = feed.get("id") or name.lower().replace(" ", "_")
            feed["id"] = feed_id

            if search_txt and not (search_txt in name.lower() or search_txt in cat.lower() or search_txt in url.lower()):
                continue
            if selected_cat != "All Categories" and selected_cat and cat != selected_cat:
                continue

            self.table.insertRow(row_count)

            # 0. Name
            item_name = QTableWidgetItem(name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_count, 0, item_name)

            # 1. Category
            item_cat = QTableWidgetItem(cat)
            item_cat.setFlags(item_cat.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_count, 1, item_cat)

            # 2. URL
            item_url = QTableWidgetItem(url)
            item_url.setFlags(item_url.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_count, 2, item_url)

            # 3. Frequency
            freq_combo = QComboBox()
            freq_combo.addItems(["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"])
            current_hours = feed.get("fetch_interval_hours", 12)
            combo_index = freq_map.get(current_hours, 3)
            freq_combo.setCurrentIndex(combo_index)
            freq_combo.currentIndexChanged.connect(
                lambda idx, fid=feed_id: self.change_feed_frequency_by_id(fid, [1, 3, 6, 12, 24][idx])
            )
            self.table.setCellWidget(row_count, 3, freq_combo)

            # 4. Checkbox Enabled
            cb_container = QWidget()
            cb_layout = QHBoxLayout(cb_container)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cb = QCheckBox()
            cb.setChecked(feed.get("enabled", True))
            cb.toggled.connect(lambda checked, fid=feed_id: self.toggle_feed_enabled_by_id(fid, checked))
            cb_layout.addWidget(cb)
            self.table.setCellWidget(row_count, 4, cb_container)

            # 5. Actions (Ping & Delete)
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(4)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            btn_ping = QPushButton("⚡ Ping")
            btn_ping.setObjectName("accentBtn")
            btn_ping.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_ping.setToolTip("Ping RSS Feed now and save results")
            btn_ping.clicked.connect(lambda _, fid=feed_id: self.ping_feed_by_id(fid))

            btn_del = QPushButton("Delete")
            btn_del.setObjectName("dangerBtn")
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda _, fid=feed_id: self.delete_feed_by_id(fid))

            btn_layout.addWidget(btn_ping)
            btn_layout.addWidget(btn_del)
            self.table.setCellWidget(row_count, 5, btn_container)

            row_count += 1

    def _on_preset_selected(self, index: int) -> None:
        """Fills input form when preset selected."""
        if index <= 0:
            return
        preset = PRESET_FEEDS[index - 1]
        self.input_name.setText(preset["name"])
        self.input_url.setText(preset["url"])
        self.input_cat.setText(preset["category"])
        self.combo_presets.setCurrentIndex(0)

    def change_feed_frequency_by_id(self, feed_id: str, hours: int) -> None:
        """Updates interval frequency for feed."""
        for feed in self.feeds:
            if feed.get("id") == feed_id:
                feed["fetch_interval_hours"] = hours
                self.save_feeds()
                self.log(f"Updated ping frequency for '{feed.get('name')}' to every {hours} hour(s).")
                break

    def toggle_feed_enabled_by_id(self, feed_id: str, enabled: bool) -> None:
        """Toggles feed active state."""
        for feed in self.feeds:
            if feed.get("id") == feed_id:
                feed["enabled"] = enabled
                self.save_feeds()
                self.update_stats()
                self.log(f"Feed '{feed.get('name')}' enabled state: {enabled}.")
                break

    def ping_feed_by_id(self, feed_id: str) -> None:
        """Pings a single RSS feed immediately."""
        target_feed = None
        for feed in self.feeds:
            if feed.get("id") == feed_id:
                target_feed = feed
                break

        if not target_feed:
            return

        if self.scrape_thread and self.scrape_thread.isRunning():
            self.log("Scrape worker busy. Please wait...")
            return

        feed_name = target_feed.get("name", "Feed")
        feed_url = target_feed.get("url", "")
        self.log(f"Pinging RSS feed '{feed_name}' ({feed_url})...")

        self.btn_scrape.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.scrape_thread = ScrapeThread([target_feed])
        self.scrape_thread.log_signal.connect(self.log)
        self.scrape_thread.finished_signal.connect(self.on_scrape_finished)
        self.scrape_thread.start()

    def add_feed(self) -> None:
        """Adds new RSS feed from form inputs."""
        name = self.input_name.text().strip()
        url = self.input_url.text().strip()
        category = self.input_cat.text().strip() or "General"
        freq_idx = self.combo_add_freq.currentIndex()
        freq_hours = [1, 3, 6, 12, 24][freq_idx]

        if not name or not url:
            QMessageBox.warning(self, "Validation Error", "Both Feed Name and RSS Feed URL are required.")
            return

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url

        feed_id = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_")
        if not feed_id:
            feed_id = f"feed_{len(self.feeds) + 1}"

        new_feed = {
            "id": feed_id,
            "name": name,
            "url": url,
            "category": category,
            "fetch_interval_hours": freq_hours,
            "enabled": True,
        }

        self.feeds.append(new_feed)
        self.save_feeds()
        self.update_table()
        self.update_stats()

        self.input_name.clear()
        self.input_url.clear()
        self.input_cat.setText("General")
        self.combo_add_freq.setCurrentIndex(3)

        self.log(f"Successfully added RSS Feed '{name}' ({url}) under '{category}'.")

    def delete_feed_by_id(self, feed_id: str) -> None:
        """Deletes feed by ID."""
        target_idx = None
        for idx, feed in enumerate(self.feeds):
            if feed.get("id") == feed_id:
                target_idx = idx
                break

        if target_idx is not None:
            deleted_feed = self.feeds.pop(target_idx)
            self.save_feeds()
            self.update_table()
            self.update_stats()
            self.log(f"Deleted RSS Feed '{deleted_feed.get('name', 'Unknown')}'.")

    def start_scraping(self) -> None:
        """Launches feed scraping in background worker thread."""
        if self.scrape_thread and self.scrape_thread.isRunning():
            self.log("Scraping already in progress...")
            return

        enabled_feeds = [f for f in self.feeds if f.get("enabled", True)]
        if not enabled_feeds:
            self.log("No enabled feeds found to scrape.")
            QMessageBox.information(self, "Sync Feeds", "There are no enabled feeds to scrape.")
            return

        self.btn_scrape.setEnabled(False)
        self.btn_scrape.setText("Syncing...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.scrape_thread = ScrapeThread(self.feeds)
        self.scrape_thread.log_signal.connect(self.log)
        self.scrape_thread.finished_signal.connect(self.on_scrape_finished)
        self.scrape_thread.start()

    def on_scrape_finished(self, new_count: int, total_count: int, errors: List[Dict[str, Any]]) -> None:
        """Callback when background scrape completes."""
        self.btn_scrape.setEnabled(True)
        self.btn_scrape.setText("⚡ Sync Now")
        self.progress_bar.setVisible(False)

        self.log(f"Scrape completed! Added {new_count} new article(s). Total stored: {total_count}.")

        if errors:
            self.log(f"Encountered {len(errors)} error(s) during feed fetch:")
            for err in errors:
                self.log(f"  - {err.get('feed_name', 'Unknown')}: {err.get('error')}")

        self.update_stats()
        self.refresh_articles_view()

    def enable_timer(self) -> None:
        """Installs systemd 12-hour background scraper timer."""
        self.log("Installing systemd 12-hour timer service...")
        success = install_systemd_timer()
        status = get_timer_status()

        if success or status.get("active"):
            self.log("Systemd background timer activated! (Every 12 Hours)")
            QMessageBox.information(
                self,
                "Scheduler Active",
                "Systemd background timer installed successfully.\nScraping will execute every 12 hours automatically.",
            )
        else:
            self.log("Warning: Systemd timer installation outputted warnings.")
            QMessageBox.warning(
                self,
                "Scheduler Notice",
                "Systemd timer installation was triggered. Status details:\n" + str(status.get("detail", "")),
            )

        self.update_stats()

    def update_stats(self) -> None:
        """Updates header stat counter pills."""
        try:
            stats = get_stats()
            timer_info = get_timer_status()

            total_arts = stats.get("total_articles", 0)
            total_feeds = len(self.feeds)
            active_feeds = sum(1 for f in self.feeds if f.get("enabled", True))

            self.lbl_stat_articles.setText(str(total_arts))
            self.lbl_stat_feeds.setText(f"{active_feeds} / {total_feeds}")

            if timer_info.get("active"):
                self.lbl_stat_timer.setText("Active (12h)")
                self.lbl_stat_timer.setStyleSheet("color: #34d399; font-size: 13px; font-weight: bold;")
            elif timer_info.get("installed"):
                self.lbl_stat_timer.setText("Installed")
                self.lbl_stat_timer.setStyleSheet("color: #fbbf24; font-size: 13px; font-weight: bold;")
            else:
                self.lbl_stat_timer.setText("Inactive")
                self.lbl_stat_timer.setStyleSheet("color: #f87171; font-size: 13px; font-weight: bold;")
        except Exception as e:
            self.log(f"Error updating UI stats: {e}")

    def refresh_articles_view(self) -> None:
        """Loads stored articles and updates Articles Library table."""
        search_query = self.input_art_search.text()
        cat_filter = self.combo_art_cat.currentText()

        articles = load_articles(limit=250, category=cat_filter, search_query=search_query)
        self.current_articles = articles

        all_articles_all = load_articles(limit=1000)
        cats = sorted(list({a.get("category", "General") for a in all_articles_all if a.get("category")}))
        cur_cat = self.combo_art_cat.currentText()
        self.combo_art_cat.blockSignals(True)
        self.combo_art_cat.clear()
        self.combo_art_cat.addItem("All Categories")
        for c in cats:
            self.combo_art_cat.addItem(c)
        if cur_cat in cats:
            self.combo_art_cat.setCurrentText(cur_cat)
        self.combo_art_cat.blockSignals(False)

        self.table_articles.setRowCount(0)
        for idx, art in enumerate(articles):
            self.table_articles.insertRow(idx)

            title_item = QTableWidgetItem(art.get("title", "Untitled"))
            feed_item = QTableWidgetItem(art.get("feed_name", "Unknown"))
            cat_item = QTableWidgetItem(art.get("category", "General"))

            raw_date = art.get("published_at_iso") or art.get("scraped_at_iso") or ""
            date_str = raw_date[:10] if len(raw_date) >= 10 else raw_date
            date_item = QTableWidgetItem(date_str)

            title_item.setFlags(title_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            feed_item.setFlags(feed_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.table_articles.setItem(idx, 0, title_item)
            self.table_articles.setItem(idx, 1, feed_item)
            self.table_articles.setItem(idx, 2, cat_item)
            self.table_articles.setItem(idx, 3, date_item)

    def _on_article_selected(self) -> None:
        """Updates right reader panel when selecting an article."""
        selected_rows = self.table_articles.selectedIndexes()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if 0 <= row < len(self.current_articles):
            art = self.current_articles[row]
            self.lbl_reader_title.setText(art.get("title", "Untitled"))

            meta_parts = []
            if art.get("feed_name"):
                meta_parts.append(f"Feed: {art['feed_name']}")
            if art.get("author"):
                meta_parts.append(f"Author: {art['author']}")
            if art.get("published_at_iso"):
                meta_parts.append(f"Published: {art['published_at_iso']}")

            self.lbl_reader_meta.setText(" | ".join(meta_parts))

            body_text = art.get("text_clean") or art.get("summary_raw") or "No content preview available."
            self.txt_reader_body.setPlainText(body_text)

            art_url = art.get("url")
            if art_url:
                self.btn_open_browser.setEnabled(True)
                self.btn_open_browser.setProperty("article_url", art_url)
            else:
                self.btn_open_browser.setEnabled(False)

    def open_article_in_browser(self) -> None:
        """Opens selected article URL in browser."""
        url = self.btn_open_browser.property("article_url")
        if url:
            QDesktopServices.openUrl(QUrl(url))
