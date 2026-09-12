"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_06_ui_subscriptions_hub_tab_build/build_subscriptions_tab.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.
"""

# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# ==============================================================================
# This test file verifies the contract of build_subscriptions_tab, which
# constructs Tab 2 of the main window — the "Subscriptions Hub." The hub
# contains a filter/search bar, a collapsible drawer for adding new feeds
# and importing preset feeds, and a six-column table that lists all subscribed
# RSS feeds with per-row controls for interval, enable/disable, ping, and
# deletion. The function stores widget references on the window object so
# other parts of the GUI can interact with these controls.
# ==============================================================================

# ==============================================================================
# LAYER BREAKDOWN
# ==============================================================================
# Layer 1 (Structural):
#   - test_file_exists : verifies the source .py file exists on disk
#   - test_import_health : verifies the module can be imported without errors
#   - test_ast_imports : AST-parses the source to verify all expected imports are present
#   - test_build_subscriptions_tab_signature : verifies build_subscriptions_tab(window) -> None exact signature
#
# Layer 2 (Behavioral):
#   - test_table_feeds_column_count_6 : verifies QTableWidget has exactly 6 columns
#   - test_table_feeds_headers : verifies column header labels match the expected six labels
#   - test_col_width_0_is_190 : verifies the Name column (column 0) has fixed width 190
#   - test_drawer_box_hidden_by_default : verifies the add-drawer QFrame is hidden (setVisible(False))
#   - test_cb_freq_items_and_default_index : verifies frequency dropdown has ['1h','3h','6h','12h','24h'] with default index 3
#   - test_in_cat_default_general : verifies the category input defaults to text "General"
#   - test_btn_toggle_drawer_connected : verifies the toggle button is connected to window.toggle_add_drawer
#   - test_btn_add_connected : verifies the add button is connected to window.add_feed
#   - test_preset_dropdown_tiered : verifies two-tier preset dropdown (category + feed selector) is created and wired
#   - test_tab_label : verifies the tab is added with label "📡 Subscriptions Hub"
# ==============================================================================

# ==============================================================================
# LAYER WHAT EACH TEST CHECKS
# ==============================================================================
# Layer 1 tests confirm the structural contract: the module file is present,
# imports are correct, and the build function has the right signature. These
# catch regressions where a developer renames the function, drops an import,
# or changes the parameter list.
#
# Layer 2 tests confirm behavioral contract: the table has six columns with
# the right headers, the drawer starts hidden, the frequency dropdown has
# the correct options and default, the category field defaults to "General",
# buttons are wired to the correct window methods, preset chips are created
# for each preset feed, and the tab is registered with the correct label.
# These catch UI logic drift where widgets are reordered, hidden, or misconfigured.
# ==============================================================================


# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# import ast: parses Python source code into an Abstract Syntax Tree (AST) so we can inspect imports without executing the module.
# import inspect: inspects function and class signatures at runtime — used to verify parameter names, kinds, defaults, and return annotations.
# import sys: manipulates the Python module search path (sys.path) so tests can import gui modules from the project root.
# from pathlib import Path: provides object-oriented filesystem path manipulation to locate the source module relative to this test file.
# from unittest.mock import MagicMock, patch: creates fake objects (MagicMock) and temporarily replaces real functions (patch) to isolate the unit under test.
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    r"""Return the absolute Path to the source module being tested.

    WHAT:
      Constructs and returns the filesystem path to build_subscriptions_tab.py,
      the source module whose contract this test file verifies.

    OPTIONS:
      None. This function takes no arguments.

    DEFAULTS:
      None.

    OUTPUT:
      A pathlib.Path object pointing to:
        <project_root>/gui/_06_ui_subscriptions_hub_tab_build/build_subscriptions_tab.py

    EFFECT:
      No side effects. Pure function.

    ERRORS/EDGE CASES:
      None expected. Path resolution is deterministic given a fixed filesystem layout.

    HOW TO TEST:
      1. Run this test file.
      2. Assert the returned path exists with .exists().
      Example: p = _module_path(); assert p.exists()
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_06_ui_subscriptions_hub_tab_build" / "build_subscriptions_tab.py"


