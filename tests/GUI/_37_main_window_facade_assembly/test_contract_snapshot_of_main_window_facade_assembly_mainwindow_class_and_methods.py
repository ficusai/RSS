"""
==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the MainWindow facade class — the thin QMainWindow subclass
that delegates every GUI operation to an atomic module. It checks:
  - MainWindow inherits from QMainWindow
  - The exact set of public methods matches the expected facade contract
  - Each delegate method imports from the correct gui._NN_... source module
  - Headless instantiation creates a window with correct title, size, tabs,
    empty feeds list, and config path

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_class_exists_and_inherits_qmainwindow : MainWindow is a class
                                                  inheriting from QMainWindow
  - test_expected_methods_exact                : MainWindow defines exactly the
                                                  EXPECTED_METHODS set — no more,
                                                  no less
  - test_method_source_paths                   : Each delegate method imports
                                                  from the correct gui._NN_... module
  - test_source_imports                        : Source imports QMainWindow,
                                                  QIcon, and core GUI modules

Layer 2 (Behavioral):
  - test_headless_instantiation : MainWindow creates with correct title, size,
                                   tabs, empty feeds, and config_path

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# pytest: Test framework; provides the @pytest.fixture decorator for the qapp
#         singleton that all PyQt6 widget tests share.
import pytest
# inspect: Examines class members (methods, functions) and function signatures
#          for structural contract verification.
import inspect
# os: Sets the QT_QPA_PLATFORM environment variable to "offscreen" before any
#     PyQt6 import, enabling headless GUI testing without a display server.
import os

# offscreen platform required for all PyQt6 widget testing
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform


@pytest.fixture(scope="module")
def qapp():
    """Provide one shared QApplication for the whole module.

    WHAT: Creates a single Qt application object so MainWindow can be
          instantiated in headless (offscreen) mode without a real display.

    OPTIONS: scope="module" — one instance shared by every test in this file.

    DEFAULTS: Qt runs in offscreen mode (no visible window).

    OUTPUT/EFFECT: Yields a QApplication; Qt cleans it up after the tests run.

    ERRORS/EDGE CASES: Creating two QApplication objects in one process crashes
                       Qt, so exactly one is shared at module scope.
    """
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
    """Structural / signature / import contract checks.

    These tests inspect the MainWindow class structure without instantiating it.
    They fail if the class hierarchy, method set, or delegation paths drift
    from the expected facade contract.
    """

    def test_class_exists_and_inherits_qmainwindow(self):
        """Layer 1 — MainWindow inherits from QMainWindow.

        WHAT: Confirms that MainWindow is a subclass of PyQt6's QMainWindow,
              which provides the base window functionality (title bar, menu bar,
              toolbars, status bar, central widget area).

        WHY INHERIT QMainWindow:
          The RSS app needs a full-featured main window with tabs, toolbars, and
          a central widget area. QMainWindow is the standard Qt class for this.

        OPTIONS: None — must inherit from QMainWindow.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when issubclass(MainWindow, QMainWindow) is True.

        ERRORS/EDGE CASES:
          - Wrong base class: issubclass assertion fails
          - MainWindow not a class: AttributeError on getattr

        HOW TO TEST: Change `class MainWindow(QMainWindow)` to
                     `class MainWindow(object)` in the source, then run —
                     the issubclass check should fail.
        """
        from PyQt6.QtWidgets import QMainWindow
        from gui._37_main_window_facade_assembly.main_window_facade import MainWindow
        assert issubclass(MainWindow, QMainWindow)

    def test_expected_methods_exact(self):
        """Layer 1 — MainWindow defines exactly the EXPECTED_METHODS set.

        WHAT: Verifies that MainWindow has exactly the methods listed in
              EXPECTED_METHODS — no extra methods and no missing ones. This
              detects both accidental method additions and unintentional removals.

        WHY EXACT SET:
          The facade pattern requires a known set of bound methods for Qt signal
          connections. Adding a method changes the public API; removing one
          breaks existing signal connections.

        OPTIONS: EXPECTED_METHODS must match exactly — same count, same names.

        DEFAULTS: 35 methods total (including __init__).

        OUTPUT/EFFECT: Passes when actual methods == EXPECTED_METHODS exactly.

        ERRORS/EDGE CASES:
          - Extra method: "CONTRACT DRIFT — unexpected methods: [...]"
          - Missing method: "CONTRACT DRIFT — missing methods: [...]"

        HOW TO TEST: Add a new method to MainWindow in the source, then run —
                     the test should fail with "unexpected methods: ['new_method']".
        """
        from gui._37_main_window_facade_assembly.main_window_facade import MainWindow
        actual = {name for name, _ in inspect.getmembers(MainWindow, predicate=inspect.isfunction)}
        extra = actual - EXPECTED_METHODS
        missing = EXPECTED_METHODS - actual
        assert not extra, f"CONTRACT DRIFT — unexpected methods: {sorted(extra)}"
        assert not missing, f"CONTRACT DRIFT — missing methods: {sorted(missing)}"

    def test_method_source_paths(self):
        """Layer 1 — each delegate method imports from the correct gui._NN_... module.

        WHAT: For every method in METHOD_SOURCE_MAP, verifies that the method's
              source code contains the expected import path. Some methods use
              inline imports (inside the method body); others use module-level
              imports (at the top of the file). This test checks both locations.

        WHY DELEGATION PATHS:
          The facade pattern requires each method to delegate to exactly one
          atomic module. If a method starts importing from a different module,
          the architectural contract has drifted.

        OPTIONS: Each method must import from its mapped gui._NN_... path.

        DEFAULTS: 34 method-to-module mappings in METHOD_SOURCE_MAP.

        OUTPUT/EFFECT: Passes when every method's source contains its expected path.

        ERRORS/EDGE CASES:
          - Wrong import path: "CONTRACT DRIFT — method 'X' does not import from Y"

        HOW TO TEST: Change the import in build_header_bar to point to a
                     different module, then run — the test should fail on that
                     method's assertion.
        """
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
        """Layer 1 — source imports QMainWindow, QIcon, and core GUI modules.

        WHAT: Verifies the MainWindow source file imports the essential modules
              needed for the facade: PyQt6 Qt classes, path constants, stylesheet
              apply, UI assembly, logging, feed loading, view refreshing, and
              systemd status.

        WHY THESE IMPORTS:
          MainWindow cannot function without QMainWindow (base class), QIcon
          (window icon), path constants (config/assets paths), and the core
          GUI modules it delegates to during startup.

        OPTIONS: Expected set is exactly the eight modules listed above.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when all eight imports exist in the source.

        ERRORS/EDGE CASES:
          - Missing import: "CONTRACT DRIFT — imports in ..." naming the module

        HOW TO TEST: Remove one import from the source, then run —
                     it should fail and name the missing module.
        """
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
    """Behavioral smoke tests against the real MainWindow class.

    These tests instantiate the actual MainWindow (headlessly) and verify
    that its runtime properties match the expected contract.
    """

    def test_headless_instantiation(self, qapp):
        """Layer 2 — main window creates with correct title, size, tabs, feeds, config.

        WHAT: Creates a MainWindow instance in headless mode and verifies:
          - Window title is "RSS Feed Tracker & Scraping Dashboard"
          - Initial size is 1280x840 pixels
          - Minimum size is 980x700 pixels
          - feeds list is empty (load_feeds is patched to prevent disk read)
          - scrape_thread is None (no background task running)
          - 4 tabs are present (header + subscriptions + articles + operations + presets)
          - config_path points to the canonical feeds.json location

        WHY PATCH load_feeds:
          The real load_feeds reads from disk and may populate feeds with
          existing data. We patch it to ensure a deterministic test that
          verifies the initial state before any data loading occurs.

        OPTIONS:
          - qapp fixture provides the headless Qt context
          - load_feeds is patched to a no-op

        DEFAULTS: Title, size, and min-size are set in MainWindow.__init__.

        OUTPUT/EFFECT: All asserted properties match the expected contract.

        ERRORS/EDGE CASES:
          - Wrong title: windowTitle() assertion fails
          - Wrong size: width()/height() assertions fail
          - Non-empty feeds: load_feeds patch not applied correctly

        HOW TO TEST: Change the window title in MainWindow.__init__ to something
                     else, then run — the windowTitle() assertion should fail.
        """
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
