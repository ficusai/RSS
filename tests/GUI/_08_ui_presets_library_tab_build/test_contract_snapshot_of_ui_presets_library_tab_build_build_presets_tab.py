"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_08_ui_presets_library_tab_build/build_presets_tab.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.
"""
# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# This test file verifies the contract of gui._08_ui_presets_library_tab_build
# build_presets_tab. It checks that the source module file exists, imports
# correctly, has the expected AST-import set (PyQt6.QtWidgets plus the two
# imported helper functions), that build_presets_tab has the correct signature,
# and that calling it with a MagicMock window produces the expected Qt widget
# hierarchy: a QTableWidget with 5 columns and exact headers, a QComboBox
# category dropdown, a QPushButton for 'Add All Presets', and the correct tab
# label "📚 Feed Presets Library". It also verifies that
# load_preset_categories and refresh_presets_table are called at the end.
# ==============================================================================
# ==============================================================================
# LAYER BREAKDOWN
#   Layer 1 — Module-level contract checks:
#     * test_file_exists: source .py file is present on disk.
#     * test_import_health: the module can be imported without error.
#     * test_ast_imports: the expected imports present via AST.
#     * test_build_presets_tab_signature: func(window) -> None signature.
#   Layer 2 — Behavioural contract checks (mocked Qt):
#     * test_table_presets_columns_5: table_presets columnCount == 5.
#     * test_table_presets_headers: table_presets headers exact match.
#     * test_preset_combo_cat_created: preset_combo_cat QComboBox created with minimum width.
#     * test_add_all_presets_button_connected: btn_add_all_presets.clicked.connect(window.add_all_presets).
#     * test_load_preset_categories_wired: load_preset_categories and refresh_presets_table called at end.
#     * test_tab_label: tab label is "📚 Feed Presets Library".
# ==============================================================================
# ==============================================================================
# LAYER WHAT EACH TEST CHECKS
#   Layer 1 tests verify the module's structural contract (file presence, import
#   health, static import set, function signature).
#   Layer 2 tests verify the runtime widget-creation contract by mocking Qt
#   classes and asserting on constructor calls, attribute assignments, signal
#   connections, table column/header values, and helper-function call ordering.
# ==============================================================================
# OVERVIEW OF IMPORTS
# import ast: abstract syntax tree parser; used to verify source-module imports statically.
# import inspect: runtime introspection; used to inspect function signatures.
# import sys: Python runtime; used to prepend the repo root to sys.path.
# import Path from pathlib: filesystem path builder; used to resolve the source-module file path.
# import MagicMock, patch from unittest.mock: test doubles; used to replace Qt widgets and module functions during Layer 2 tests.
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    r"""Return the absolute Path to the source module under test.

    WHAT: Builds the filesystem path to the source .py file.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: A pathlib.Path pointing to gui/_08_ui_presets_library_tab_build/build_presets_tab.py.
    EFFECT: None (pure function).
    ERRORS/EDGE CASES: Should never fail; returns a Path even if the file does not exist.
    EDGE CASES: None.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_08_ui_presets_library_tab_build" / "build_presets_tab.py"


def _import_module():
    r"""Import and return the source module under test.

    WHAT: Dynamically imports the GUI source module so tests can inspect it.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: The imported module object.
    EFFECT: Side-effect of importing the module (may run module-level code).
    ERRORS/EDGE CASES: ImportError if the module is missing or has a syntax error.
    EDGE CASES: The sys.path insertion above ensures the repo root is on the path.
    """
    import gui._08_ui_presets_library_tab_build.build_presets_tab as mod
    return mod


def test_file_exists():
    r"""Layer 1 — file existence.

    WHAT: Verifies the source module file exists on disk.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if the source file is missing.
    ERRORS/EDGE CASES: FileNotFoundError if the path resolves incorrectly.
    EDGE CASES: None.
    HOW TO TEST: Call _module_path() and check .exists().
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    r"""Layer 1 — import health.

    WHAT: Verifies the source module can be imported without raising.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: The imported module object.
    EFFECT: Module-level code executes (side-effect).
    ERRORS/EDGE CASES: ImportError or ModuleNotFoundError on bad module.
    EDGE CASES: None.
    HOW TO TEST: Call _import_module() and assert result is not None.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    r"""Layer 1 — AST-verified imports.

    WHAT: Verifies the expected PyQt6.QtWidgets and two gui submodule imports are
          present in the source AST.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if any expected import is missing.
    ERRORS/EDGE CASES: SyntaxError if source file has invalid Python.
    EDGE CASES: None.
    HOW TO TEST: Parse the source AST and walk for Import/ImportFrom nodes.
    """
    expected = {
        "PyQt6.QtWidgets",
        "gui._30_preset_categories_load_dropdown.load_preset_categories",
        "gui._31_presets_table_refresh_view.refresh_presets_table",
    }
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