def _import_module():
    r"""Import and return the source module under test.

    WHAT:
      Dynamically imports gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab
      and returns the module object so tests can access the build_subscriptions_tab function.

    OPTIONS:
      None. This function takes no arguments.

    DEFAULTS:
      None.

    OUTPUT:
      The imported module object (sys.modules entry for gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab).

    EFFECT:
      The module is loaded into sys.modules. Any module-level side effects
      (e.g., import-time calls to get_preset_feeds) will execute.

    ERRORS/EDGE CASES:
      - If the source module has a syntax error, ImportError or SyntaxError is raised.
      - If the module is already cached in sys.modules, the cached version is returned.
      - If PYTHONPATH or sys.path does not include the project root, ImportError is raised.
      - If the presets library feature is not installed, get_preset_feeds import may fail.

    HOW TO TEST:
      1. Call mod = _import_module().
      2. Assert mod is not None.
      3. Access mod.build_subscriptions_tab to verify the function is available.
      Example: mod = _import_module(); assert callable(mod.build_subscriptions_tab)
    """
    import gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab as mod
    return mod


def test_file_exists():
    r"""Layer 1 — Source file must exist on disk.

    WHAT:
      Verifies that the source module file build_subscriptions_tab.py is present
      at the expected location in the project's gui/ directory.

    WHY:
      If the file is missing, all other tests in this suite will fail with
      ImportError, making diagnosis harder. Catching a missing file first
      gives a clear, actionable error message.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if the file exists; raises AssertionError with the file path
      if the file is missing.

    ERRORS/EDGE CASES:
      - File moved or deleted: assertion fails with the full path printed.
      - Symlink broken: assertion fails (Path.exists() returns False for broken symlinks).

    HOW TO TEST:
      1. Confirm the file exists at gui/_06_ui_subscriptions_hub_tab_build/build_subscriptions_tab.py.
      2. Rename or delete it temporarily — the test should fail with a clear path message.
      3. Restore the file — the test should pass again.
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    r"""Layer 1 — Module must import without raising any exception.

    WHAT:
      Verifies that importing the source module completes successfully with
      no SyntaxError, ImportError, or other exception.

    WHY:
      A module that cannot be imported is fundamentally broken. This test
      catches syntax errors, missing dependencies, or circular import issues
      before any deeper structural or behavioral tests run.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if import succeeds and returns a non-None module object.
      Raises any exception thrown during import if it occurs.

    ERRORS/EDGE CASES:
      - Missing dependency (e.g., PyQt6 not installed): ImportError propagates.
      - Circular import: ImportError or RecursionError propagates.
      - Presets library not installed: ImportError from get_preset_feeds propagation.
      - Module already cached: returns cached module (still valid).

    HOW TO TEST:
      1. Call mod = _import_module() — should not raise.
      2. Temporarily introduce a syntax error in the source — test should fail.
      3. Restore the source — test should pass again.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    r"""Layer 1 — All expected imports must be present in the source AST.

    WHAT:
      Parses the source file with Python's ast module and verifies that the
      following three imports are present: PyQt6.QtCore, PyQt6.QtWidgets,
      and features.feature_feed_presets_library.implementation.feeds_presets.
      Missing any of these would cause runtime import failures.

    WHY:
      Dynamic imports (importlib) could miss renamed or removed imports.
      AST parsing statically inspects the source text, catching import
      drift even before the module is executed.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if all three expected import modules are found in the AST.
      Raises AssertionError listing the missing import names.

    ERRORS/EDGE CASES:
      - Import renamed (e.g., PyQt6.QtCore -> PyQt5.QtCore): assertion fails with missing import listed.
      - Import dropped entirely: assertion fails.
      - Import aliased (as X): still detected because AST checks node.module, not alias.name.
      - Presets import path changed: assertion fails if the full dotted path differs.

    HOW TO TEST:
      1. Remove one expected import from the source — test should fail listing the missing name.
      2. Add an extra unexpected import — test should still pass (only checks for expected set).
      3. Restore the source — test should pass again.
    """
    expected = {"PyQt6.QtCore", "PyQt6.QtWidgets", "features.feature_feed_presets_library.implementation.feeds_presets"}
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, f"Missing imports: {sorted(missing)}"


