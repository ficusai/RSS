"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_05_ui_articles_explorer_tab_build/build_articles_tab.py
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
    return Path(__file__).resolve().parents[3] / "gui" / "_05_ui_articles_explorer_tab_build" / "build_articles_tab.py"


def _import_module():
    import gui._05_ui_articles_explorer_tab_build.build_articles_tab as mod
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
    expected = {"PyQt6.QtCore", "PyQt6.QtGui", "PyQt6.QtWidgets"}
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


def test_build_articles_tab_signature():
    """Layer 1 — build_articles_tab(window) -> None."""
    mod = _import_module()
    func = mod.build_articles_tab
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_table_column_count_4():
    """Layer 2 — table_articles columnCount 4."""
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    window.table_articles = table_mock
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        table_mock.verticalHeader = MagicMock()
        table_mock.verticalHeader.return_value.setVisible = MagicMock()
        table_mock.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        table_mock.setAlternatingRowColors = MagicMock()
        table_mock.setSelectionBehavior = MagicMock()
        table_mock.itemSelectionChanged = MagicMock()
        table_mock.itemSelectionChanged.connect = MagicMock()
        mod.build_articles_tab(window)
        table_mock.setColumnCount.assert_called_once_with(4)


def test_table_headers_exact():
    """Layer 2 — headers ['Article Title','Source Feed','Category','Date']."""
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        table_mock.verticalHeader = MagicMock()
        table_mock.verticalHeader.return_value.setVisible = MagicMock()
        table_mock.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        table_mock.setAlternatingRowColors = MagicMock()
        table_mock.setSelectionBehavior = MagicMock()
        table_mock.itemSelectionChanged = MagicMock()
        table_mock.itemSelectionChanged.connect = MagicMock()
        mod.build_articles_tab(window)
        table_mock.setHorizontalHeaderLabels.assert_called_once_with(
            ["Article Title", "Source Feed", "Category", "Date"]
        )


def test_alternating_rows_hidden_vertical_header_row_height():
    """Layer 2 — alternating rows, row height 50, hidden vertical header."""
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        vh_mock = MagicMock()
        table_mock.verticalHeader.return_value = vh_mock
        table_mock.setAlternatingRowColors = MagicMock()
        table_mock.setSelectionBehavior = MagicMock()
        table_mock.itemSelectionChanged = MagicMock()
        table_mock.itemSelectionChanged.connect = MagicMock()
        mod.build_articles_tab(window)
        vh_mock.setVisible.assert_called_once_with(False)
        vh_mock.setDefaultSectionSize.assert_called_once_with(50)
        table_mock.setAlternatingRowColors.assert_called_once_with(True)


def test_input_search_placeholder():
    """Layer 2 — input_search placeholder text exact."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QLineEdit") as MockLine:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_line = MagicMock()
        mock_line.setPlaceholderText = MagicMock()
        mock_line.textChanged = MagicMock()
        mock_line.textChanged.connect = MagicMock()
        MockLine.return_value = mock_line
        mod.build_articles_tab(window)
        mock_line.setPlaceholderText.assert_called_once_with(
            "🔍 Search by title, text body, author, or feed name..."
        )


def test_combo_cat_first_item_all_categories():
    """Layer 2 — combo_cat first item 'All Categories'."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        mod.build_articles_tab(window)
        mock_combo.addItem.assert_called_once_with("All Categories")


def test_btn_refresh_view_connected():
    """Layer 2 — btn_refresh_view connected to window.refresh."""
    mod = _import_module()
    window = MagicMock()
    window.refresh = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        mod.build_articles_tab(window)
        mock_btn.clicked.connect.assert_called_once_with(window.refresh)


def test_btn_copy_link_and_open_disabled_initially():
    """Layer 2 — btn_copy_link and btn_open disabled initially."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        side_effects = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        MockButton.side_effect = side_effects
        mod.build_articles_tab(window)
        # btn_copy_link is index 2, btn_open is index 3
        side_effects[2].setEnabled.assert_called_once_with(False)
        side_effects[3].setEnabled.assert_called_once_with(False)


def test_btn_open_object_name_primary_blue():
    """Layer 2 — btn_open objectName 'primary_blue'."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        side_effects = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        MockButton.side_effect = side_effects
        mod.build_articles_tab(window)
        side_effects[3].setObjectName.assert_called_once_with("primary_blue")


def test_reader_widgets_present():
    """Layer 2 — Reader widgets present (lbl_reader_title, lbl_reader_meta, txt_reader)."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QLabel") as MockLabel, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTextEdit") as MockText:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        MockLabel.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_articles_tab(window)


def test_tab_label_and_added_to_tabs():
    """Layer 2 — Tab label '📰 Articles Explorer', added to window.tabs."""
    mod = _import_module()
    window = MagicMock()
    window.tabs = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTextEdit") as MockText, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QLabel") as MockLabel, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        MockLabel.return_value = MagicMock()
        MockText.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        mod.build_articles_tab(window)
        window.tabs.addTab.assert_called_once()
        call_args = window.tabs.addTab.call_args
        assert call_args[0][1] == "📰 Articles Explorer"
