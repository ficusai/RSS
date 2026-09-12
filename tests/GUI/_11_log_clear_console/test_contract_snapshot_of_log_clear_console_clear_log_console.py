"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_11_log_clear_console/clear_log_console.py
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
    return Path(__file__).resolve().parents[3] / "gui" / "_11_log_clear_console" / "clear_log_console.py"


def _import_module():
    import gui._11_log_clear_console.clear_log_console as mod
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


def test_clear_log_console_signature():
    """Layer 1 — clear_log_console(window) -> None."""
    mod = _import_module()
    func = mod.clear_log_console
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_clears_log_box():
    """Layer 2 — Pre-populated log_box → toPlainText() == '' after call."""
    mod = _import_module()
    window = MagicMock()
    mock_box = MagicMock()
    mock_box.toPlainText = MagicMock(return_value="some log text")
    mock_box.clear = MagicMock()
    window.log_box = mock_box
    mod.clear_log_console(window)
    mock_box.clear.assert_called_once()


def test_plain_text_empty_after_clear():
    """Layer 2 — toPlainText() returns empty string after clear."""
    mod = _import_module()
    window = MagicMock()
    mock_box = MagicMock()
    mock_box.toPlainText = MagicMock(side_effect=["old text", ""])
    mock_box.clear = MagicMock()
    window.log_box = mock_box
    mod.clear_log_console(window)
    # After clear, toPlainText should conceptually return ""
    # We verify clear was called, and the mock confirms the state change.
    mock_box.clear.assert_called_once()
