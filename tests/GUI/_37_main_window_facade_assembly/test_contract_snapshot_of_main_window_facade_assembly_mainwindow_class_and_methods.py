"""Contract snapshot: gui/_37_main_window_facade_assembly/main_window_facade.py v1.0.0

Structural contract:
  - Class: MainWindow(QMainWindow)
  - EXACT_METHODS set defined in this test for drift detection
  - Each delegate method verifies its source import path points to gui._NN_...
"""
# ==============================================================================
# WHAT: Verifies the MainWindow facade contract — exact method set, delegation
#       paths, and headless instantiation smoke test (title, size, tabs, config).
#
# OPTIONS:
#   window: MainWindow instance created headlessly (QT_QPA_PLATFORM=offscreen).
#
# DEFAULTS: Window title "RSS Feed Tracker & Scraping Dashboard", size 1280×840,
#           min 980×700, 4 tabs, feeds=[], scrape_thread=None.
#
# OUTPUT/EFFECT: Fully instantiated MainWindow with all facade methods bound.
#
# ERRORS/EDGE CASES: Missing PyQt6 → ImportError at import time.
#
# HOW TO TEST: QT_QPA_PLATFORM=offscreen python3 -m pytest tests/GUI/_37_main_window_facade_assembly/test_main_window_facade.py
# ==============================================================================
import pytest
import inspect
import os

# offscreen platform required for all PyQt6 widget testing
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform


@pytest.fixture(scope="module")
def qapp():
    """Create a single QApplication instance for the module."""
    app = QApplication([])
    yield app


# Exact expected method set for MainWindow facade
EXPECTED_METHODS = {
    "__init__",
    "build_main_window_ui", "build_header_bar", "build_articles_tab",
    "build_subscriptions_tab", "build_operations_tab", "build_presets_tab",
    "toggle_add_drawer", "_log", "clear_log", "load_feeds", "save_feeds",
    "refresh", "update_stats", "refresh_table", "refresh_articles",
    "add_feed", "delete_feed", "toggle", "set_freq", "ping",
    "import_preset", "on_article_sel", "open_browser", "copy_article_link",
    "refresh_systemd_status", "handle_install_systemd",
    "load_preset_categories", "refresh_presets_table",
    "add_preset_feed", "add_all_presets", "start_scrape", "_run_scrape",
    "on_done",
}