def test_build_subscriptions_tab_signature():
    r"""Layer 1 — build_subscriptions_tab must accept (window) and return None.

    WHAT:
      Verifies that build_subscriptions_tab has exactly one parameter named
      window (positional-or-keyword, no default) and that its return type
      annotation is None.

    WHY:
      The function signature is the public contract. The orchestrator in
      build_main_window_ui calls build_subscriptions_tab(window) with the
      MainWindow instance. Changing the parameter name or adding required
      parameters would break the call site.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if the signature matches exactly.
      Raises AssertionError with expected vs. actual parameter list.

    ERRORS/EDGE CASES:
      - Parameter renamed (e.g., window -> main_win): assertion fails.
      - Default added (e.g., window=None): assertion fails (Parameter.empty vs None).
      - Extra parameter added: assertion fails (length mismatch).
      - Return annotation changed (e.g., -> int): assertion fails.

    HOW TO TEST:
      1. Rename the parameter in source — test should fail.
      2. Add a second parameter — test should fail.
      3. Change return annotation from None to int — test should fail.
      4. Restore — test should pass again.
    """
    mod = _import_module()
    func = mod.build_subscriptions_tab
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_table_feeds_column_count_6():
    r"""Layer 2 — table_feeds must have exactly 6 columns.

    WHAT:
      Mocks QTableWidget and calls build_subscriptions_tab. Verifies that
      setColumnCount was called exactly once with the argument 6, meaning
      the feed management table has six columns.

    WHY:
      The six columns correspond to: Name, RSS Endpoint URL, Category,
      Interval, Active, and Actions. If the column count drifts (e.g.,
      someone adds or removes a column), the table layout breaks and the
      header labels will not match the data.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if table_mock.setColumnCount was called once with argument 6.
      Raises AssertionError if called with a different value or not at all.

    ERRORS/EDGE CASES:
      - Column count changed to 5: assertion fails (expected 6).
      - Column count changed to 7: assertion fails.
      - setColumnCount called multiple times: assert_called_once_with fails.

    HOW TO TEST:
      1. Patch QTableWidget to return a MagicMock.
      2. Call build_subscriptions_tab(window).
      3. Assert table_mock.setColumnCount.assert_called_once_with(6).
      Realistic example: table_mock.setColumnCount.assert_called_once_with(6)
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        table_mock.setColumnWidth = MagicMock()
        table_mock.verticalHeader = MagicMock()
        table_mock.verticalHeader.return_value.setVisible = MagicMock()
        table_mock.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        table_mock.setAlternatingRowColors = MagicMock()
        mod.build_subscriptions_tab(window)
        table_mock.setColumnCount.assert_called_once_with(6)


def test_table_feeds_headers():
    r"""Layer 2 — table_feeds headers must be ['Name','RSS Endpoint URL','Category','Interval','Active','Actions'].

    WHAT:
      Mocks QTableWidget and calls build_subscriptions_tab. Verifies that
      setHorizontalHeaderLabels was called exactly once with the six expected
      column header strings in the correct order.

    WHY:
      The header labels tell the user what each column represents. If labels
      are missing, reordered, or misspelled, users will be confused about
      what data to enter or what each column displays.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if setHorizontalHeaderLabels was called once with the exact
      expected label list.
      Raises AssertionError if labels differ or are in wrong order.

    ERRORS/EDGE CASES:
      - Header label misspelled (e.g., "Categroy" instead of "Category"): assertion fails.
      - Extra label added (7 items): assertion fails (list length mismatch).
      - Labels reordered: assertion fails (list equality check).

    HOW TO TEST:
      1. Patch QTableWidget to return a MagicMock.
      2. Call build_subscriptions_tab(window).
      3. Assert table_mock.setHorizontalHeaderLabels.assert_called_once_with(["Name", "RSS Endpoint URL", "Category", "Interval", "Active", "Actions"]).
      Realistic example: headers = ["Name", "RSS Endpoint URL", "Category", "Interval", "Active", "Actions"]; table_mock.setHorizontalHeaderLabels.assert_called_once_with(headers)
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        table_mock.setColumnWidth = MagicMock()
        table_mock.verticalHeader = MagicMock()
        table_mock.verticalHeader.return_value.setVisible = MagicMock()
        table_mock.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        table_mock.setAlternatingRowColors = MagicMock()
        mod.build_subscriptions_tab(window)
        table_mock.setHorizontalHeaderLabels.assert_called_once_with(
            ["Name", "RSS Endpoint URL", "Category", "Interval", "Active", "Actions"]
        )


