"""
PyQt6 Main Window and GUI components for RSS Feed Manager & Scraper.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
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
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.fetcher import fetch_all_feeds
from core.scheduler import get_timer_status, install_systemd_timer
from core.storage import get_stats, save_articles

CONFIG_PATH = Path("/home/ficus-pro/Documents/RSS/config/feeds.json")

STYLESHEET = """
QMainWindow {
    background-color: #1e1e2e;
    color: #cdd6f4;
}
QWidget {
    font-family: "Segoe UI", "Ubuntu", sans-serif;
    color: #cdd6f4;
}
QFrame.card {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 8px;
}
QGroupBox {
    font-weight: bold;
    font-size: 13px;
    border: 1px solid #313244;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 14px;
    background-color: #181825;
    color: #89b4fa;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}
QLineEdit {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 8px 12px;
    color: #cdd6f4;
    font-size: 13px;
}
QLineEdit:focus {
    border: 1px solid #89b4fa;
}
QPushButton {
    background-color: #89b4fa;
    color: #11111b;
    font-weight: bold;
    font-size: 12px;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #b4befe;
}
QPushButton:pressed {
    background-color: #74c7ec;
}
QPushButton:disabled {
    background-color: #45475a;
    color: #7f849c;
}
QPushButton#dangerBtn {
    background-color: #f38ba8;
    color: #11111b;
    padding: 4px 10px;
    font-size: 11px;
}
QPushButton#dangerBtn:hover {
    background-color: #eba0ac;
}
QPushButton#accentBtn {
    background-color: #a6e3a1;
    color: #11111b;
}
QPushButton#accentBtn:hover {
    background-color: #94e2d5;
}
QTableWidget {
    background-color: #11111b;
    border: 1px solid #313244;
    gridline-color: #313244;
    border-radius: 6px;
    color: #cdd6f4;
    selection-background-color: #45475a;
    selection-color: #cdd6f4;
}
QHeaderView::section {
    background-color: #313244;
    color: #cdd6f4;
    padding: 8px;
    font-weight: bold;
    border: none;
}
QTextEdit {
    background-color: #11111b;
    border: 1px solid #313244;
    border-radius: 6px;
    color: #a6e3a1;
    font-family: "Cascadia Code", "Consolas", "Monospace", monospace;
    font-size: 12px;
}
QProgressBar {
    border: 1px solid #313244;
    border-radius: 6px;
    text-align: center;
    background-color: #181825;
    color: #cdd6f4;
}
QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 5px;
}
"""


class ScrapeThread(QThread):
    """Background worker thread for non-blocking RSS scraping."""

    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int, int, list)  # (new_articles, total_articles, errors)

    def __init__(self, feeds: List[Dict[str, Any]], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.feeds = feeds

    def run(self) -> None:
        try:
            self.log_signal.emit("Starting background feed scraping worker...")
            articles, errors = fetch_all_feeds(self.feeds)
            self.log_signal.emit(f"Fetch completed. Processing {len(articles)} total raw articles...")
            new_count, total_count = save_articles(articles)
            self.finished_signal.emit(new_count, total_count, errors)
        except Exception as e:
            self.log_signal.emit(f"Critical error during feed scraping: {e}")
            self.finished_signal.emit(0, 0, [{"feed_name": "System", "error": str(e)}])


class MainWindow(QMainWindow):
    """Main application window for RSS Feed Manager & Scraper."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RSS Feed Manager & Scraper")
        self.resize(1000, 750)

        self.config_path = CONFIG_PATH
        self.feeds: List[Dict[str, Any]] = []
        self.scrape_thread: Optional[ScrapeThread] = None

        self.setStyleSheet(STYLESHEET)
        self._init_ui()
        self.load_feeds()
        self.update_table()
        self.update_stats()
        self.log("Application started. Ready.")

    def _init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # 1. Header Card & Stats Bar
        header_card = QFrame()
        header_card.setProperty("class", "card")
        header_card.setStyleSheet("background-color: #181825; border: 1px solid #313244; border-radius: 8px;")
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(16, 14, 16, 14)

        # Title container
        title_box = QVBoxLayout()
        title_label = QLabel("RSS Feed Manager & Scraper")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #89b4fa;")
        subtitle_label = QLabel("Automated Feed Scraper & Systemd Scheduler Dashboard")
        subtitle_label.setStyleSheet("color: #a6adc8; font-size: 11px;")
        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        # Stat Counters Layout
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        # Stat Card 1: Total Articles
        self.card_articles = self._create_stat_card("Total Articles", "0", "#b4befe")
        self.lbl_stat_articles = self.card_articles.findChild(QLabel, "stat_value")
        stats_layout.addWidget(self.card_articles)

        # Stat Card 2: Feeds Count
        self.card_feeds = self._create_stat_card("Tracked Feeds", "0", "#89b4fa")
        self.lbl_stat_feeds = self.card_feeds.findChild(QLabel, "stat_value")
        stats_layout.addWidget(self.card_feeds)

        # Stat Card 3: Timer Status
        self.card_timer = self._create_stat_card("Timer Status", "Checking...", "#f38ba8")
        self.lbl_stat_timer = self.card_timer.findChild(QLabel, "stat_value")
        stats_layout.addWidget(self.card_timer)

        header_layout.addLayout(stats_layout)
        main_layout.addWidget(header_card)

        # 2. Add Feed Section
        add_box = QGroupBox("Add RSS Feed")
        add_layout = QHBoxLayout(add_box)
        add_layout.setSpacing(10)
        add_layout.setContentsMargins(14, 16, 14, 14)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Feed Name (e.g. TechCrunch)")
        
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("RSS Feed URL (https://...)")

        self.input_cat = QLineEdit()
        self.input_cat.setPlaceholderText("Category")
        self.input_cat.setText("General")

        self.btn_add_feed = QPushButton("Add RSS Feed")
        self.btn_add_feed.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_feed.clicked.connect(self.add_feed)

        add_layout.addWidget(self.input_name, 2)
        add_layout.addWidget(self.input_url, 4)
        add_layout.addWidget(self.input_cat, 2)
        add_layout.addWidget(self.btn_add_feed, 2)

        main_layout.addWidget(add_box)

        # 3. Tracked Feeds Table
        table_box = QGroupBox("Tracked Feeds")
        table_layout = QVBoxLayout(table_box)
        table_layout.setContentsMargins(14, 16, 14, 14)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "URL", "Enabled", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 90)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        table_layout.addWidget(self.table)
        main_layout.addWidget(table_box, 3)

        # 4. Manual Action & Scheduler Toolbar
        toolbar_box = QFrame()
        toolbar_box.setProperty("class", "card")
        toolbar_box.setStyleSheet("background-color: #181825; border: 1px solid #313244; border-radius: 8px;")
        toolbar_layout = QHBoxLayout(toolbar_box)
        toolbar_layout.setContentsMargins(14, 10, 14, 10)
        toolbar_layout.setSpacing(12)

        self.btn_scrape = QPushButton("⚡ Scrape Feeds Now")
        self.btn_scrape.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_scrape.clicked.connect(self.start_scraping)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(22)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)

        self.btn_timer = QPushButton("⚙ Enable 12-Hour Background Scraping")
        self.btn_timer.setObjectName("accentBtn")
        self.btn_timer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_timer.clicked.connect(self.enable_timer)

        toolbar_layout.addWidget(self.btn_scrape, 2)
        toolbar_layout.addWidget(self.progress_bar, 3)
        toolbar_layout.addWidget(self.btn_timer, 3)

        main_layout.addWidget(toolbar_box)

        # 5. Log Console
        log_box = QGroupBox("Log Console")
        log_layout = QVBoxLayout(log_box)
        log_layout.setContentsMargins(14, 16, 14, 14)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)

        log_layout.addWidget(self.log_console)
        main_layout.addWidget(log_box, 2)

    def _create_stat_card(self, title: str, default_value: str, color_hex: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            "QFrame { background-color: #11111b; border: 1px solid #313244; border-radius: 6px; min-width: 120px; }"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #a6adc8; font-size: 10px; font-weight: bold;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        val_lbl = QLabel(default_value)
        val_lbl.setObjectName("stat_value")
        val_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        val_lbl.setStyleSheet(f"color: {color_hex}; font-size: 13px;")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(val_lbl)
        return card

    def log(self, message: str) -> None:
        """Appends a timestamped log message to the log console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        self.log_console.append(formatted)

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
        """Saves current feed list to config/feeds.json."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump({"feeds": self.feeds}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Failed to save feeds to config: {e}")

    def update_table(self) -> None:
        """Populates the QTableWidget with current tracked feeds."""
        self.table.setRowCount(0)

        for row_idx, feed in enumerate(self.feeds):
            self.table.insertRow(row_idx)

            # Name
            item_name = QTableWidgetItem(feed.get("name", ""))
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_idx, 0, item_name)

            # Category
            item_cat = QTableWidgetItem(feed.get("category", "General"))
            item_cat.setFlags(item_cat.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_idx, 1, item_cat)

            # URL
            item_url = QTableWidgetItem(feed.get("url", ""))
            item_url.setFlags(item_url.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_idx, 2, item_url)

            # Enabled (Checkbox)
            cb_container = QWidget()
            cb_layout = QHBoxLayout(cb_container)
            cb_layout.setContentsMargins(0, 0, 0, 0)
            cb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cb = QCheckBox()
            cb.setChecked(feed.get("enabled", True))
            cb.toggled.connect(lambda checked, idx=row_idx: self.toggle_feed_enabled(idx, checked))
            cb_layout.addWidget(cb)
            self.table.setCellWidget(row_idx, 3, cb_container)

            # Action (Delete Button)
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_del = QPushButton("Delete")
            btn_del.setObjectName("dangerBtn")
            btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_del.clicked.connect(lambda _, idx=row_idx: self.delete_feed(idx))
            btn_layout.addWidget(btn_del)
            self.table.setCellWidget(row_idx, 4, btn_container)

    def add_feed(self) -> None:
        """Adds a new RSS feed from the input form."""
        name = self.input_name.text().strip()
        url = self.input_url.text().strip()
        category = self.input_cat.text().strip() or "General"

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
            "enabled": True,
        }

        self.feeds.append(new_feed)
        self.save_feeds()
        self.update_table()
        self.update_stats()

        self.input_name.clear()
        self.input_url.clear()
        self.input_cat.setText("General")

        self.log(f"Successfully added RSS Feed '{name}' ({url}) under '{category}'.")

    def delete_feed(self, index: int) -> None:
        """Removes a feed at the specified index."""
        if 0 <= index < len(self.feeds):
            deleted_feed = self.feeds.pop(index)
            self.save_feeds()
            self.update_table()
            self.update_stats()
            self.log(f"Deleted RSS Feed '{deleted_feed.get('name', 'Unknown')}'.")

    def toggle_feed_enabled(self, index: int, enabled: bool) -> None:
        """Toggles the enabled status of a feed."""
        if 0 <= index < len(self.feeds):
            self.feeds[index]["enabled"] = enabled
            self.save_feeds()
            self.update_stats()
            self.log(f"Feed '{self.feeds[index].get('name')}' enabled state updated to: {enabled}.")

    def start_scraping(self) -> None:
        """Launches feed scraping in a background thread."""
        if self.scrape_thread and self.scrape_thread.isRunning():
            self.log("Scraping already in progress...")
            return

        enabled_feeds = [f for f in self.feeds if f.get("enabled", True)]
        if not enabled_feeds:
            self.log("No enabled feeds found to scrape.")
            QMessageBox.information(self, "Scrape Feeds", "There are no enabled feeds to scrape.")
            return

        self.btn_scrape.setEnabled(False)
        self.btn_scrape.setText("Scraping...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate mode

        self.scrape_thread = ScrapeThread(self.feeds)
        self.scrape_thread.log_signal.connect(self.log)
        self.scrape_thread.finished_signal.connect(self.on_scrape_finished)
        self.scrape_thread.start()

    def on_scrape_finished(self, new_count: int, total_count: int, errors: List[Dict[str, Any]]) -> None:
        """Callback executed when background scrape thread completes."""
        self.btn_scrape.setEnabled(True)
        self.btn_scrape.setText("⚡ Scrape Feeds Now")
        self.progress_bar.setVisible(False)

        self.log(f"Scrape completed successfully! Added {new_count} new article(s). Total stored: {total_count}.")

        if errors:
            self.log(f"Encountered {len(errors)} error(s) during feed fetch:")
            for err in errors:
                self.log(f"  - {err.get('feed_name', 'Unknown')}: {err.get('error')}")

        self.update_stats()

    def enable_timer(self) -> None:
        """Installs and starts the systemd 12-hour background scraping timer."""
        self.log("Installing systemd 12-hour timer service...")
        success = install_systemd_timer()
        status = get_timer_status()

        if success or status.get("active"):
            self.log("Systemd background timer installed & activated successfully! (Every 12 Hours)")
            QMessageBox.information(
                self,
                "Scheduler Active",
                "Systemd background timer installed successfully.\nScraping will execute every 12 hours automatically.",
            )
        else:
            self.log("Warning: Systemd timer installation completed with potential warnings.")
            QMessageBox.warning(
                self,
                "Scheduler Notice",
                "Systemd timer installation was triggered. Status details:\n" + str(status.get("detail", "")),
            )

        self.update_stats()

    def update_stats(self) -> None:
        """Updates stat counter widgets and timer status."""
        try:
            stats = get_stats()
            timer_info = get_timer_status()

            total_arts = stats.get("total_articles", 0)
            total_feeds = len(self.feeds)
            active_feeds = sum(1 for f in self.feeds if f.get("enabled", True))

            self.lbl_stat_articles.setText(str(total_arts))
            self.lbl_stat_feeds.setText(f"{total_feeds} ({active_feeds} Active)")

            if timer_info.get("active"):
                self.lbl_stat_timer.setText("Active (12h)")
                self.lbl_stat_timer.setStyleSheet("color: #a6e3a1; font-size: 13px; font-weight: bold;")
            elif timer_info.get("installed"):
                self.lbl_stat_timer.setText("Installed")
                self.lbl_stat_timer.setStyleSheet("color: #f9e2af; font-size: 13px; font-weight: bold;")
            else:
                self.lbl_stat_timer.setText("Inactive")
                self.lbl_stat_timer.setStyleSheet("color: #f38ba8; font-size: 13px; font-weight: bold;")
        except Exception as e:
            self.log(f"Error updating UI stats: {e}")
