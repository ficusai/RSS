# GUI Contract-Drift Test Suite — Complete Execution Plan

**Project:** RSS (`/home/ficus-pro/Documents/RSS`)
**Source under test:** 39 atomic GUI modules under `gui/_00_*` … `gui/_38_*`
**Target:** 39 dedicated test folders + scripts under `tests/`, mirroring `gui/` 1:1
**Git branch:** `feature/gui-contract-tests`
**Remote:** `https://github.com/ficusai/RSS.git`

---

## 1. Objective

Populate `/home/ficus-pro/Documents/RSS/tests/` with a dedicated folder **and** one test script per GUI module (39 folders total). The primary requirement is **contract-drift detection**: if *anything* in the source module changes (function signature, imports, constants, public members, widget names, labels, file paths), the test **must fail with an error** so the user is aware the codebase changed and can regenerate/replace that test.

**No tests are executed in this session** — files are created, committed to a new git branch, and pushed to remote.

---

## 2. Core Design — The Contract-Drift Pattern

Every test script asserts TWO layers:

### Layer 1 — Structural contract (drift detection)
Hard-coded snapshot of the module's public API. Any drift raises a descriptive `AssertionError`:

- **Exact function/class signature** via `inspect.signature()` — parameter names, kinds, defaults, return annotations.
- **Exact set of public callables** — a newly added or removed public function fails the test (signals a refactor).
- **Module-level constants** — exact expected values.
- **Import statements** — expected imports must be present in the module's source. Verified via **`ast.parse()` of the source file**, NOT grep (grep is brittle on multi-line/parenthesized imports).
- **File existence** — the GUI module file must still exist at its expected path (renamed/moved folder fails).
- **Import health** — `importlib.import_module` of the GUI module must succeed; a broken import fails immediately.

### Layer 2 — Behavioral smoke
Functional assertions on fixed inputs/outputs, widget attributes, and mocked side-effects, so *logic* changes that do not touch signatures also fail:

- Pure functions: exact outputs for fixed inputs + edge cases.
- Widget builders: exact column counts, header labels, placeholder texts, default values, button texts, widget objectNames, signal connections.
- Handlers/orchestrators: mocked dependencies (via `unittest.mock.patch` on the module's namespace), verifying call counts, argument forwarding, and state mutations.

---

## 3. Shared Helper — `tests/conftest.py`

Shared primitives so all 39 scripts stay small, consistent, and fail loudly:

- **Offscreen Qt enforcement — MUST be the very first statements in `conftest.py`**, before any PyQt6 import:

  ```python
  import os
  os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

  # Only now import PyQt6
  from PyQt6.QtWidgets import QApplication
  ```

  If any test file imports PyQt6 at module level before conftest runs, it fails in headless CI. Every test file that imports PyQt6 adds the comment `# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.` above the PyQt6 import.
- `qapp` fixture — one shared `QApplication` across the whole suite.
- `assert_signature(func, expected_params, expected_return)` — compares param **names, kinds, defaults** (`<required>` sentinel when default is empty) AND the **return annotation**; on drift raises an error naming the exact diff:

  ```python
  import inspect

  def assert_signature(func, expected_params, expected_return):
      sig = inspect.signature(func)
      actual_params = [
          (p.name, p.kind, p.default if p.default is not inspect.Parameter.empty else "<required>")
          for p in sig.parameters.values()
      ]
      actual_return = sig.return_annotation
      assert actual_params == expected_params, (
          f"SIGNATURE CHANGED for {func.__qualname__}:\n"
          f"  Expected params: {expected_params}\n"
          f"  Actual params:   {actual_params}\n"
          f"→ Regenerate this test file."
      )
      assert actual_return == expected_return, (
          f"RETURN ANNOTATION CHANGED for {func.__qualname__}:\n"
          f"  Expected: {expected_return}\n"
          f"  Actual:   {actual_return}\n"
          f"→ Regenerate this test file."
      )
  ```

  For PyQt6-bound methods (e.g., `QThread.__init__`), `inspect.signature` may return `(*args, **kwargs)` — assert on the **source signature we wrote** (`ScrapeThread.__init__`: `self, feeds, parent=None`), not the inherited one.
- `assert_constants(module, pairs)` — compares module constant values.
- `assert_source_imports(module_path, expected_imports)` — AST-based (NOT grep); parses source and collects every imported module via `ast.walk`, then asserts the expected set is a subset:

  ```python
  import ast

  def assert_source_imports(module_path: str, expected: set[str]):
      tree = ast.parse(open(module_path).read())
      found = set()
      for node in ast.walk(tree):
          if isinstance(node, ast.Import):
              for alias in node.names:
                  found.add(alias.name)
          elif isinstance(node, ast.ImportFrom):
              found.add(node.module)
      missing = expected - found
      assert not missing, (
          f"IMPORTS CHANGED in {module_path}:\n"
          f"  Expected: {sorted(expected)}\n"
          f"  Missing:  {sorted(missing)}\n"
          f"  Found:    {sorted(found)}\n"
          f"→ Source changed. Regenerate this test file."
      )
  ```
- `assert_callables(module, allowed)` — asserts the module's public callable set matches exactly, but **filters dunder (`__*`) and private (`_*`) names, AND imported names** (only names whose `__module__ == module.__name__` count — so re-exported symbols don't cause false drift):

  ```python
  def assert_callables(module, allowed: set[str]):
      defined = {
          name for name, obj in inspect.getmembers(module, inspect.isfunction)
          if obj.__module__ == module.__name__ and not name.startswith("_")
      }
      extra = defined - allowed
      assert not extra, (
          f"NEW PUBLIC CALLABLES in {module.__name__}: {sorted(extra)}\n"
          f"→ Refactor detected. Regenerate this test file."
      )
  ```