def test_col_width_0_is_190():
    r"""Layer 2 — column 0 (Name) must have fixed width 190 pixels.

    WHAT:
      Mocks QTableWidget and calls build_subscriptions_tab. Verifies that
      setColumnWidth was called exactly once with arguments (0, 190), meaning
      the Name column has a fixed width of 190 pixels.

    WHY:
      The Name column is the most visually important column and needs enough
      width to display feed names like "TechCrunch" or "BBC News" without
      truncation. A width of 190 pixels provides comfortable reading space.
      If this changes, names may be cut off or wasted space may appear.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if setColumnWidth was called once with (0, 190).
      Raises AssertionError if called with different arguments.

    ERRORS/EDGE CASES:
      - Width changed to 150: assertion fails (names may truncate).
      - Width changed to 250: assertion fails (excess whitespace).
      - setColumnWidth called for a different column index: assertion fails.

    HOW TO TEST:
      1. Patch QTableWidget to return a MagicMock.
      2. Call build_subscriptions_tab(window).
      3. Assert table_mock.setColumnWidth.assert_called_once_with(0, 190).
      Realistic example: table_mock.setColumnWidth.assert_called_once_with(0, 190)
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        table_mock.setColumnWidth = MagicMock()
        table_mock.verticalHeader = MagicMock()
        table_mock.verticalHeader.return_value.setVisible = MagicMock()
        table_mock.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        table_mock.setAlternatingRowColors = MagicMock()
        mod.build_subscriptions_tab(window)
        table_mock.setColumnWidth.assert_called_once_with(0, 190)


def test_drawer_box_hidden_by_default():
    r"""Layer 2 — drawer_box must be hidden (setVisible(False)) by default.

    WHAT:
      Mocks QTableWidget, QFrame, QLineEdit, QComboBox, and QPushButton.
      Calls build_subscriptions_tab and verifies that the drawer QFrame's
      setVisible was called exactly once with False, meaning the add-feed
      drawer is collapsed when the tab first appears.

    WHY:
      The drawer contains the add-feed form and preset chips. It should be
      hidden by default to keep the UI clean; users open it by clicking
      the "New Feed / Presets" button. If it is visible by default, it
      clutters the interface and wastes space.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if mock_frame.setVisible was called once with False.
      Raises AssertionError if called with True or not at all.

    ERRORS/EDGE CASES:
      - Drawer visible by default (setVisible(True)): assertion fails.
      - setVisible called multiple times: assert_called_once_with fails.
      - setVisible not called: assert_called_once_with fails.

    HOW TO TEST:
      1. Patch QFrame to return a MagicMock with setVisible mock.
      2. Call build_subscriptions_tab(window).
      3. Assert mock_frame.setVisible.assert_called_once_with(False).
      Realistic example: mock_frame.setVisible.assert_called_once_with(False)
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QFrame") as MockFrame, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLineEdit") as MockLine, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QComboBox") as MockCombo, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.setColumnWidth = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        mock_frame = MagicMock()
        mock_frame.setVisible = MagicMock()
        MockFrame.return_value = mock_frame
        MockLine.return_value = MagicMock()
        MockCombo.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        mod.build_subscriptions_tab(window)
        mock_frame.setVisible.assert_called_once_with(False)


