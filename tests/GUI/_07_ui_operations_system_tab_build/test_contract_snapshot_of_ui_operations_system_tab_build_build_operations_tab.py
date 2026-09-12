"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_07_ui_operations_system_tab_build/build_operations_tab.py
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
    return Path(__file__).resolve().parents[3] / "gui" / "_07_ui_operations_system_tab_build" / "build_operations_tab.py"


def _import_module():
    import gui._07_ui_operations_system_tab_build.build_operations_tab as mod
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
    expected = {"PyQt6.QtWidgets"}
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


def test_build_operations_tab_signature():
    """Layer 1 — build_operations_tab(window) -> None."""
    mod = _import_module()
    func = mod.build_operations_tab
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_lbl_sys_service_created():
    """Layer 2 — lbl_sys_service created."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)


def test_lbl_sys_timer_created():
    """Layer 2 — lbl_sys_timer created."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)


def test_lbl_sys_enabled_created():
    """Layer 2 — lbl_sys_enabled created."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)


def test_log_box_is_qtextedit():
    """Layer 2 — log_box QTextEdit (objectName log_console)."""
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        mock_text = MagicMock()
        mock_text.setObjectName = MagicMock()
        mock_text.setReadOnly = MagicMock()
        MockText.return_value = mock_text
        mod.build_operations_tab(window)
        assert window.log_box is mock_text
        mock_text.setObjectName.assert_called_once_with("log_console")
        mock_text.setReadOnly.assert_called_once_with(True)


def test_btn_clear_connected():
    """Layer 2 — btn_clear connected to window.clear_log."""
    mod = _import_module()
    window = MagicMock()
    window.clear_log = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        mock_btn.clicked.connect.assert_called_once_with(window.clear_log)


def test_btn_refresh_sys_connected():
    """Layer 2 — btn_refresh_sys connected to window.refresh_systemd_status."""
    mod = _import_module()
    window = MagicMock()
    window.refresh_systemd_status = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        # First button is btn_refresh_sys
        calls = mock_btn.clicked.connect.call_args_list
        assert window.refresh_systemd_status in [c[0][0] for c in calls]


def test_btn_install_timer_connected():
    """Layer 2 — btn_install_timer connected to window.handle_install_systemd."""
    mod = _import_module()
    window = MagicMock()
    window.handle_install_systemd = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        calls = mock_btn.clicked.connect.call_args_list
        assert window.handle_install_systemd in [c[0][0] for c in calls]


def test_tab_label():
    """Layer 2 — Tab label '⚙️ Operations & System'."""
    mod = _import_module()
    window = MagicMock()
    window.tabs = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        window.tabs.addTab.assert_called_once()
        call_args = window.tabs.addTab.call_args
        assert call_args[0][1] == "⚙️ Operations & System"