- `assert_signals(cls, expected_sigs)` — asserts pyqtSignal declarations (types + arg counts).
- `patch_constant(module, name, value)` — context-managed constant patch with auto-restore (used for `CONFIG_PATH` redirection to `TemporaryDirectory`).
- `WindowStub` helpers per category where needed (real Qt widgets + no-op slots required by builder modules).

**Note on workspace standard:** product code follows "one file per function"; test infrastructure may share `conftest.py` (standard pytest practice) to avoid 39× duplication.

---

## 4. Test File Map (tests/ — 1:1 with gui/)

### Naming rules (no exceptions)
- **Test folder naming:** mirror the GUI folder name **byte-for-byte** — no `test_` prefix, no renaming:
  `tests/_00_paths_config_constant_definitions/`, `tests/_01_window_stylesheet_dark_modern_theme/`, … , `tests/_38_bootstrap_launch_window/`. This keeps the 1:1 mapping obvious and grep-able.
- **Test script naming:** `test_<source_filename_without_.py>.py` — the **source module basename**, prefixed with `test_`. Example: source `add_feed_subscription.py` → test `test_add_feed_subscription.py`. No deviations.

| # | gui module folder | test folder under `tests/` | test script |
| :-- | :-- | :-- | :-- |
| 00 | `_00_paths_config_constant_definitions` | `_00_paths_config_constant_definitions/` | `test_paths_config_constants.py` |
| 01 | `_01_window_stylesheet_dark_modern_theme` | `_01_window_stylesheet_dark_modern_theme/` | `test_window_stylesheet_apply.py` |
| 02 | `_02_background_scrape_thread_worker` | `_02_background_scrape_thread_worker/` | `test_scrape_thread_worker.py` |
| 03 | `_03_ui_assembly_orchestrator` | `_03_ui_assembly_orchestrator/` | `test_build_main_window_ui.py` |
| 04 | `_04_ui_header_bar_top_section_build` | `_04_ui_header_bar_top_section_build/` | `test_build_header_bar.py` |
| 05 | `_05_ui_articles_explorer_tab_build` | `_05_ui_articles_explorer_tab_build/` | `test_build_articles_tab.py` |
| 06 | `_06_ui_subscriptions_hub_tab_build` | `_06_ui_subscriptions_hub_tab_build/` | `test_build_subscriptions_tab.py` |
| 07 | `_07_ui_operations_system_tab_build` | `_07_ui_operations_system_tab_build/` | `test_build_operations_tab.py` |
| 08 | `_08_ui_presets_library_tab_build` | `_08_ui_presets_library_tab_build/` | `test_build_presets_tab.py` |
| 09 | `_09_feed_identifier_generate_from_name` | `_09_feed_identifier_generate_from_name/` | `test_generate_feed_id.py` |
| 10 | `_10_log_append_timestamped_message` | `_10_log_append_timestamped_message/` | `test_append_timestamped_log.py` |
| 11 | `_11_log_clear_console` | `_11_log_clear_console/` | `test_clear_log_console.py` |
| 12 | `_12_add_drawer_toggle_visibility` | `_12_add_drawer_toggle_visibility/` | `test_toggle_add_drawer.py` |
| 13 | `_13_stats_badges_update_live` | `_13_stats_badges_update_live/` | `test_update_stats_badges.py` |
| 14 | `_14_feed_config_load_from_disk` | `_14_feed_config_load_from_disk/` | `test_load_feeds.py` |
| 15 | `_15_feed_config_save_to_disk` | `_15_feed_config_save_to_disk/` | `test_save_feeds.py` |
| 16 | `_16_refresh_all_views_pipeline` | `_16_refresh_all_views_pipeline/` | `test_refresh_all_views.py` |
| 17 | `_17_subscriptions_table_refresh_view` | `_17_subscriptions_table_refresh_view/` | `test_refresh_subscriptions_table.py` |
| 18 | `_18_articles_table_refresh_view` | `_18_articles_table_refresh_view/` | `test_refresh_articles_table.py` |
| 19 | `_19_feed_add_single_subscription` | `_19_feed_add_single_subscription/` | `test_add_feed_subscription.py` |
| 20 | `_20_feed_delete_subscription` | `_20_feed_delete_subscription/` | `test_delete_feed_subscription.py` |
| 21 | `_21_feed_toggle_enabled_state` | `_21_feed_toggle_enabled_state/` | `test_toggle_feed_state.py` |
| 22 | `_22_feed_update_interval_frequency` | `_22_feed_update_interval_frequency/` | `test_set_feed_frequency.py` |
| 23 | `_23_feed_ping_endpoint_single_scrape` | `_23_feed_ping_endpoint_single_scrape/` | `test_ping_feed_endpoint.py` |
| 24 | `_24_preset_quick_import_single_feed` | `_24_preset_quick_import_single_feed/` | `test_import_preset_feed.py` |
| 25 | `_25_article_selection_reader_update` | `_25_article_selection_reader_update/` | `test_on_article_selected.py` |
| 26 | `_26_article_link_open_in_browser` | `_26_article_link_open_in_browser/` | `test_open_article_in_browser.py` |
| 27 | `_27_article_link_copy_to_clipboard` | `_27_article_link_copy_to_clipboard/` | `test_copy_article_link.py` |
| 28 | `_28_systemd_status_refresh_daemon` | `_28_systemd_status_refresh_daemon/` | `test_refresh_systemd_status.py` |
| 29 | `_29_systemd_timer_install_handler` | `_29_systemd_timer_install_handler/` | `test_handle_install_systemd.py` |
| 30 | `_30_preset_categories_load_dropdown` | `_30_preset_categories_load_dropdown/` | `test_load_preset_categories.py` |
| 31 | `_31_presets_table_refresh_view` | `_31_presets_table_refresh_view/` | `test_refresh_presets_table.py` |
| 32 | `_32_preset_add_single_from_catalog` | `_32_preset_add_single_from_catalog/` | `test_add_preset_feed.py` |
| 33 | `_33_preset_add_all_bulk_import` | `_33_preset_add_all_bulk_import/` | `test_add_all_presets.py` |
| 34 | `_34_scrape_start_enabled_feeds` | `_34_scrape_start_enabled_feeds/` | `test_start_scrape.py` |
| 35 | `_35_scrape_run_background_orchestrator` | `_35_scrape_run_background_orchestrator/` | `test_run_scrape_background.py` |
| 36 | `_36_scrape_finished_signal_handler` | `_36_scrape_finished_signal_handler/` | `test_on_scrape_done.py` |
| 37 | `_37_main_window_facade_assembly` | `_37_main_window_facade_assembly/` | `test_main_window_facade.py` |
| 38 | `_38_bootstrap_launch_window` | `_38_bootstrap_launch_window/` | `test_bootstrap_launch_window.py` |

