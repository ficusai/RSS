"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_03_ui_assembly_orchestrator/build_main_window_ui.py
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
# PyQt6.QtWidgets.QApplication: Required before any Qt widget construction.
from PyQt6.QtWidgets import QApplication
QApplication.instance() or QApplication([])

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_03_ui_assembly_orchestrator" / "build_main_window_ui.py"


def _import_module():
    import gui._03_ui_assembly_orchestrator.build_main_window_ui as mod
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
        "PyQt6.QtCore",
        "PyQt6.QtWidgets",
        "gui._04_ui_header_bar_top_section_build.build_header_bar",
        "gui._05_ui_articles_explorer_tab_build.build_articles_tab",
        "gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab",
        "gui._07_ui_operations_system_tab_build.build_operations_tab",
        "gui._08_ui_presets_library_tab_build.build_presets_tab",
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


def test_build_main_window_ui_signature():
    """Layer 1 — build_main_window_ui(window) -> None."""
    mod = _import_module()
    func = mod.build_main_window_ui
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_build_calls_sub_builders():
    """Layer 2 — Calls build_header_bar, build_articles_tab, etc. once each."""
    mod = _import_module()
    window = MagicMock()
    with patch.object(mod, "QWidget") as MockW, \
         patch.object(mod, "QVBoxLayout") as MockL, \
         patch.object(mod, "build_header_bar") as mock_hdr, \
         patch.object(mod, "build_articles_tab") as mock_art, \
         patch.object(mod, "build_subscriptions_tab") as mock_sub, \
         patch.object(mod, "build_operations_tab") as mock_ops, \
         patch.object(mod, "build_presets_tab") as mock_pre:
        MockW.return_value = MagicMock()
        mock_layout = MagicMock()
        mock_layout.setSpacing = MagicMock()
        mock_layout.setContentsMargins = MagicMock()
        mock_layout.addWidget = MagicMock()
        MockL.return_value = mock_layout
        mod.build_main_window_ui(window)
        mock_hdr.assert_called_once_with(window)
        mock_art.assert_called_once_with(window)
        mock_sub.assert_called_once_with(window)
        mock_ops.assert_called_once_with(window)
        mock_pre.assert_called_once_with(window)


def test_creates_progress_bar():
    """Layer 2 — Creates progress bar."""
    mod = _import_module()
    window = MagicMock()
    with patch.object(mod, "QWidget") as MockW, \
         patch.object(mod, "QVBoxLayout") as MockL, \
         patch("gui._03_ui_assembly_orchestrator.build_main_window_ui.QProgressBar") as MockProgress:
        mock_central = MagicMock()
        MockW.return_value = mock_central
        mock_layout = MagicMock()
        mock_layout.setSpacing = MagicMock()
        mock_layout.setContentsMargins = MagicMock()
        mock_layout.addWidget = MagicMock()
        MockL.return_value = mock_layout
        mock_bar = MagicMock()
        mock_bar.setTextVisible = MagicMock()
        mock_bar.setVisible = MagicMock()
        MockProgress.return_value = mock_bar
        mod.build_main_window_ui(window)
        window.setCentralWidget.assert_called_once()
        mock_bar.setTextVisible.assert_called_once_with(False)
        mock_bar.setVisible.assert_called_once_with(False)


def test_creates_tabs_widget():
    """Layer 2 — Creates tabs QTabWidget."""
    mod = _import_module()
    window = MagicMock()
    with patch.object(mod, "QWidget") as MockW, \
         patch.object(mod, "QVBoxLayout") as MockL, \
         patch("gui._03_ui_assembly_orchestrator.build_main_window_ui.QTabWidget") as MockTabs:
        mock_central = MagicMock()
        MockW.return_value = mock_central
        mock_layout = MagicMock()
        mock_layout.setSpacing = MagicMock()
        mock_layout.setContentsMargins = MagicMock()
        mock_layout.addWidget = MagicMock()
        MockL.return_value = mock_layout
        mock_tabs = MagicMock()
        MockTabs.return_value = mock_tabs
        mod.build_main_window_ui(window)
        MockTabs.assert_called_once()
        assert window.tabs is mock_tabs