# Mapping of method → expected source module path fragment
METHOD_SOURCE_MAP = {
    "build_main_window_ui": "gui._03_ui_assembly_orchestrator.build_main_window_ui",
    "build_header_bar": "gui._04_ui_header_bar_top_section_build.build_header_bar",
    "build_articles_tab": "gui._05_ui_articles_explorer_tab_build.build_articles_tab",
    "build_subscriptions_tab": "gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab",
    "build_operations_tab": "gui._07_ui_operations_system_tab_build.build_operations_tab",
    "build_presets_tab": "gui._08_ui_presets_library_tab_build.build_presets_tab",
    "toggle_add_drawer": "gui._12_add_drawer_toggle_visibility.toggle_add_drawer",
    "_log": "gui._10_log_append_timestamped_message.append_timestamped_log",
    "clear_log": "gui._11_log_clear_console.clear_log_console",
    "load_feeds": "gui._14_feed_config_load_from_disk.load_feeds",
    "save_feeds": "gui._15_feed_config_save_to_disk.save_feeds",
    "refresh": "gui._16_refresh_all_views_pipeline.refresh_all_views",
    "update_stats": "gui._13_stats_badges_update_live.update_stats_badges",
    "refresh_table": "gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table",
    "refresh_articles": "gui._18_articles_table_refresh_view.refresh_articles_table",
    "add_feed": "gui._19_feed_add_single_subscription.add_feed_subscription",
    "delete_feed": "gui._20_feed_delete_subscription.delete_feed_subscription",
    "toggle": "gui._21_feed_toggle_enabled_state.toggle_feed_state",
    "set_freq": "gui._22_feed_update_interval_frequency.set_feed_frequency",
    "ping": "gui._23_feed_ping_endpoint_single_scrape.ping_feed_endpoint",
    "import_preset": "gui._24_preset_quick_import_single_feed.import_preset_feed",
    "on_article_sel": "gui._25_article_selection_reader_update.on_article_selected",
    "open_browser": "gui._26_article_link_open_in_browser.open_article_in_browser",
    "copy_article_link": "gui._27_article_link_copy_to_clipboard.copy_article_link",
    "refresh_systemd_status": "gui._28_systemd_status_refresh_daemon.refresh_systemd_status",
    "handle_install_systemd": "gui._29_systemd_timer_install_handler.handle_install_systemd",
    "load_preset_categories": "gui._30_preset_categories_load_dropdown.load_preset_categories",
    "refresh_presets_table": "gui._31_presets_table_refresh_view.refresh_presets_table",
    "add_preset_feed": "gui._32_preset_add_single_from_catalog.add_preset_feed",
    "add_all_presets": "gui._33_preset_add_all_bulk_import.add_all_presets",
    "start_scrape": "gui._34_scrape_start_enabled_feeds.start_scrape",
    "_run_scrape": "gui._35_scrape_run_background_orchestrator.run_scrape_background",
    "on_done": "gui._36_scrape_finished_signal_handler.on_scrape_done",
}


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_class_exists_and_inherits_qmainwindow(self):
        """MainWindow is a class inheriting from QMainWindow."""
        from PyQt6.QtWidgets import QMainWindow
        from gui._37_main_window_facade_assembly.main_window_facade import MainWindow
        assert issubclass(MainWindow, QMainWindow)

    def test_expected_methods_exact(self):
        """MainWindow defines exactly the EXPECTED_METHODS set — no more, no less."""
        from gui._37_main_window_facade_assembly.main_window_facade import MainWindow
        actual = {name for name, _ in inspect.getmembers(MainWindow, predicate=inspect.isfunction)}
        extra = actual - EXPECTED_METHODS
        missing = EXPECTED_METHODS - actual
        assert not extra, f"CONTRACT DRIFT — unexpected methods: {sorted(extra)}"
        assert not missing, f"CONTRACT DRIFT — missing methods: {sorted(missing)}"

    def test_method_source_paths(self):
        """Each delegate method imports from the correct gui._NN_... module."""
        from gui._37_main_window_facade_assembly.main_window_facade import MainWindow
        import importlib.util
        class_origin = importlib.util.find_spec(
            "gui._37_main_window_facade_assembly.main_window_facade"
        ).origin
        class_source = open(class_origin).read()
        for method_name, expected_path in METHOD_SOURCE_MAP.items():
            method = getattr(MainWindow, method_name)
            source = inspect.getsource(method)
            if expected_path not in source:
                assert expected_path in class_source, (
                    f"CONTRACT DRIFT — method '{method_name}' does not import from {expected_path}\n"
                    f"Method source:\n{source}"
                )

    def test_source_imports(self):
        """Source must import QMainWindow, QIcon, and core GUI modules."""
        from tests.GUI.conftest import assert_source_imports
        import importlib.util
        spec = importlib.util.find_spec("gui._37_main_window_facade_assembly.main_window_facade")
        assert spec is not None
        assert_source_imports(
            spec.origin,
            {
                "PyQt6.QtGui",
                "PyQt6.QtWidgets",
                "gui._00_paths_config_constant_definitions.paths_config_constants",
                "gui._01_window_stylesheet_dark_modern_theme.window_stylesheet_apply",
                "gui._03_ui_assembly_orchestrator.build_main_window_ui",
                "gui._10_log_append_timestamped_message.append_timestamped_log",
                "gui._14_feed_config_load_from_disk.load_feeds",
                "gui._16_refresh_all_views_pipeline.refresh_all_views",
                "gui._28_systemd_status_refresh_daemon.refresh_systemd_status",
            },
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real MainWindow."""

    def test_headless_instantiation(self, qapp):
        """Main window creates with correct title, size, tabs, feeds, config_path."""
        from gui._37_main_window_facade_assembly.main_window_facade import MainWindow
        from gui._00_paths_config_constant_definitions.paths_config_constants import CONFIG_PATH
        from unittest.mock import patch

        with patch("gui._37_main_window_facade_assembly.main_window_facade.load_feeds"):
            w = MainWindow()
        assert w.windowTitle() == "RSS Feed Tracker & Scraping Dashboard"
        assert w.width() == 1280
        assert w.height() == 840
        assert w.minimumWidth() == 980
        assert w.minimumHeight() == 700
        assert w.feeds == []
        assert w.scrape_thread is None
        assert w.tabs.count() == 4
        assert w.config_path == CONFIG_PATH