Existing `tests/*.py` core suites (test_rss, test_cache_manager, etc.) remain untouched.

---

## 5. Per-Module Contract & Smoke Assertions

### Category A — Constants (module _00)
- `PROJECT_ROOT == Path(__file__).resolve().parents[2]`
- `CONFIG_PATH == PROJECT_ROOT / "config" / "feeds.json"`
- `ASSETS_DIR == PROJECT_ROOT / "assets"`
- All three are `pathlib.Path` instances.
- No public callables expected.

### Category B — Pure/stdlib functions (_09, _10, _11, _12, _13, _14, _15)
- **`_09 generate_feed_id(name: str, fallback_seed: int) -> str`**
  - Signature exact. No extra public callables. Source contains `import re` + the slug regex literal `r"[^a-zA-Z0-9_]+"`.
  - Behavior: `"TechCrunch"→"techcrunch"`, `"BBC News"→"bbc_news"`, `"NASA!Science"→"nasa_science"`, `"!!!",5→"f5"`, `"",5→"f5"`, output matches `^[a-z0-9_]+$`.
- **`_10 append_log_message(window, msg: str) -> None`**
  - Signature exact. Source contains `strftime("%H:%M:%S")`.
  - Behavior (headless `QTextEdit` as `log_box`): appended line matches `^\[\d{2}:\d{2}:\d{2}\] test msg`; `verticalScrollBar().setValue(maximum())` invoked.