def test_build_presets_tab_signature():
    r"""Layer 1 — build_presets_tab(window) -> None.

    WHAT: Verifies the exact function signature of build_presets_tab.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if signature differs.
    ERRORS/EDGE CASES: AttributeError if the function does not exist on the module.
    EDGE CASES: None.
    HOW TO TEST: Use inspect.signature and compare parameters + return annotation.
    """
    mod = _import_module()
    func = mod.build_presets_tab
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_table_presets_columns_5():
    r"""Layer 2 — table_presets columns + headers exact (5 columns).

    WHAT: Verifies that build_presets_tab creates a QTableWidget with exactly
          5 columns (columnCount == 5).
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if columnCount was not called with 5.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QTableWidget; call build_presets_tab; assert
                 columnCount.assert_called_once_with(5).
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QTableWidget") as MockTable:
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
        table_mock.setSelectionBehavior = MagicMock()
        mod.build_presets_tab(window)
        table_mock.setColumnCount.assert_called_once_with(5)


def test_table_presets_headers():
    r"""Layer 2 — table_presets headers exact.

    WHAT: Verifies that build_presets_tab sets the QTableWidget horizontal header
          labels to exactly ['Name', 'RSS Endpoint URL', 'Category', 'Status', 'Actions'].
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if headers do not match exactly.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QTableWidget; call build_presets_tab; assert
                 setHorizontalHeaderLabels was called once with the exact list.
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QTableWidget") as MockTable:
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
        table_mock.setSelectionBehavior = MagicMock()
        mod.build_presets_tab(window)
        table_mock.setHorizontalHeaderLabels.assert_called_once_with(
            ["Name", "RSS Endpoint URL", "Category", "Status", "Actions"]
        )


def test_preset_combo_cat_created():
    r"""Layer 2 — preset_combo_cat created.

    WHAT: Verifies that build_presets_tab creates a QComboBox for category
          selection (window.preset_combo_cat) and calls setMinimumWidth on it.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if setMinimumWidth was not called.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QComboBox; call build_presets_tab; assert
                 setMinimumWidth was called once.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QTableWidget") as MockTable, \
         patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QComboBox") as MockCombo:
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
        MockTable.return_value.setSelectionBehavior = MagicMock()
        mock_combo = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        mod.build_presets_tab(window)
        mock_combo.setMinimumWidth.assert_called_once()


def test_add_all_presets_button_connected():
    r"""Layer 2 — 'Add All Presets' button connected to window.add_all_presets.

    WHAT: Verifies that build_presets_tab creates a 'Add All Presets' QPushButton
          (with objectName 'accent') and connects its clicked signal to
          window.add_all_presets.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if clicked.connect was not called with window.add_all_presets.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QPushButton; provide a mock clicked.connect; call the
                 function; assert clicked.connect was called once with
                 window.add_all_presets.
    """
    mod = _import_module()
    window = MagicMock()
    window.add_all_presets = MagicMock()
    with patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QTableWidget") as MockTable, \
         patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QComboBox") as MockCombo, \
         patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QPushButton") as MockButton:
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
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockCombo.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.setObjectName = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        mod.build_presets_tab(window)
        mock_btn.clicked.connect.assert_called_once_with(window.add_all_presets)


def test_load_preset_categories_wired():
    r"""Layer 2 — load_preset_categories called at end.

    WHAT: Verifies that build_presets_tab calls load_preset_categories(window)
          and refresh_presets_table(window) after creating the widget hierarchy.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if either helper is not called exactly once with window.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch both helper functions; call build_presets_tab; assert
                 mock_load.assert_called_once_with(window) and
                 mock_refresh.assert_called_once_with(window).
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QTableWidget") as MockTable, \
         patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QComboBox") as MockCombo, \
         patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QPushButton") as MockButton, \
         patch.object(mod, "load_preset_categories") as mock_load, \
         patch.object(mod, "refresh_presets_table") as mock_refresh:
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
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockCombo.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        mod.build_presets_tab(window)
        mock_load.assert_called_once_with(window)
        mock_refresh.assert_called_once_with(window)


def test_tab_label():
    r"""Layer 2 — Tab label '📚 Feed Presets Library'.

    WHAT: Verifies that build_presets_tab registers itself with the exact label
          '📚 Feed Presets Library'.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if the tab label string does not match exactly.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QTableWidget/QComboBox/QPushButton; provide window.tabs
                 as MagicMock; call build_presets_tab; assert
                 window.tabs.addTab was called once with the correct label.
    """
    mod = _import_module()
    window = MagicMock()
    window.tabs = MagicMock()
    with patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QTableWidget") as MockTable, \
         patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QComboBox") as MockCombo, \
         patch("gui._08_ui_presets_library_tab_build.build_presets_tab.QPushButton") as MockButton, \
         patch.object(mod, "load_preset_categories"), \
         patch.object(mod, "refresh_presets_table"):
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
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockCombo.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        mod.build_presets_tab(window)
        window.tabs.addTab.assert_called_once()
        call_args = window.tabs.addTab.call_args
        assert call_args[0][1] == "📚 Feed Presets Library"