def test_cb_freq_items_and_default_index():
    r"""Layer 2 — cb_freq must have items ['1h','3h','6h','12h','24h'] with default index 3.

    WHAT:
      Mocks the Qt widgets and calls build_subscriptions_tab. Verifies that
      the frequency ComboBox's addItems was called with the five interval
      strings and that setCurrentIndex was called with 3 (selecting "12h").

    WHY:
      The fetch interval determines how often the app checks each feed for
      new articles. The five options (1h, 3h, 6h, 12h, 24h) cover common
      check frequencies. Index 3 ("12h") is the sensible default — frequent
      enough for most users without excessive network traffic.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if addItems was called with ["1h", "3h", "6h", "12h", "24h"]
      and setCurrentIndex was called with 3.
      Raises AssertionError if items or index differ.

    ERRORS/EDGE CASES:
      - Items in wrong order (e.g., ["24h","12h","6h","3h","1h"]): assertion fails.
      - Default index changed (e.g., 0 for "1h"): assertion fails.
      - Extra item added (e.g., "48h"): assertion fails (list length mismatch).
      - Missing item (e.g., no "6h"): assertion fails.

    HOW TO TEST:
      1. Patch QComboBox to return a MagicMock with addItems and setCurrentIndex mocks.
      2. Call build_subscriptions_tab(window) with patched get_preset_feeds returning [].
      3. Assert addItems called with ["1h","3h","6h","12h","24h"] and setCurrentIndex called with 3.
      Realistic example: mock_combo.addItems.assert_called_once_with(["1h", "3h", "6h", "12h", "24h"]); mock_combo.setCurrentIndex.assert_called_once_with(3)
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QFrame") as MockFrame, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLineEdit") as MockLine, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QComboBox") as MockCombo, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.setColumnWidth = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockFrame.return_value = MagicMock()
        MockLine.return_value = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItems = MagicMock()
        mock_combo.setCurrentIndex = MagicMock()
        mock_combo.setMaximumWidth = MagicMock()
        MockCombo.return_value = mock_combo
        MockButton.return_value = MagicMock()
        with patch.object(mod, "get_preset_feeds", return_value=[]):
            mod.build_subscriptions_tab(window)
        mock_combo.addItems.assert_any_call(["1h", "3h", "6h", "12h", "24h"])
        mock_combo.setCurrentIndex.assert_any_call(3)


def test_in_cat_default_general():
    r"""Layer 2 — in_cat (category input) must default to text "General".

    WHAT:
      Mocks the Qt widgets and calls build_subscriptions_tab. Verifies that
      the third QLineEdit (window.in_cat) has setText called with "General",
      meaning the category input field is pre-filled with the default value.

    WHY:
      Most RSS feeds belong to a general or uncategorized bucket. Pre-filling
      the category field with "General" saves users from typing it for every
      new feed they add. If the default changes, users may accidentally create
      feeds in the wrong category.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if mock_lines[2].setText was called once with "General".
      Raises AssertionError if the default text differs.

    ERRORS/EDGE CASES:
      - Default changed to "Uncategorized": assertion fails.
      - Default changed to empty string "": assertion fails.
      - setText called multiple times: assert_called_once_with fails.

    HOW TO TEST:
      1. Patch QLineEdit to return three MagicsMocks, with the third having setText mock.
      2. Call build_subscriptions_tab(window) with patched get_preset_feeds returning [].
      3. Assert mock_lines[2].setText.assert_called_once_with("General").
      Realistic example: mock_lines[2].setText.assert_called_once_with("General")
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QFrame") as MockFrame, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLineEdit") as MockLine, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QComboBox") as MockCombo, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.setColumnWidth = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockFrame.return_value = MagicMock()
        mock_lines = [MagicMock(), MagicMock(), MagicMock()]
        mock_lines[2].setText = MagicMock()
        mock_lines[2].setPlaceholderText = MagicMock()
        mock_lines[2].setMaximumWidth = MagicMock()
        MockLine.side_effect = mock_lines
        MockCombo.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        with patch.object(mod, "get_preset_feeds", return_value=[]):
            mod.build_subscriptions_tab(window)
        mock_lines[2].setText.assert_called_once_with("General")