- **`_11 clear_log_console(window) -> None`**
  - Signature exact.
  - Behavior: pre-populated `log_box` → `toPlainText() == ""` after call.
- **`_12 toggle_add_drawer(window) -> None`**
  - Signature exact.
  - Behavior (real `QFrame` + `QPushButton`): first call → visible + text `"➖ Hide Drawer"`; second call → hidden + text `"➕ New Feed / Presets ▾"`.
- **`_13 update_stats_badges(window) -> None`**
  - Signature exact. Source imports `from core.storage import get_stats`.
  - Behavior: patch `get_stats` → `lbl_articles_stat == "📰 150 Articles"`, `lbl_feeds_stat == "📡 3/5 Feeds Active"`; patch to raise → badges unchanged.
- **`_14 load_feeds(window) -> None`**
  - Signature exact. Source imports `CONFIG_PATH` from `gui._00_...`.
  - Behavior with patched `CONFIG_PATH`: missing file → `feeds == []`; malformed JSON → `[]`; `{"feeds":[...]}` → list extracted; raw list → used directly.
- **`_15 save_feeds(window) -> None`**
  - Signature exact. Source imports `CONFIG_PATH` + `append_log_message`.
  - Behavior with patched `CONFIG_PATH` in `TemporaryDirectory`: `config/` auto-created; file parsed → `{"feeds": [...]}` with 2-space indent; error path logs via `append_log_message`.

### Category C — Widget builders (_04, _05, _06, _07, _08)
Each runs headless against a `WindowStub` providing the required no-op slots; asserts exact widget attributes + connections. Signature `build_*(window) -> None` exact.
- **`_04 build_header_bar(window)`**
  - Returns `QFrame` with `objectName == "card"`.
  - Creates `lbl_articles_stat`, `lbl_feeds_stat`, `btn_sync`.
  - `btn_sync.text() == "🔄 Sync All Feeds"`, `objectName == "accent"`, connected to `window.start_scrape`.
- **`_05 build_articles_tab(window)`**
  - `table_articles` columnCount 4, headers `["Article Title","Source Feed","Category","Date"]`, alternating rows, row height 50, hidden vertical header.
  - `input_search.placeholderText()` exact; `combo_cat` first item "All Categories"; `btn_refresh_view` connected to `window.refresh`.
  - `btn_copy_link` and `btn_open` disabled initially; `btn_open` objectName "primary_blue".
  - Reader widgets present; tab label exact `"📰 Articles Explorer"`; tab added to `window.tabs`.
- **`_06 build_subscriptions_tab(window)`**
  - `table_feeds` columnCount 6, headers `["Name","RSS Endpoint URL","Category","Interval","Active","Actions"]`, col width 0 == 190.
  - `drawer_box` hidden by default; `cb_freq` items `["1h","3h","6h","12h","24h"]` default index 3; `in_cat` default "General".
  - `btn_toggle_drawer` connected to `window.toggle_add_drawer`; `btn_add` connected to `window.add_feed`.
  - Preset chips: one `QPushButton` per `get_preset_feeds()` item with objectName "chip" + tooltip containing name/url/category; tab label `"📡 Subscriptions Hub"`.
