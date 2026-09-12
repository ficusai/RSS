"""MainWindow delegating facade — thin QMainWindow with all logic in atomic modules."""
# WHAT: Re-exports the real MainWindow class that delegates every method to an atomic module.
#       Keeps Qt signal typing coherent (self.btn_x.clicked.connect(self.method)).
# OPTIONS: N/A — constructor orchestration is internal.
# DEFAULTS: Window opens at 1280x840, min 980x700.
# OUTPUT/EFFECT: A fully functional PyQt6 QMainWindow.
# ERRORS/EDGE CASES: Import-time failures if PyQt6 or core features are missing.
# HOW TO TEST: QT_QPA_PLATFORM=offscreen python3 -c "from gui._37_main_window_facade_assembly.main_window_facade import MainWindow; from PyQt6.QtWidgets import QApplication; app=QApplication([]); w=MainWindow(); print('tabs=', w.tabs.count())"
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow

from gui._00_paths_config_constant_definitions.paths_config_constants import ASSETS_DIR, CONFIG_PATH
from gui._01_window_stylesheet_dark_modern_theme.window_stylesheet_apply import apply_window_stylesheet
from gui._03_ui_assembly_orchestrator.build_main_window_ui import build_main_window_ui
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message
from gui._14_feed_config_load_from_disk.load_feeds import load_feeds
from gui._16_refresh_all_views_pipeline.refresh_all_views import refresh_window
from gui._28_systemd_status_refresh_daemon.refresh_systemd_status import refresh_systemd_status


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

        apply_window_stylesheet(self)
        build_main_window_ui(self)
        load_feeds(self)
        refresh_window(self)
        refresh_systemd_status(self)
        append_log_message(self, "RSS Engine initialized and ready.")

    # --- UI builders (1-line delegators) ---
    def build_main_window_ui(self):
        from gui._03_ui_assembly_orchestrator.build_main_window_ui import build_main_window_ui
        build_main_window_ui(self)

    def build_header_bar(self):
        from gui._04_ui_header_bar_top_section_build.build_header_bar import build_header_bar
        build_header_bar(self)

    def build_articles_tab(self):
        from gui._05_ui_articles_explorer_tab_build.build_articles_tab import build_articles_tab
        build_articles_tab(self)

    def build_subscriptions_tab(self):
        from gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab import build_subscriptions_tab
        build_subscriptions_tab(self)

    def build_operations_tab(self):
        from gui._07_ui_operations_system_tab_build.build_operations_tab import build_operations_tab
        build_operations_tab(self)

    def build_presets_tab(self):
        from gui._08_ui_presets_library_tab_build.build_presets_tab import build_presets_tab
        build_presets_tab(self)

    # --- Utilities ---
    def toggle_add_drawer(self):
        from gui._12_add_drawer_toggle_visibility.toggle_add_drawer import toggle_add_drawer
        toggle_add_drawer(self)

    def toggle_url_column(self):
        from gui._39_toggle_url_column_visibility.toggle_url_column import toggle_url_column
        toggle_url_column(self)

    def _log(self, msg):
        append_log_message(self, msg)

    def clear_log(self):
        from gui._11_log_clear_console.clear_log_console import clear_log_console
        clear_log_console(self)

    # --- Config ---
    def load_feeds(self):
        load_feeds(self)

    def save_feeds(self):
        from gui._15_feed_config_save_to_disk.save_feeds import save_feeds
        save_feeds(self)

    # --- Refresh ---
    def refresh(self):
        refresh_window(self)

    def update_stats(self):
        from gui._13_stats_badges_update_live.update_stats_badges import update_stats_badges
        update_stats_badges(self)

    def refresh_table(self):
        from gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table import refresh_subscriptions_table
        refresh_subscriptions_table(self)

    def refresh_articles(self):
        from gui._18_articles_table_refresh_view.refresh_articles_table import refresh_articles_table
        refresh_articles_table(self)

    # --- Subscription CRUD ---
    def add_feed(self):
        from gui._19_feed_add_single_subscription.add_feed_subscription import add_feed
        add_feed(self)

    def delete_feed(self, fid):
        from gui._20_feed_delete_subscription.delete_feed_subscription import delete_feed
        delete_feed(self, fid)

    def toggle(self, fid, on):
        from gui._21_feed_toggle_enabled_state.toggle_feed_state import toggle_feed
        toggle_feed(self, fid, on)

    def set_freq(self, fid, hours):
        from gui._22_feed_update_interval_frequency.set_feed_frequency import set_feed_frequency
        set_feed_frequency(self, fid, hours)

    def ping(self, fid):
        from gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint import ping_feed
        ping_feed(self, fid)

    def import_preset(self, name, url, category):
        from gui._24_preset_quick_import_single_feed.import_preset_feed import import_preset
        import_preset(self, name, url, category)

    # --- Article reader ---
    def on_article_sel(self):
        from gui._25_article_selection_reader_update.on_article_selected import on_article_selected
        on_article_selected(self)

    def open_browser(self):
        from gui._26_article_link_open_in_browser.open_article_in_browser import open_article_in_browser
        open_article_in_browser(self)

    def copy_article_link(self):
        from gui._27_article_link_copy_to_clipboard.copy_article_link import copy_article_link
        copy_article_link(self)

    # --- Systemd ---
    def refresh_systemd_status(self):
        refresh_systemd_status(self)

    def handle_install_systemd(self):
        from gui._29_systemd_timer_install_handler.handle_install_systemd import handle_install_systemd
        handle_install_systemd(self)

    # --- Presets ---
    def load_preset_categories(self):
        from gui._30_preset_categories_load_dropdown.load_preset_categories import load_preset_categories
        load_preset_categories(self)

    def refresh_presets_table(self):
        from gui._31_presets_table_refresh_view.refresh_presets_table import refresh_presets_table
        refresh_presets_table(self)

    def add_preset_feed(self, preset):
        from gui._32_preset_add_single_from_catalog.add_preset_feed import add_preset_feed
        add_preset_feed(self, preset)

    def add_all_presets(self):
        from gui._33_preset_add_all_bulk_import.add_all_presets import add_all_presets
        add_all_presets(self)

    # --- Scrape ---
    def start_scrape(self):
        from gui._34_scrape_start_enabled_feeds.start_scrape import start_scrape
        start_scrape(self)

    def _run_scrape(self, feeds):
        from gui._35_scrape_run_background_orchestrator.run_scrape_background import run_scrape
        run_scrape(self, feeds)

    def on_done(self, new, total, errors):
        from gui._36_scrape_finished_signal_handler.on_scrape_done import on_scrape_done
        on_scrape_done(self, new, total, errors)
