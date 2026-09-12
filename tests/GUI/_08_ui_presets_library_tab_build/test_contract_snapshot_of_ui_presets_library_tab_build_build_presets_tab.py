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
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_08_ui_presets_library_tab_build" / "build_presets_tab.py"


def _import_module():
    import gui._08_ui_presets_library_tab_build.build_presets_tab as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence."""
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health."""
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports."""
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
    """Layer 1 — build_presets_tab(window) -> None."""
    mod = _import_module()
    func = mod.build_presets_tab
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_table_presets_columns_5():
    """Layer 2 — table_presets columns + headers exact (5 columns)."""
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
    """Layer 2 — table_presets headers exact."""
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
    """Layer 2 — preset_combo_cat created."""
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
    """Layer 2 — 'Add All Presets' button connected to window.add_all_presets."""
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
    """Layer 2 — load_preset_categories called at end."""
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
    """Layer 2 — Tab label '📚 Feed Presets Library'."""
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