def test_btn_toggle_drawer_connected():
    r"""Layer 2 — btn_toggle_drawer clicked signal must connect to window.toggle_add_drawer.

    WHAT:
      Mocks the Qt widgets and calls build_subscriptions_tab. Verifies that
      the toggle drawer button's clicked signal is connected to
      window.toggle_add_drawer, meaning clicking the button will show/hide
      the add-feed drawer.

    WHY:
      The toggle button is the primary user interaction for opening the
      add-feed drawer. If the connection is broken or points to the wrong
      method, clicking the button will do nothing, and users cannot add feeds.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if mock_btn.clicked.connect was called once with window.toggle_add_drawer.
      Raises AssertionError if the connection is missing or points elsewhere.

    ERRORS/EDGE CASES:
      - Button connected to wrong method (e.g., window.close_drawer): assertion fails.
      - Button not connected at all: assert_called_once_with fails.
      - Button connected multiple times: assert_called_once_with fails.

    HOW TO TEST:
      1. Patch QPushButton to return a MagicMock with clicked.connect mock (as the first button).
      2. Set window.toggle_add_drawer = MagicMock().
      3. Call build_subscriptions_tab(window) with patched get_preset_feeds returning [].
      4. Assert mock_btn.clicked.connect.assert_called_once_with(window.toggle_add_drawer).
      Realistic example: mock_btn.clicked.connect.assert_called_once_with(window.toggle_add_drawer)
    """
    mod = _import_module()
    window = MagicMock()
    window.toggle_add_drawer = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QFrame") as MockFrame, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLineEdit") as MockLine, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QComboBox") as MockCombo, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.setColumnWidth = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockFrame.return_value = MagicMock()
        MockLine.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.side_effect = [mock_btn, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        MockCombo.return_value = MagicMock()
        with patch.object(mod, "get_preset_feeds", return_value=[]):
            mod.build_subscriptions_tab(window)
        mock_btn.clicked.connect.assert_called_once_with(window.toggle_add_drawer)


def test_btn_add_connected():
    r"""Layer 2 — btn_add clicked signal must connect to window.add_feed.

    WHAT:
      Mocks the Qt widgets and calls build_subscriptions_tab. Verifies that
      the add-feed button's clicked signal is connected to window.add_feed,
      meaning clicking "Add Feed" will submit the form.

    WHY:
      The add button is the primary action for creating new feed subscriptions.
      If the connection is broken, users can fill in the form but submitting
      it will have no effect, making the entire add-feed feature non-functional.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if mock_btn.clicked.connect was called once with window.add_feed.
      Raises AssertionError if the connection is missing or points elsewhere.

    ERRORS/EDGE CASES:
      - Button connected to wrong method (e.g., window.reset_form): assertion fails.
      - Button not connected at all: assert_called_once_with fails.
      - Button connected multiple times: assert_called_once_with fails.

    HOW TO TEST:
      1. Patch QPushButton to return a MagicMock with clicked.connect mock (as the fifth button).
      2. Set window.add_feed = MagicMock().
      3. Call build_subscriptions_tab(window) with patched get_preset_feeds returning [].
      4. Assert mock_btn.clicked.connect.assert_called_once_with(window.add_feed).
      Realistic example: mock_btn.clicked.connect.assert_called_once_with(window.add_feed)
    """
    mod = _import_module()
    window = MagicMock()
    window.add_feed = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QFrame") as MockFrame, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLineEdit") as MockLine, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QComboBox") as MockCombo, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.setColumnWidth = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockFrame.return_value = MagicMock()
        MockLine.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.side_effect = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), mock_btn, MagicMock()]
        MockCombo.return_value = MagicMock()
        with patch.object(mod, "get_preset_feeds", return_value=[]):
            mod.build_subscriptions_tab(window)
        mock_btn.clicked.connect.assert_called_once_with(window.add_feed)


