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
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_06_ui_subscriptions_hub_tab_build" / "build_subscriptions_tab.py"


def _import_module():
    import gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab as mod
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
    """Layer 1 — build_subscriptions_tab(window) -> None."""
    mod = _import_module()
    func = mod.build_subscriptions_tab
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_table_feeds_column_count_6():
    """Layer 2 — table_feeds columnCount 6."""
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
    """Layer 2 — headers ['Name','RSS Endpoint URL','Category','Interval','Active','Actions']."""
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
    """Layer 2 — column 0 width == 190."""
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
    """Layer 2 — drawer_box hidden by default."""
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
    """Layer 2 — cb_freq items ['1h','3h','6h','12h','24h'] default index 3."""
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
        mock_combo.addItems.assert_called_once_with(["1h", "3h", "6h", "12h", "24h"])
        mock_combo.setCurrentIndex.assert_called_once_with(3)


def test_in_cat_default_general():
    """Layer 2 — in_cat default 'General'."""
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
    """Layer 2 — btn_toggle_drawer connected to window.toggle_add_drawer."""
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
    """Layer 2 — btn_add connected to window.add_feed."""
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


def test_preset_chips_created():
    """Layer 2 — Preset chips created for get_preset_feeds() items."""
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
        MockCombo.return_value = MagicMock()
        mock_chip = MagicMock()
        mock_chip.setObjectName = MagicMock()
        mock_chip.setToolTip = MagicMock()
        mock_chip.clicked = MagicMock()
        mock_chip.clicked.connect = MagicMock()
        MockButton.return_value = mock_chip
        presets = [
            {"name": "TechCrunch", "url": "http://tc.com/feed", "category": "Technology"},
            {"name": "BBC", "url": "http://bbc.com/feed", "category": "News"},
        ]
        with patch.object(mod, "get_preset_feeds", return_value=presets):
            mod.build_subscriptions_tab(window)
        assert mock_chip.clicked.connect.call_count == 2


def test_tab_label():
    """Layer 2 — Tab label '📡 Subscriptions Hub'."""
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
