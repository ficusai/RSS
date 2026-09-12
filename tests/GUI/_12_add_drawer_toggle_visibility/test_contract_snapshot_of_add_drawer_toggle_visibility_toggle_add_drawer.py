"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_12_add_drawer_toggle_visibility/toggle_add_drawer.py
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
from unittest.mock import MagicMock

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_12_add_drawer_toggle_visibility" / "toggle_add_drawer.py"


def _import_module():
    import gui._12_add_drawer_toggle_visibility.toggle_add_drawer as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence."""
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health."""
    mod = _import_module()
    assert mod is not None


def test_ast_no_imports():
    """Layer 1 — no external imports expected."""
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    assert not found, f"Unexpected imports: {sorted(found)}"


def test_toggle_add_drawer_signature():
    """Layer 1 — toggle_add_drawer(window) -> None."""
    mod = _import_module()
    func = mod.toggle_add_drawer
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_first_call_shows_drawer():
    """Layer 2 — First call: visible=True + text '➖ Hide Drawer'."""
    mod = _import_module()
    window = MagicMock()
    mock_drawer = MagicMock()
    mock_drawer.isVisible = MagicMock(return_value=False)
    mock_drawer.setVisible = MagicMock()
    window.drawer_box = mock_drawer
    mock_btn = MagicMock()
    mock_btn.setText = MagicMock()
    window.btn_toggle_drawer = mock_btn
    mod.toggle_add_drawer(window)
    mock_drawer.setVisible.assert_called_once_with(True)
    mock_btn.setText.assert_called_once_with("➖ Hide Drawer")


def test_second_call_hides_drawer():
    """Layer 2 — Second call: visible=False + text '➕ New Feed / Presets ▾'."""
    mod = _import_module()
    window = MagicMock()
    mock_drawer = MagicMock()
    # After first call, drawer is now visible
    mock_drawer.isVisible = MagicMock(side_effect=[False, True])
    mock_drawer.setVisible = MagicMock()
    window.drawer_box = mock_drawer
    mock_btn = MagicMock()
    mock_btn.setText = MagicMock()
    window.btn_toggle_drawer = mock_btn
    mod.toggle_add_drawer(window)
    mod.toggle_add_drawer(window)
    mock_drawer.setVisible.assert_called_with(False)
    calls = [c[0][0] for c in mock_btn.setText.call_args_list]
    assert "➕ New Feed / Presets ▾" in calls