- **`_07 build_operations_tab(window)`**
  - Systemd badge labels `lbl_sys_service`, `lbl_sys_timer`, `lbl_sys_enabled` created.
  - `log_box` `QTextEdit` created (objectName `log_console` style target).
  - Clear-log button connected to `window.clear_log`; install-timer button connected to `window.handle_install_systemd`; refresh-systemd button wired.
  - Tab label exact.
- **`_08 build_presets_tab(window)`**
  - `table_presets` columns + headers exact (5 columns).
  - `preset_combo_cat` created; "Import All" bulk button connected to `window.add_all_presets`.
  - `load_preset_categories` + `refresh_presets_table` wiring (buttons/proxies). Tab label exact.

### Category D — Orchestrators & refreshers (_02, _03, _16, _17, _18)
- **`_02 ScrapeThread(QThread)`**
  - Class exists, inherits `QThread`.
  - `log_signal = pyqtSignal(str)`; `finished_signal = pyqtSignal(int, int, list)`.
  - `__init__(self, feeds, parent=None)` exact; `run(self) -> None` returns None.
  - Source imports `fetch_all_feeds` + `save_articles`.
  - Behavior: construct with feeds → deepcopy isolation (mutating original after construction does not affect `thread.feeds`). No `.start()` — network avoided.
- **`_03 build_main_window_ui(window)`**
  - Signature exact. Patches `build_header_bar` + 4 tab builders; asserts each called exactly once.
  - `window.progress` exists, hidden, `setTextVisible(False)`.
  - `window.tabs` is a `QTabWidget`; 4 tabs added when real builders used (fallback: patch-driven count check).
- **`_16 refresh_window(window)`**
  - Signature exact. Source calls `refresh_subscriptions_table`, `refresh_articles_table`, `update_stats_badges`.
  - Behavior: patch the three in module namespace → all called exactly once.
- **`_17 refresh_subscriptions_table(window)`**
  - Signature exact; source imports save_feeds / delete_feed / toggle_feed / set_feed_frequency / ping_feed / generate_feed_id / get_category_color.
  - Behavior headless: 3-feed fixture → `table_feeds.rowCount() == 3`; correct cell texts; interval cell embeds `QComboBox` with 5 items; enabled cell `QCheckBox`; actions cell Ping + Delete `QPushButton`; `cb_cat_filter` rebuilt to "All Categories" + unique names with `blockSignals` guard; filters (search/category) respected.
- **`_18 refresh_articles_table(window)`**
  - Signature exact; source imports `load_articles` + `get_category_color`.
  - Behavior: patch `load_articles` returning fixtures → 4-col rows correct; `combo_cat` rebuilt with categories + `blockSignals`; `window.current_articles` set.

### Category E — Feed mutation handlers (_19, _20, _21, _22, _23, _24)
- **`_19 add_feed(window)`** — hooks `QMessageBox.warning`, `generate_feed_id`, `save_feeds`, `refresh_window`, `append_log_message` are patched.
  - Missing name/url → warning called, feeds unchanged.
  - Valid feed → appended dict with exact key set `{id,name,url,category,fetch_interval_hours,enabled}`; URL gets `https://` prefix when scheme-less; `save_feeds` + `refresh_window` called; fields cleared.
  - Duplicate URL (trailing-slash normalized) → not appended, log message emitted.
  - `h = [1,3,6,12,24][cb_freq.currentIndex()]` correct per index.
- **`_20 delete_feed(window, fid: str)`** — removes matching feed, `save_feeds` + `refresh_window` called; unknown id → no-op, no save.
- **`_21 toggle_feed(window, fid: str, on: bool)`** — sets `enabled`; `save_feeds` + `update_stats_badges` called; unknown id → no-op.
- **`_22 set_feed_frequency(window, fid: str, hours)`** — sets `fetch_interval_hours`; `save_feeds` called; unknown id → no-op.
- **`_23 ping_feed(window, fid: str)`** — `window.scrape_thread.isRunning()` False + feed found → `run_scrape(window, [target])` called; running thread → no-op; unknown id → no-op.
- **`_24 import_preset(window, name: str, url: str, category: str)`** — fills `in_name`/`in_url`/`in_cat`; calls `window.add_feed` exactly once.

### Category F — Article reader handlers (_25, _26, _27)
- **`_25 on_article_selected(window)`**
  - Source imports `calculate_reading_time_minutes`.
  - Behavior headless with real `QTableWidget` selection: reader title/meta/body populated from `window.current_articles`; `btn_open`/`btn_copy_link` enabled when URL present; URL stored as Qt property on buttons; meta includes feed/date/read time; empty/out-of-range selection → early return (no crash).
