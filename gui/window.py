"""
PyQt6 Minimal Dark GUI for RSS Feed Manager & Scraper.
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

# Strictly dark palette - zero white
STYLESHEET = """
QMainWindow { background-color: #0d1117; color: #e6edf3; }
QWidget { font-family: "Segoe UI", system-ui, sans-serif; color: #e6edf3; }

QTabWidget::pane { border: none; background: #0d1117; top: 0; }
QTabBar::tab {
    background: #161b22; color: #8b949e;
    border: 1px solid #21262d; border-bottom: none;
    border-top-left-radius: 6px; border-top-right-radius: 6px;
    padding: 10px 22px; font-size: 14px; font-weight: 500;
}
QTabBar::tab:selected { background: #0d1117; color: #58a6ff; border-bottom: 2px solid #58a6ff; }
QTabBar::tab:hover { background: #1c2128; }

QFrame { background-color: #161b22; border: 1px solid #21262d; border-radius: 6px; }

QLineEdit {
    background: #0d1117; border: 1px solid #21262d; border-radius: 8px;
    padding: 14px 18px; color: #e6edf3; font-size: 15px;
    min-height: 46px;
}
QLineEdit:focus { border-color: #58a6ff; }
QLineEdit::placeholder { color: #484f58; }

QPushButton {
    background: #21262d; color: #e6edf3; border: 1px solid #30363d;
    border-radius: 8px; padding: 14px 28px; font-size: 15px;
    min-height: 46px;
}
QPushButton:hover { background: #30363d; border-color: #58a6ff; }
QPushButton:pressed { background: #1f6feb; color: #e6edf3; }
QPushButton:disabled { background: #161b22; color: #484f58; border-color: #21262d; }

QPushButton#accent { background: #1a5a2e; color: #3fb950; border-color: #238636; min-height: 46px; }
QPushButton#accent:hover { background: #216e39; }

QPushButton#danger { background: #3d1818; color: #f85149; border-color: #da3633; min-height: 46px; }
QPushButton#danger:hover { background: #4e2020; }

QTableWidget {
    background: #0d1117; border: 1px solid #21262d; border-radius: 6px;
    color: #e6edf3; gridline-color: #21262d; font-size: 14px;
    selection-background-color: #1f6feb33; selection-color: #e6edf3;
    min-height: 32px;
}
QHeaderView::section {
    background: #161b22; color: #8b949e; border: none;
    border-bottom: 1px solid #21262d; padding: 14px 12px;
    font-weight: 600; font-size: 14px; min-height: 44px;
}
QTableWidget::item { padding: 12px 14px; min-height: 44px; }

QTextEdit {
    background: #0d1117; border: 1px solid #21262d; border-radius: 6px;
    color: #e6edf3; font-family: "Cascadia Code", monospace; font-size: 14px; padding: 16px;
    min-height: 120px;
}

QProgressBar {
    border: 1px solid #21262d; border-radius: 6px; text-align: center;
    background: #161b22; height: 8px;
}
QProgressBar::chunk { background: #1f6feb; border-radius: 4px; }

QComboBox {
    background: #0d1117; border: 1px solid #21262d; border-radius: 8px;
    padding: 14px 18px; color: #e6edf3; font-size: 15px;
    min-height: 50px; max-height: 52px;
}
QComboBox::drop-down { border: none; width: 32px; }
QComboBox::down-arrow { width: 20px; height: 20px; }
QComboBox QAbstractItemView {
    background: #161b22; color: #e6edf3; border: 1px solid #21262d;
    selection-background-color: #1f6feb33; font-size: 15px;
    min-height: 48px; padding: 8px;
}
QComboBox QAbstractItemView::item {
    min-height: 48px; padding: 12px;
}

QScrollBar:vertical { background: #0d1117; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #30363d; border-radius: 4px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #484f58; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }

QScrollBar:horizontal { background: #0d1117; height: 8px; border-radius: 4px; }
QScrollBar::handle:horizontal { background: #30363d; border-radius: 4px; min-width: 24px; }
QScrollBar::handle:horizontal:hover { background: #484f58; }

QCheckBox { spacing: 10px; color: #e6edf3; font-size: 15px; min-height: 50px; padding: 8px; }
QCheckBox::indicator { width: 22px; height: 22px; border: 2px solid #30363d; border-radius: 5px; background: #0d1117; }
QCheckBox::indicator:checked { background: #1f6feb; border-color: #1f6feb; }
"""

PRESET_FEEDS = [
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"},
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss", "category": "Tech News"},
    {"name": "Federal Reserve", "url": "https://www.federalreserve.gov/feeds/press_all.xml", "category": "Finance"},
    {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/rss.xml", "category": "World News"},
    {"name": "Ars Technica", "url": "http://feeds.arstechnica.com/arstechnica/index", "category": "Technology"},
]


class ScrapeThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int, int, list)

    def __init__(self, feeds, parent=None):
        super().__init__(parent)
        self.feeds = copy.deepcopy(feeds)

    def run(self):
        try:
            self.log_signal.emit("Scraping feeds...")
            articles, errors = fetch_all_feeds(self.feeds)
            new, total = save_articles(articles)
            self.finished_signal.emit(new, total, errors)
        except Exception as e:
            self.log_signal.emit(f"Error: {e}")
            self.finished_signal.emit(0, 0, [{"feed_name": "System", "error": str(e)}])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSS")
        self.resize(900, 640)
        self.setMinimumSize(700, 500)

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
        self._log("Started")

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(0)
        layout.setContentsMargins(12, 12, 12, 12)

        # Header
        hdr = QFrame()
        hdr_layout = QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(12, 8, 12, 8)

        title_lbl = QLabel("RSS Feed Manager")
        title_lbl.setFont(QFont("", 14, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #58a6ff;")
        hdr_layout.addWidget(title_lbl)
        hdr_layout.addStretch()

        self.lbl_stats = QLabel("0 articles | 0 feeds")
        self.lbl_stats.setStyleSheet("color: #8b949e; font-size: 14px;")
        hdr_layout.addWidget(self.lbl_stats)

        self.btn_sync = QPushButton("Sync")
        self.btn_sync.setObjectName("accent")
        self.btn_sync.clicked.connect(self.start_scrape)
        hdr_layout.addWidget(self.btn_sync)

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        layout.addWidget(self.progress, 0, Qt.AlignmentFlag.AlignRight)

        layout.addWidget(hdr)
        layout.addSpacing(8)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Tab 1: Articles
        tab_art = QWidget()
        art_l = QVBoxLayout(tab_art)
        art_l.setContentsMargins(0, 0, 0, 0)
        art_l.setSpacing(8)

        art_filter = QHBoxLayout()
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Search...")
        self.input_search.textChanged.connect(self.refresh_articles)
        self.combo_cat = QComboBox()
        self.combo_cat.addItem("All")
        self.combo_cat.currentIndexChanged.connect(self.refresh_articles)
        art_filter.addWidget(self.input_search, 1)
        art_filter.addWidget(self.combo_cat)
        art_l.addLayout(art_filter)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.table_articles = QTableWidget()
        self.table_articles.setColumnCount(4)
        self.table_articles.setHorizontalHeaderLabels(["Title", "Source", "Category", "Date"])
        self.table_articles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_articles.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_articles.verticalHeader().setVisible(False)
        self.table_articles.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_articles.itemSelectionChanged.connect(self.on_article_sel)

        self.txt_reader = QTextEdit()
        self.txt_reader.setReadOnly(True)
        self.btn_open = QPushButton("Open in Browser")
        self.btn_open.setObjectName("accent")
        self.btn_open.setEnabled(False)
        self.btn_open.clicked.connect(self.open_browser)

        reader_box = QFrame()
        reader_l = QVBoxLayout(reader_box)
        reader_l.setContentsMargins(8, 8, 8, 8)
        reader_l.setSpacing(6)
        self.lbl_reader_title = QLabel("")
        self.lbl_reader_title.setStyleSheet("color: #58a6ff; font-size: 14px; font-weight: bold;")
        self.lbl_reader_meta = QLabel("")
        self.lbl_reader_meta.setStyleSheet("color: #8b949e; font-size: 14px;")
        reader_l.addWidget(self.lbl_reader_title)
        reader_l.addWidget(self.lbl_reader_meta)
        reader_l.addWidget(self.txt_reader, 1)
        reader_l.addWidget(self.btn_open, 0, Qt.AlignmentFlag.AlignRight)

        splitter.addWidget(self.table_articles)
        splitter.addWidget(reader_box)
        splitter.setSizes([500, 350])
        art_l.addWidget(splitter, 1)
        self.tabs.addTab(tab_art, "Articles")

        # Tab 2: Feeds
        tab_feed = QWidget()
        feed_l = QVBoxLayout(tab_feed)
        feed_l.setContentsMargins(0, 0, 0, 0)
        feed_l.setSpacing(8)

        add_box = QFrame()
        add_l = QHBoxLayout(add_box)
        add_l.setContentsMargins(8, 6, 8, 6)
        add_l.setSpacing(6)

        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("Name")
        self.in_url = QLineEdit()
        self.in_url.setPlaceholderText("https://feed-url")
        self.in_cat = QLineEdit()
        self.in_cat.setText("General")
        self.in_cat.setPlaceholderText("Category")
        self.cb_freq = QComboBox()
        self.cb_freq.addItems(["1h", "3h", "6h", "12h", "24h"])
        self.cb_freq.setCurrentIndex(3)
        self.cb_preset = QComboBox()
        self.cb_preset.setMaximumWidth(150)
        self.cb_preset.addItem("Presets")
        for p in PRESET_FEEDS:
            self.cb_preset.addItem(p["name"])
        self.cb_preset.currentIndexChanged.connect(self.on_preset)
        self.btn_add = QPushButton("Add")
        self.btn_add.setObjectName("accent")
        self.btn_add.clicked.connect(self.add_feed)

        add_l.addWidget(self.in_name)
        add_l.addWidget(self.in_url, 1)
        add_l.addWidget(self.in_cat)
        add_l.addWidget(self.cb_freq)
        add_l.addWidget(self.cb_preset)
        add_l.addWidget(self.btn_add)
        feed_l.addWidget(add_box)

        filter_l = QHBoxLayout()
        self.in_filter = QLineEdit()
        self.in_filter.setPlaceholderText("Filter feeds...")
        self.in_filter.textChanged.connect(self.refresh_table)
        self.cb_cat_filter = QComboBox()
        self.cb_cat_filter.addItem("All")
        self.cb_cat_filter.currentIndexChanged.connect(self.refresh_table)
        filter_l.addWidget(self.in_filter, 1)
        filter_l.addWidget(self.cb_cat_filter)
        feed_l.addLayout(filter_l)

        self.table_feeds = QTableWidget()
        self.table_feeds.setColumnCount(5)
        self.table_feeds.setHorizontalHeaderLabels(["Name", "Category", "Interval", "Active", "Actions"])
        self.table_feeds.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_feeds.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_feeds.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_feeds.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_feeds.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table_feeds.verticalHeader().setVisible(False)
        feed_l.addWidget(self.table_feeds, 1)

        sched_l = QHBoxLayout()
        self.btn_timer = QPushButton("Enable Scheduler")
        self.btn_timer.setObjectName("accent")
        self.btn_timer.clicked.connect(self.enable_timer)
        self.btn_clear = QPushButton("Clear Log")
        self.btn_clear.clicked.connect(self.clear_log)
        sched_l.addWidget(self.btn_timer)
        sched_l.addStretch()
        sched_l.addWidget(self.btn_clear)
        feed_l.addLayout(sched_l)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        feed_l.addWidget(self.log_box)

        self.tabs.addTab(tab_feed, "Feeds")

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
            with open(self.config_path, "r") as f:
                data = json.load(f)
                self.feeds = data.get("feeds", data) if isinstance(data, dict) else data
        except Exception:
            self.feeds = []

    def save_feeds(self):
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump({"feeds": self.feeds}, f, indent=2)
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
            timer = get_timer_status()
            timer_s = "on" if timer.get("active") else "off"
            self.lbl_stats.setText(f"{arts} articles | {active}/{total} feeds | sync:{timer_s}")
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
        self.cb_cat_filter.addItem("All")
        for c in cats:
            self.cb_cat_filter.addItem(c)
        if cur in cats:
            self.cb_cat_filter.setCurrentText(cur)
        self.cb_cat_filter.blockSignals(False)

        freq_map = {"1h": 0, "3h": 1, "6h": 2, "12h": 3, "24h": 4}
        row = 0
        for feed in self.feeds:
            name = feed.get("name", "")
            cat = feed.get("category", "General")
            url = feed.get("url", "")
            fid = feed.get("id") or re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"f{row}"
            feed["id"] = fid

            if search and not any(search in v.lower() for v in [name, cat, url]):
                continue
            if cat_f != "All" and cat != cat_f:
                continue

            self.table_feeds.insertRow(row)
            self.table_feeds.setItem(row, 0, QTableWidgetItem(name))
            self.table_feeds.setItem(row, 1, QTableWidgetItem(cat))

            freq_cb = QComboBox()
            freq_cb.addItems(["1h", "3h", "6h", "12h", "24h"])
            h = feed.get("fetch_interval_hours", 12)
            freq_cb.setCurrentIndex(freq_map.get(h, 3))
            freq_cb.currentIndexChanged.connect(lambda i, fid=fid: self.set_freq(fid, [1,3,6,12,24][i]))
            freq_cb.setMinimumHeight(46)
            freq_cb.setMaximumHeight(50)
            self.table_feeds.setCellWidget(row, 2, freq_cb)

            cb_w = QWidget()
            cb_l = QHBoxLayout(cb_w)
            cb_l.setContentsMargins(0,0,0,0)
            cb_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cb = QCheckBox()
            cb.setChecked(feed.get("enabled", True))
            cb.toggled.connect(lambda on, fid=fid: self.toggle(fid, on))
            cb.setMinimumHeight(46)
            cb.setMaximumHeight(50)
            cb_l.addWidget(cb)
            self.table_feeds.setCellWidget(row, 3, cb_w)

            act_w = QWidget()
            act_l = QHBoxLayout(act_w)
            act_l.setContentsMargins(0,0,0,0)
            act_l.setSpacing(6)
            pbtn = QPushButton("Ping")
            pbtn.setObjectName("accent")
            pbtn.setMinimumHeight(46)
            pbtn.setMaximumHeight(50)
            pbtn.clicked.connect(lambda _, fid=fid: self.ping(fid))
            dbtn = QPushButton("Del")
            dbtn.setObjectName("danger")
            dbtn.setMinimumHeight(46)
            dbtn.setMaximumHeight(50)
            dbtn.clicked.connect(lambda _, fid=fid: self.delete_feed(fid))
            act_l.addWidget(pbtn)
            act_l.addWidget(dbtn)
            self.table_feeds.setCellWidget(row, 4, act_w)
            row += 1

    def refresh_articles(self):
        q = self.input_search.text()
        cat = self.combo_cat.currentText()

        arts = load_articles(limit=300, category=cat if cat != "All" else "", search_query=q)
        self.current_articles = arts

        all_cats = sorted({a.get("category", "General") for a in load_articles(limit=1000) if a.get("category")})
        cur = self.combo_cat.currentText()
        self.combo_cat.blockSignals(True)
        self.combo_cat.clear()
        self.combo_cat.addItem("All")
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
            cat = a.get("category", "General")
            dt = (a.get("published_at_iso") or a.get("scraped_at_iso") or "")[:10]
            for col, val in enumerate([title, src, cat, dt]):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table_articles.setItem(i, col, item)

    def on_article_sel(self):
        rows = self.table_articles.selectedIndexes()
        if not rows:
            return
        a = self.current_articles[rows[0].row()]
        self.lbl_reader_title.setText(a.get("title", ""))
        meta = []
        if a.get("feed_name"): meta.append(a["feed_name"])
        if a.get("author"): meta.append(a["author"])
        if a.get("published_at_iso"): meta.append(a["published_at_iso"][:10])
        self.lbl_reader_meta.setText(" · ".join(meta))
        body = a.get("text_clean") or a.get("summary_raw") or ""
        self.txt_reader.setPlainText(body)
        url = a.get("url")
        self.btn_open.setEnabled(bool(url))
        if url:
            self.btn_open.setProperty("url", url)

    def open_browser(self):
        url = self.btn_open.property("url")
        if url:
            QDesktopServices.openUrl(QUrl(url))

    def on_preset(self, i):
        if i <= 0:
            return
        p = PRESET_FEEDS[i - 1]
        self.in_name.setText(p["name"])
        self.in_url.setText(p["url"])
        self.in_cat.setText(p["category"])
        self.cb_preset.setCurrentIndex(0)

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
        self._log(f"Pinging {target['name']}")
        self._run_scrape([target])

    def add_feed(self):
        name = self.in_name.text().strip()
        url = self.in_url.text().strip()
        cat = self.in_cat.text().strip() or "General"
        h = [1, 3, 6, 12, 24][self.cb_freq.currentIndex()]
        if not name or not url:
            QMessageBox.warning(self, "Missing", "Name and URL required")
            return
        if not url.startswith("http"):
            url = "https://" + url
        fid = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_") or f"f{len(self.feeds)}"
        self.feeds.append({"id": fid, "name": name, "url": url, "category": cat, "fetch_interval_hours": h, "enabled": True})
        self.save_feeds()
        self.refresh()
        self._log(f"Added {name}")
        self.in_name.clear()
        self.in_url.clear()

    def delete_feed(self, fid):
        for i, f in enumerate(self.feeds):
            if f.get("id") == fid:
                self.feeds.pop(i)
                self.save_feeds()
                self.refresh()
                self._log(f"Deleted {f.get('name')}")
                return

    def start_scrape(self):
        if self.scrape_thread and self.scrape_thread.isRunning():
            return
        enabled = [f for f in self.feeds if f.get("enabled")]
        if not enabled:
            QMessageBox.information(self, "No feeds", "Enable at least one feed.")
            return
        self._run_scrape(self.feeds)

    def _run_scrape(self, feeds):
        self.btn_sync.setEnabled(False)
        self.btn_sync.setText("...")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.scrape_thread = ScrapeThread(feeds)
        self.scrape_thread.log_signal.connect(self._log)
        self.scrape_thread.finished_signal.connect(self.on_done)
        self.scrape_thread.start()

    def on_done(self, new, total, errors):
        self.btn_sync.setEnabled(True)
        self.btn_sync.setText("Sync")
        self.progress.setVisible(False)
        self._log(f"Done. +{new} articles. Total: {total}.")
        if errors:
            self._log(f"Errors: {len(errors)}")
        self.update_stats()
        self.refresh_articles()

    def enable_timer(self):
        self._log("Installing timer...")
        ok = install_systemd_timer()
        st = get_timer_status()
        if ok or st.get("active"):
            self._log("Timer enabled (12h)")
            QMessageBox.information(self, "Timer", "Background scraper active every 12h.")
        else:
            self._log("Timer failed")
            QMessageBox.warning(self, "Timer", str(st.get("detail", "")))
        self.update_stats()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