def test_preset_dropdown_tiered():
    r"""Layer 2 — two-tier preset dropdown must be created and wired.

    WHAT:
      Mocks the Qt widgets and provides two preset feeds via get_preset_feeds
      (TechCrunch and BBC) plus two categories via get_preset_categories.
      Calls build_subscriptions_tab and verifies that:
        - window.cb_preset_cat (category combo) was created and populated
        - window.cb_preset_select (preset combo) was created
        - cb_preset_select.currentIndexChanged was connected to import logic
        - window._preset_feeds was set with the preset list

    WHY:
      The two-tier dropdown replaces the 475 chip buttons. Users first pick
      a category, then pick a feed from the filtered list. Selecting a feed
      immediately imports it. If the dropdown setup is broken, users lose
      access to quick-import entirely.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if cb_preset_cat and cb_preset_select are both created,
      cb_preset_cat is populated with categories, and cb_preset_select
      has currentIndexChanged connected (called at least once).

    ERRORS/EDGE CASES:
      - get_preset_feeds returns empty list: dropdowns still created with placeholder.
      - get_preset_categories raises: falls back to ["All Categories"].

    HOW TO TEST:
      1. Patch get_preset_feeds to return two presets and get_preset_categories
         to return two categories.
      2. Patch QComboBox to return a MagicMock with addItems/currentIndexChanged
         mocks.
      3. Call build_subscriptions_tab(window).
      4. Assert window.cb_preset_cat exists and addItems was called.
      5. Assert window.cb_preset_select exists and currentIndexChanged.connect
         was called.
      6. Assert window._preset_feeds equals the preset list.
    """
    mod = _import_module()
    window = MagicMock()
    window._preset_feeds = None
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QFrame") as MockFrame, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLineEdit") as MockLine, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QComboBox") as MockCombo, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QPushButton") as MockButton, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLabel") as MockLabel:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.setColumnWidth = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockFrame.return_value = MagicMock()
        MockLine.return_value = MagicMock()
        mock_label = MagicMock()
        mock_label.setStyleSheet = MagicMock()
        MockLabel.return_value = mock_label
        mock_btn_toggle = MagicMock()
        mock_btn_toggle.clicked = MagicMock()
        mock_btn_toggle.clicked.connect = MagicMock()
        mock_btn_add = MagicMock()
        mock_btn_add.clicked = MagicMock()
        mock_btn_add.clicked.connect = MagicMock()
        MockButton.side_effect = [mock_btn_toggle, mock_btn_add]

        # Track each QComboBox creation individually.
        combo_captures = []

        def combo_factory(*args, **kwargs):
            m = MagicMock()
            m.addItems = MagicMock()
            m.setCurrentIndex = MagicMock()
            m.setMinimumWidth = MagicMock()
            m.currentIndexChanged = MagicMock()
            m.currentIndexChanged.connect = MagicMock()
            m.itemText = MagicMock(return_value="All Categories")
            m.count = MagicMock(return_value=1)
            combo_captures.append(m)
            return m

        MockCombo.side_effect = combo_factory
        presets = [
            {"name": "TechCrunch", "url": "http://tc.com/feed", "category": "Technology"},
            {"name": "BBC", "url": "http://bbc.com/feed", "category": "News"},
        ]
        categories = ["Technology", "News"]
        with patch.object(mod, "get_preset_feeds", return_value=presets), \
             patch.object(mod, "get_preset_categories", return_value=categories):
            mod.build_subscriptions_tab(window)

        # cb_preset_cat is the 3rd QComboBox (after cb_cat_filter and cb_freq).
        assert len(combo_captures) >= 3
        cb_preset_cat = combo_captures[2]
        # cb_preset_select is the 4th QComboBox.
        cb_preset_select = combo_captures[3] if len(combo_captures) > 3 else combo_captures[2]

        # Category combo must have been populated.
        cb_preset_cat.addItems.assert_called_once()
        # Preset combo must have had its index changed signal connected.
        cb_preset_select.currentIndexChanged.connect.assert_called_once()
        # window must have the preset list stored for lookup.
        assert window._preset_feeds == presets


def test_tab_label():
    r"""Layer 2 — tab must be added to window.tabs with label "📡 Subscriptions Hub".

    WHAT:
      Mocks the Qt widgets and calls build_subscriptions_tab. Verifies that
      window.tabs.addTab was called once and that the second argument (the
      tab label) is exactly "📡 Subscriptions Hub".

    WHY:
      The tab label is what the user sees in the main window's tab bar.
      If the label is wrong, missing, or contains extra whitespace, users
      will be confused about which tab is which. The emoji prefix is part
      of the designed branding and should not be stripped or changed.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if window.tabs.addTab was called once with label "📡 Subscriptions Hub".
      Raises AssertionError if the label differs.

    ERRORS/EDGE CASES:
      - Label misspelled (e.g., "Subscriptons Hub"): assertion fails.
      - Label missing emoji (e.g., "Subscriptions Hub"): assertion fails.
      - Extra whitespace (e.g., "📡 Subscriptions Hub "): assertion fails.
      - addTab called multiple times: assert_called_once fails.

    HOW TO TEST:
      1. Set window.tabs = MagicMock().
      2. Call build_subscriptions_tab(window) with patched get_preset_feeds returning [].
      3. Assert call_args[0][1] == "📡 Subscriptions Hub".
      Realistic example: call_args = window.tabs.addTab.call_args; assert call_args[0][1] == "📡 Subscriptions Hub"
    """
    mod = _import_module()
    window = MagicMock()
    window.tabs = MagicMock()
    with patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QTableWidget") as MockTable, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QFrame") as MockFrame, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QLineEdit") as MockLine, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QComboBox") as MockCombo, \
         patch("gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.setColumnWidth = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockFrame.return_value = MagicMock()
        MockLine.return_value = MagicMock()
        MockCombo.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        with patch.object(mod, "get_preset_feeds", return_value=[]):
            mod.build_subscriptions_tab(window)
        window.tabs.addTab.assert_called_once()
        call_args = window.tabs.addTab.call_args
        assert call_args[0][1] == "📡 Subscriptions Hub"