- **`_26 open_article_in_browser(window)`** — patch `QDesktopServices.openUrl`; `btn_open` property url set → called once with `QUrl(url)`; no property → not called.
- **`_27 copy_article_link(window)`** — patch `QMessageBox.information`; `btn_copy_link` property url → `QApplication.clipboard().text() == url`; `append_log_message` called; no property → not called.

### Category G — Systemd handlers (_28, _29)
- **`_28 refresh_systemd_status(window)`** — patch feature `get_timer_status` returning `{installed:True, active:True, enabled:True}` → badges text + green styles; False states → red/gray styles; raise → `append_log_message` called, badges unchanged.
- **`_29 handle_install_systemd(window)`** — patch `install_systemd_timer` success → `QMessageBox.information` + `refresh_systemd_status` called; failure → `QMessageBox.critical` called; logs emitted.

### Category H — Presets pipeline (_30, _31, _32, _33)
- **`_30 load_preset_categories(window)`** — patch feature function; dropdown = "All Categories" + sorted categories; `blockSignals` guard active during rebuild; previous selection restored when still present.
- **`_31 refresh_presets_table(window)`** — patch `get_presets_by_category`/`search_presets`/`feed_already_present`/`add_preset_feed`; 5-col rows; status cell "Subscribed" (green) vs "Available" (gray); Add `QPushButton` disabled when subscribed; search text drives `search_presets`.
- **`_32 add_preset_feed(window, preset)`** — already-present → skip + log; valid → appended dict exact keys, `save_feeds`/`refresh_window`/`refresh_presets_table` called; name/url stripped, empty → no-op.
- **`_33 add_all_presets(window)`** — patch `get_preset_feeds` (n fixtures incl. 1 duplicate, 1 empty) → correct added count; appended dicts valid; `save_feeds` + `refresh_window` + `refresh_presets_table` called; info dialog with count; log "Preset import complete: N new feed(s) added."

### Category I — Scrape orchestration (_34, _35, _36)
- **`_34 start_scrape(window)`** — running thread → no-op; no enabled feeds → `QMessageBox.information("No Active Subscriptions", …)`; enabled feeds → `run_scrape(window, enabled_only)` called with full list.
- **`_35 run_scrape(window, feeds)`** — patch `ScrapeThread` to a Mock; asserts `btn_sync` disabled + text `"⏳ Syncing..."`; `progress` shown with `setRange(0, 0)`; `log_signal` → `append_log_message`; `finished_signal` → `on_scrape_done`; `ScrapeThread(feeds)` constructed once; `.start()` called.
- **`_36 on_scrape_done(window, new, total, errors)`** — `btn_sync` re-enabled + text `"🔄 Sync All Feeds"`; progress hidden; log "Scrape job complete: +{new} new article(s) added. Total database count: {total}."; errors non-empty → "Encountered {n} feed fetching issue(s)."; `update_stats_badges` + `refresh_articles_table` called.

### Category J — Facade & bootstrap (_37, _38)
- **`_37 MainWindow(QMainWindow)`**
  - Class inherits `QMainWindow`.
  - **Assert the EXACT method set** (including underscore helpers). Any added/removed method fails — this is the strongest refactor detector:

    ```python
    EXPECTED_METHODS = {
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
    ```
  - Each delegate method's source body verified for its target module path (`gui._NN_...`).
  - Headless instantiation smoke: window title exact, size 1280×840 (min 980×700), `feeds == []`, `scrape_thread is None`, `tabs.count() == 4`, `CONFIG_PATH` constant used for config.
- **`_38 launch_gui_window() -> int`**
  - **Structural ONLY — do NOT call `launch_gui_window()`** (it starts an event loop and blocks). Assert the source guard instead:

    ```python
    def test_launch_gui_window_structure():
        import gui._38_bootstrap_launch_window.bootstrap_launch_window as mod
        sig = inspect.signature(mod.launch_gui_window)
        assert sig.return_annotation is int
        src = open(mod.__file__).read()
        assert "sys.exit(app.exec())" in src, "Entry point guard changed"
        assert "QApplication(sys.argv)" in src, "QApplication construction changed"
        assert "MainWindow()" in src, "MainWindow instantiation changed"
    ```
  - Source imports `QApplication` + `MainWindow` + `sys`; no extra public callables.

