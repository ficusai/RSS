"""
PyQt6 Main Window and GUI components for RSS Feed Manager & Scraper.
Clean, modern Deep Slate theme with simplified navigation.
"""

import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import Qt, QThread, QUrl, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
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

# Deep Slate Theme - Clean, Refined
STYLESHEET = """
QMainWindow {
    background-color: #0f172a;
    color: #f8fafc;
}
QWidget {
    font-family: "Segoe UI", "Inter", system-ui, sans-serif;
    color: #f8fafc;
}

/* Tab Bar */
QTabWidget::pane {
    border: none;
    background-color: #0f172a;
    top: 0px;
}
QTabBar::tab {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-bottom: 2px solid #334155;
    padding: 12px 24px;
    font-weight: 500;
    font-size: 14px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: transparent;
    color: #38bdf8;
    border-bottom: 2px solid #38bdf8;
}
QTabBar::tab:hover:!selected {
    color: #f8fafc;
}

/* Cards */
QFrame#headerCard, QFrame#toolbarCard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
}

/* Group Boxes */
QGroupBox {
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 12px;
    background-color: #1e293b;
    color: #38bdf8;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
}

/* Inputs */
QLineEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 9px 14px;
    color: #f8fafc;
    font-size: 13px;
}
QLineEdit:focus {
    border: 1px solid #38bdf8;
    background-color: #0f172a;
}
QLineEdit::placeholder {
    color: #64748b;
}

/* Buttons */
QPushButton {
    background-color: #38bdf8;
    color: #0f172a;
    font-weight: 600;
    font-size: 13px;
    border: none;
    border-radius: 6px;
    padding: 9px 18px;
}
QPushButton:hover {
    background-color: #7dd3fc;
}
QPushButton:pressed {
    background-color: #0ea5e9;
}
QPushButton:disabled {
    background-color: #334155;
    color: #64748b;
}
QPushButton#dangerBtn {
    background-color: #ef4444;
    color: white;
    padding: 6px 14px;
    font-size: 12px;
}
QPushButton#dangerBtn:hover {
    background-color: #f87171;
}
QPushButton#accentBtn {
    background-color: #10b981;
    color: white;
    padding: 6px 14px;
    font-size: 12px;
}
QPushButton#accentBtn:hover {
    background-color: #34d399;
}
QPushButton#secondaryBtn {
    background-color: #334155;
    color: #f8fafc;
    font-size: 13px;
}
QPushButton#secondaryBtn:hover {
    background-color: #475569;
}

/* Tables */
QTableWidget {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: #1e293b;
    color: #f8fafc;
    selection-background-color: #334155;
    selection-color: #f8fafc;
}
QHeaderView::section {
    background-color: #1e293b;
    color: #38bdf8;
    padding: 10px 12px;
    font-weight: 600;
    border: none;
    border-bottom: 1px solid #334155;
}
QTableWidget::item {
    padding: 8px 12px;
}

/* Text Editor / Log */
QTextEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #e2e8f0;
    font-family: "Cascadia Code", "JetBrains Mono", "Consolas", monospace;
    font-size: 12px;
    padding: 10px;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #334155;
    border-radius: 6px;
    text-align: center;
    background-color: #1e293b;
    color: #f8fafc;
    height: 6px;
}
QProgressBar::chunk {
    background-color: #38bdf8;
    border-radius: 5px;
}

/* Combo Box */
QComboBox {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 12px;
    color: #f8fafc;
    font-size: 13px;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #1e293b;
    color: #f8fafc;
    selection-background-color: #334155;
    border: 1px solid #334155;
    outline: none;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #0f172a;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background-color: #334155;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background-color: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background-color: #0f172a;
    height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background-color: #334155;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #475569;
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
    finished_signal = pyqtSignal(int, int, list)

    def __init__(self, feeds: List[Dict[str, Any]], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.feeds = copy.deepcopy(feeds)

    def run(self) -> None:
        try:
            self.log_signal.emit("Starting background feed scraper...")
            articles, errors = fetch_all_feeds(self.feeds)
            self.log_signal.emit(f"Processed {len(articles)} article(s)...")
            new_count, total_count = save_articles(articles)
            self.finished_signal.emit(new_count, total_count, errors)
        except Exception as e:
            self.log_signal.emit(f"Critical error: {e}")
            self.finished_signal.emit(0, 0, [{"feed_name": "System", "error": str(e)}])


class MainWindow(QMainWindow):
    """Main application window for RSS Feed Manager & Scraper."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RSS Reader & Scraper")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)

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
        self.log("Application started.")

    def _init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ── Header Card ──
        header_card = QFrame()
        header_card.setObjectName("headerCard")
        header_card.setFixedHeight(80)
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(16)

        # Logo & Title
        title_box = QHBoxLayout()
        title_box.setSpacing(12)

        logo_path = ASSETS_DIR / "ficus.png"
        if logo_path.exists():
            lbl_logo = QLabel()
            pix = QPixmap(str(logo_path))
            lbl_logo.setPixmap(pix.scaled(44, 44, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            title_box.addWidget(lbl_logo)

        text_box = QVBoxLayout()
        text_box.setSpacing(2)
        title_label = QLabel("RSS Reader & Scraper")
        title_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #38bdf8;")

        subtitle_label = QLabel("Automated Feed Aggregator")
        subtitle_label.setStyleSheet("color: #64748b; font-size: 11px;")
        text_box.addWidget(title_label)
        text_box.addWidget(subtitle_label)
        title_box.addLayout(text_box)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        # Stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(8)

        self.lbl_stat_articles = QLabel("0")
        self.card_articles = self._create_stat_card("Articles", self.lbl_stat_articles, "#818cf8")
        stats_layout.addWidget(self.card_articles)

        self.lbl_stat_feeds = QLabel("0")
        self.card_feeds = self._create_stat_card("Feeds", self.lbl_stat_feeds, "#38bdf8")
        stats_layout.addWidget(self.card_feeds)

        self.lbl_stat_timer = QLabel("Checking...")
        self.card_timer = self._create_stat_card("Auto-Sync", self.lbl_stat_timer, "#10b981")
        stats_layout.addWidget(self.card_timer)

        header_layout.addLayout(stats_layout)

        # Sync Button & Progress
        sync_box = QVBoxLayout()
        sync_box.setSpacing(4)
        self.btn_scrape = QPushButton("⚡ Sync Now")
        self.btn_scrape.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_scrape.clicked.connect(self.start_scraping)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)

        sync_box.addWidget(self.btn_scrape, 0, Qt.AlignmentFlag.AlignRight)
        sync_box.addWidget(self.progress_bar, 0, Qt.AlignmentFlag.AlignRight)
        header_layout.addLayout(sync_box)

        main_layout.addWidget(header_card)
        main_layout.addSpacing(16)

        # ── Tabs ──
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # ─── Tab 1: Articles ───
        tab_articles = QWidget()
        art_layout = QVBoxLayout(tab_articles)
        art_layout.setContentsMargins(0, 0, 0, 0)
        art_layout.setSpacing(12)

        # Search toolbar
        art_toolbar = QHBoxLayout()
        art_toolbar.setSpacing(10)

        self.input_art_search = QLineEdit()
        self.input_art_search.setPlaceholderText("Search articles by title, author, or keyword...")
        self.input_art_search.textChanged.connect(self.refresh_articles_view)

        self.combo_art_cat = QComboBox()
        self.combo_art_cat.addItem("All Categories")
        self.combo_art_cat.currentIndexChanged.connect(self.refresh_articles_view)

        self.btn_refresh_arts = QPushButton("Refresh")
        self.btn_refresh_arts.setObjectName("secondaryBtn")
        self.btn_refresh_arts.clicked.connect(self.refresh_articles_view)

        art_toolbar.addWidget(self.input_art_search, 1)
        art_toolbar.addWidget(self.combo_art_cat)
        art_toolbar.addWidget(self.btn_refresh_arts)
        art_layout.addLayout(art_toolbar)

        # Splitter: List | Reader
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(4)

        self.table_articles = QTableWidget()
        self.table_articles.setColumnCount(4)
        self.table_articles.setHorizontalHeaderLabels(["Title", "Source", "Category", "Date"])
        self.table_articles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_articles.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.setAlternatingRowColors(True)
        self.table_articles.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_articles.itemSelectionChanged.connect(self._on_article_selected)
        self.table_articles.verticalHeader().setVisible(False)
        self.table_articles.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Reader panel
        reader_frame = QFrame()
        reader_frame.setObjectName("toolbarCard")
        reader_layout = QVBoxLayout(reader_frame)
        reader_layout.setContentsMargins(16, 16, 16, 16)
        reader_layout.setSpacing(12)

        self.lbl_reader_title = QLabel("Select an article to read")
        self.lbl_reader_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.lbl_reader_title.setStyleSheet("color: #38bdf8;")
        self.lbl_reader_title.setWordWrap(True)

        self.lbl_reader_meta = QLabel("")
        self.lbl_reader_meta.setStyleSheet("color: #64748b; font-size: 11px;")
        self.lbl_reader_meta.setWordWrap(True)

        self.txt_reader_body = QTextEdit()
        self.txt_reader_body.setReadOnly(True)

        self.btn_open_browser = QPushButton("🌐 Open in Browser")
        self.btn_open_browser.setObjectName("accentBtn")
        self.btn_open_browser.setEnabled(False)
        self.btn_open_browser.clicked.connect(self.open_article_in_browser)

        reader_layout.addWidget(self.lbl_reader_title)
        reader_layout.addWidget(self.lbl_reader_meta)
        reader_layout.addStretch()
        reader_layout.addWidget(self.txt_reader_body, 1)
        reader_layout.addSpacing(8)
        reader_layout.addWidget(self.btn_open_browser, 0, Qt.AlignmentFlag.AlignRight)

        splitter.addWidget(self.table_articles)
        splitter.addWidget(reader_frame)
        splitter.setSizes([550, 500])

        art_layout.addWidget(splitter, 1)
        self.tabs.addTab(tab_articles, "📰 Articles")

        # ─── Tab 2: Feeds ───
        tab_feeds = QWidget()
        feeds_layout = QVBoxLayout(tab_feeds)
        feeds_layout.setContentsMargins(0, 0, 0, 0)
        feeds_layout.setSpacing(12)

        # Add Feed Form
        add_group = QGroupBox("Add New Feed")
        add_layout = QHBoxLayout(add_group)
        add_layout.setSpacing(10)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Feed Name")

        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://example.com/feed.xml")

        self.input_cat = QLineEdit()
        self.input_cat.setText("General")
        self.input_cat.setPlaceholderText("Category")

        self.combo_add_freq = QComboBox()
        self.combo_add_freq.addItems(["1h", "3h", "6h", "12h", "24h"])
        self.combo_add_freq.setCurrentIndex(3)

        self.combo_presets = QComboBox()
        self.combo_presets.setMaximumWidth(180)
        self.combo_presets.addItem("Quick Presets...")
        for pf in PRESET_FEEDS:
            self.combo_presets.addItem(f"{pf['name']}")
        self.combo_presets.currentIndexChanged.connect(self._on_preset_selected)

        self.btn_add_feed = QPushButton("Add Feed")
        self.btn_add_feed.clicked.connect(self.add_feed)

        add_layout.addWidget(self.input_name)
        add_layout.addWidget(self.input_url, 1)
        add_layout.addWidget(self.input_cat)
        add_layout.addWidget(self.combo_add_freq)
        add_layout.addWidget(self.combo_presets)
        add_layout.addWidget(self.btn_add_feed)

        feeds_layout.addWidget(add_group)

        # Feed Table
        table_group = QGroupBox("Tracked Feeds")
        table_layout = QVBoxLayout(table_group)
        table_layout.setSpacing(8)

        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(10)

        self.input_feed_search = QLineEdit()
        self.input_feed_search.setPlaceholderText("Filter feeds...")
        self.input_feed_search.textChanged.connect(self.update_table)

        self.combo_cat_filter = QComboBox()
        self.combo_cat_filter.addItem("All Categories")
        self.combo_cat_filter.currentIndexChanged.connect(self.update_table)

        filter_bar.addWidget(self.input_feed_search, 1)
        filter_bar.addWidget(self.combo_cat_filter)
        table_layout.addLayout(filter_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "URL", "Interval", "Active", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 60)
        self.table.setColumnWidth(5, 130)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        table_layout.addWidget(self.table)
        feeds_layout.addWidget(table_group, 1)

        # Scheduler & Log
        sched_group = QGroupBox("Background Scheduler")
        sched_layout = QVBoxLayout(sched_group)
        sched_layout.setSpacing(8)

        sched_btns = QHBoxLayout()

        self.btn_timer = QPushButton("Enable 12h Auto-Sync")
        self.btn_timer.setObjectName("accentBtn")
        self.btn_timer.clicked.connect(self.enable_timer)

        self.btn_clear_log = QPushButton("Clear Log")
        self.btn_clear_log.setObjectName("secondaryBtn")
        self.btn_clear_log.clicked.connect(self.clear_log)

        sched_btns.addWidget(self.btn_timer)
        sched_btns.addStretch()
        sched_btns.addWidget(self.btn_clear_log)
        sched_layout.addLayout(sched_btns)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        sched_layout.addWidget(self.log_console)

        feeds_layout.addWidget(sched_group)
        self.tabs.addTab(tab_feeds, "⚙️ Feeds")

    def _create_stat_card(self, title: str, val_lbl: QLabel, color_hex: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"background-color: #0f172a; border-radius: 6px; min-width: 90px;")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        val_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        val_lbl.setStyleSheet(f"color: {color_hex};")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)
        return card

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_console.append(f"<span style='color: #64748b;'>[{timestamp}]</span> {message}")
        self.log_console.verticalScrollBar().setValue(self.log_console.verticalScrollBar().maximum())

    def clear_log(self) -> None:
        self.log_console.clear()

    def load_feeds(self) -> List[Dict[str, Any]]:
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
            self.log(f"Error loading config: {e}")
            self.feeds = []
        return self.feeds

    def save_feeds(self) -> None:
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"feeds": self.feeds}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Failed to save config: {e}")

    def update_table(self) -> None:
        self.table.setRowCount(0)

        search_txt = self.input_feed_search.text().strip().lower()
        selected_cat = self.combo_cat_filter.currentText()

        categories = sorted({f.get("category", "General") for f in self.feeds if f.get("category")})
        cur_cat = self.combo_cat_filter.currentText()
        self.combo_cat_filter.blockSignals(True)
        self.combo_cat_filter.clear()
        self.combo_cat_filter.addItem("All Categories")
        for c in categories:
            self.combo_cat_filter.addItem(c)
        if cur_cat in categories:
            self.combo_cat_filter.setCurrentText(cur_cat)
        self.combo_cat_filter.blockSignals(False)

        freq_map = {1: 0, 3: 1, 6: 2, 12: 3, 24: 4}
        row = 0

        for feed in self.feeds:
            name = feed.get("name", "")
            cat = feed.get("category", "General")
            url = feed.get("url", "")
            feed_id = feed.get("id") or re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"feed_{row}"
            feed["id"] = feed_id

            if search_txt and not any(search_txt in v.lower() for v in [name, cat, url]):
                continue
            if selected_cat != "All Categories" and cat != selected_cat:
                continue

            self.table.insertRow(row)

            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, name_item)

            cat_item = QTableWidgetItem(cat)
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 1, cat_item)

            url_item = QTableWidgetItem(url)
            url_item.setFlags(url_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 2, url_item)

            freq_combo = QComboBox()
            freq_combo.addItems(["1h", "3h", "6h", "12h", "24h"])
            hours = feed.get("fetch_interval_hours", 12)
            freq_combo.setCurrentIndex(freq_map.get(hours, 3))
            freq_combo.currentIndexChanged.connect(
                lambda idx, fid=feed_id: self.change_feed_frequency(fid, [1, 3, 6, 12, 24][idx])
            )
            self.table.setCellWidget(row, 3, freq_combo)

            cb_container = QWidget()
            cb_layout = QHBoxLayout(cb_container)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cb = QCheckBox()
            cb.setChecked(feed.get("enabled", True))
            cb.toggled.connect(lambda checked, fid=feed_id: self.toggle_feed_enabled(fid, checked))
            cb_layout.addWidget(cb)
            self.table.setCellWidget(row, 4, cb_container)

            act_container = QWidget()
            act_layout = QHBoxLayout(act_container)
            act_layout.setContentsMargins(2, 2, 2, 2)
            act_layout.setSpacing(4)

            ping_btn = QPushButton("Ping")
            ping_btn.setObjectName("accentBtn")
            ping_btn.clicked.connect(lambda _, fid=feed_id: self.ping_feed(fid))

            del_btn = QPushButton("Delete")
            del_btn.setObjectName("dangerBtn")
            del_btn.clicked.connect(lambda _, fid=feed_id: self.delete_feed(fid))

            act_layout.addWidget(ping_btn)
            act_layout.addWidget(del_btn)
            self.table.setCellWidget(row, 5, act_container)

            row += 1

    def _on_preset_selected(self, index: int) -> None:
        if index <= 0:
            return
        preset = PRESET_FEEDS[index - 1]
        self.input_name.setText(preset["name"])
        self.input_url.setText(preset["url"])
        self.input_cat.setText(preset["category"])
        self.combo_presets.setCurrentIndex(0)

    def change_feed_frequency(self, feed_id: str, hours: int) -> None:
        for feed in self.feeds:
            if feed.get("id") == feed_id:
                feed["fetch_interval_hours"] = hours
                self.save_feeds()
                self.log(f"Updated '{feed.get('name')}' to every {hours}h")
                break

    def toggle_feed_enabled(self, feed_id: str, enabled: bool) -> None:
        for feed in self.feeds:
            if feed.get("id") == feed_id:
                feed["enabled"] = enabled
                self.save_feeds()
                self.update_stats()
                self.log(f"'{feed.get('name')}' {'enabled' if enabled else 'disabled'}")
                break

    def ping_feed(self, feed_id: str) -> None:
        target = next((f for f in self.feeds if f.get("id") == feed_id), None)
        if not target:
            return
        if self.scrape_thread and self.scrape_thread.isRunning():
            self.log("Scraper busy. Please wait...")
            return

        name = target.get("name", "Feed")
        self.log(f"Pinging '{name}'...")
        self.btn_scrape.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

        self.scrape_thread = ScrapeThread([target])
        self.scrape_thread.log_signal.connect(self.log)
        self.scrape_thread.finished_signal.connect(self.on_scrape_finished)
        self.scrape_thread.start()

    def add_feed(self) -> None:
        name = self.input_name.text().strip()
        url = self.input_url.text().strip()
        category = self.input_cat.text().strip() or "General"
        freq_idx = self.combo_add_freq.currentIndex()
        hours = [1, 3, 6, 12, 24][freq_idx]

        if not name or not url:
            QMessageBox.warning(self, "Validation Error", "Feed name and URL are required.")
            return

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        feed_id = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"feed_{len(self.feeds) + 1}"

        self.feeds.append({
            "id": feed_id,
            "name": name,
            "url": url,
            "category": category,
            "fetch_interval_hours": hours,
            "enabled": True,
        })
        self.save_feeds()
        self.update_table()
        self.update_stats()
        self.log(f"Added '{name}'")

        self.input_name.clear()
        self.input_url.clear()
        self.input_cat.setText("General")
        self.combo_add_freq.setCurrentIndex(3)

    def delete_feed(self, feed_id: str) -> None:
        for i, feed in enumerate(self.feeds):
            if feed.get("id") == feed_id:
                self.feeds.pop(i)
                self.save_feeds()
                self.update_table()
                self.update_stats()
                self.log(f"Deleted '{feed.get('name', 'Unknown')}'")
                return

    def start_scraping(self) -> None:
        if self.scrape_thread and self.scrape_thread.isRunning():
            return

        enabled = [f for f in self.feeds if f.get("enabled", True)]
        if not enabled:
            QMessageBox.information(self, "No Feeds", "No enabled feeds to sync.")
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
        self.btn_scrape.setEnabled(True)
        self.btn_scrape.setText("⚡ Sync Now")
        self.progress_bar.setVisible(False)

        self.log(f"Sync complete. +{new_count} articles. Total: {total_count}.")

        if errors:
            self.log(f"{len(errors)} error(s) occurred:")
            for err in errors:
                self.log(f"  • {err.get('feed_name', 'Unknown')}: {err.get('error')}")

        self.update_stats()
        self.refresh_articles_view()

    def enable_timer(self) -> None:
        self.log("Installing systemd timer...")
        success = install_systemd_timer()
        status = get_timer_status()

        if success or status.get("active"):
            self.log("Auto-sync enabled (12h intervals).")
            QMessageBox.information(self, "Timer Active", "Background scraping is now scheduled every 12 hours.")
        else:
            self.log("Timer installation failed.")
            QMessageBox.warning(self, "Timer Warning", f"Systemd timer status:\n{status.get('detail', '')}")

        self.update_stats()

    def update_stats(self) -> None:
        try:
            stats = get_stats()
            timer_info = get_timer_status()

            self.lbl_stat_articles.setText(str(stats.get("total_articles", 0)))
            active = sum(1 for f in self.feeds if f.get("enabled", True))
            self.lbl_stat_feeds.setText(f"{active}/{len(self.feeds)}")

            if timer_info.get("active"):
                self.lbl_stat_timer.setText("Active")
                self.lbl_stat_timer.setStyleSheet("color: #10b981; font-weight: bold;")
            elif timer_info.get("installed"):
                self.lbl_stat_timer.setText("Ready")
                self.lbl_stat_timer.setStyleSheet("color: #fbbf24; font-weight: bold;")
            else:
                self.lbl_stat_timer.setText("Off")
                self.lbl_stat_timer.setStyleSheet("color: #ef4444; font-weight: bold;")
        except Exception as e:
            self.log(f"Stats error: {e}")

    def refresh_articles_view(self) -> None:
        query = self.input_art_search.text()
        cat = self.combo_art_cat.currentText()

        articles = load_articles(limit=300, category=cat, search_query=query)
        self.current_articles = articles

        all_cats = sorted({a.get("category", "General") for a in load_articles(limit=1000) if a.get("category")})
        cur = self.combo_art_cat.currentText()
        self.combo_art_cat.blockSignals(True)
        self.combo_art_cat.clear()
        self.combo_art_cat.addItem("All Categories")
        for c in all_cats:
            self.combo_art_cat.addItem(c)
        if cur in all_cats:
            self.combo_art_cat.setCurrentText(cur)
        self.combo_art_cat.blockSignals(False)

        self.table_articles.setRowCount(0)
        for i, art in enumerate(articles):
            self.table_articles.insertRow(i)

            title = QTableWidgetItem(art.get("title", "Untitled"))
            feed = QTableWidgetItem(art.get("feed_name", "Unknown"))
            category = QTableWidgetItem(art.get("category", "General"))
            date_raw = art.get("published_at_iso") or art.get("scraped_at_iso") or ""
            date = QTableWidgetItem(date_raw[:10] if len(date_raw) >= 10 else date_raw)

            for col, item in enumerate([title, feed, category, date]):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_articles.setItem(i, col, item)

    def _on_article_selected(self) -> None:
        rows = self.table_articles.selectedIndexes()
        if not rows:
            return

        art = self.current_articles[rows[0].row()]
        self.lbl_reader_title.setText(art.get("title", "Untitled"))

        meta = []
        if art.get("feed_name"):
            meta.append(f"From: {art['feed_name']}")
        if art.get("author"):
            meta.append(f"By: {art['author']}")
        if art.get("published_at_iso"):
            meta.append(art["published_at_iso"][:10])
        self.lbl_reader_meta.setText("  •  ".join(meta))

        body = art.get("text_clean") or art.get("summary_raw") or "No content available."
        self.txt_reader_body.setPlainText(body)

        url = art.get("url")
        self.btn_open_browser.setEnabled(bool(url))
        if url:
            self.btn_open_browser.setProperty("article_url", url)

    def open_article_in_browser(self) -> None:
        url = self.btn_open_browser.property("article_url")
        if url:
            QDesktopServices.openUrl(QUrl(url))