---

## 6. Test Style Conventions

- Pytest style: `def test_*` + bare `assert` (consistent with `tests/test_stealth_fetcher.py`).
- Run command (matching SCRIPT-project GUI pattern): `QT_QPA_PLATFORM=offscreen pytest tests/` or `python3 -m pytest tests/_NN_.../ -v` per folder.
- **Every test file starts with a contract header docstring** — makes the "always show me an error" requirement self-documenting:

  ```python
  """
  CONTRACT SNAPSHOT — do not edit by hand.

  Source: gui/_NN_.../module.py
  Generated against branch: feature/gui-contract-tests

  If this test fails, the source module has drifted from its contract.
  Do NOT patch this test. Instead:
    1. Inspect the source change.
    2. If intentional, regenerate this test file.
    3. If unintentional, revert the source change.
  """
  ```

- Every test module also carries the project's docstring convention (`# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:`).
- Any PyQt6 import in a test file is preceded by `# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.`
- All drift assertions raise `AssertionError` messages prefixed `CONTRACT DRIFT — <module>: regenerate test (reason: ...)`.
- Network, real systemd, and real browser/clipboard are always mocked — tests are offline and deterministic.

---

## 7. Git & Release Workflow

1. **Branch creation:** `git checkout -b feature/gui-contract-tests` (from current `feature/gui-atomic-modular-refactor` state; carries existing uncommitted changes in the working tree).
2. **Implement:** write `tests/conftest.py` + 39 test folders/scripts.
3. **README sync (mandatory per AGENTS.md):**
   - Add branch-map row: `feature/gui-contract-tests` | Contract-drift test suite for the 39 atomic GUI modules.
   - Add `#### feature/gui-contract-tests` table under `## Branch-Related File Changes` listing every added file with a one-line description.
4. **Commit scope (user decision):** ONLY new `tests/` folders/scripts + `README.md`.
   Stage precisely:
   ```bash
   git add tests/ README.md
   ```
   Commit with an explicit message:
   ```bash
   git commit -m "test: add contract-drift test suite for all 39 GUI atomic modules

   - Add tests/conftest.py with shared contract-diff helpers
   - Add 39 test folders mirroring gui/_00_* through gui/_38_*
   - Each test asserts structural contract (exact signatures, public
     callables, constants, AST-verified imports, file existence) plus
     behavioral smoke tests
   - Any source drift fails with a descriptive error naming the drift
   - No tests executed in this session

   Branch: feature/gui-contract-tests"
   ```
5. **No test execution this session** (user instruction).
6. **Push:** `git push -u origin feature/gui-contract-tests`.

**Note:** The uncommitted `feature/gui-atomic-modular-refactor` changes remain in the working tree on the new branch (uncommitted). That's intentional — only the new test scripts are committed.

---

## 8. Final Pre-flight Checklist

| # | Check |
| :-- | :-- |
| 1 | 39 test folders mirror `gui/_00_*` … `gui/_38_*` byte-for-byte |
| 2 | Each folder has exactly one `test_<source_filename>.py` (source basename + `test_` prefix) |
| 3 | `tests/conftest.py` sets `QT_QPA_PLATFORM=offscreen` before any PyQt6 import |
| 4 | Every test file has the CONTRACT SNAPSHOT docstring |
| 5 | Imports verified via `ast.parse`, not grep |
| 6 | Signatures include param names, kinds, defaults, and return annotation |
| 7 | `assert_callables` filters dunders, privates, and imported names |
| 8 | `_37` asserts exact method set (incl. `_log`, `_run_scrape`) |
| 9 | `_38` structural only — no `app.exec()` call in tests |
| 10 | Commit scope = `tests/` + `README.md` only |
| 11 | No tests executed this session |
| 12 | Branch name = `feature/gui-contract-tests` |

---

## 9. Deliverables Summary

- `tests/conftest.py` (shared contract-diff helpers + offscreen Qt fixture)
- 39 new test folders under `tests/` (mirroring `gui/_00_*`…`gui/_38_*`), one pytest script each
- `README.md` updated (branch map + Branch-Related File Changes)
- New branch `feature/gui-contract-tests` committed locally and pushed to `origin`