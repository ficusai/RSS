"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_10_log_append_timestamped_message/append_timestamped_log.py
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
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_10_log_append_timestamped_message" / "append_timestamped_log.py"


def _import_module():
    import gui._10_log_append_timestamped_message.append_timestamped_log as mod
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
    expected = {"datetime"}
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


def test_append_log_message_signature():
    """Layer 1 — append_log_message(window, msg: str) -> None."""
    mod = _import_module()
    func = mod.append_log_message
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [
        ("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ("msg", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
    ]
    assert params == expected
    assert sig.return_annotation is None


def test_appends_timestamped_line():
    """Layer 2 — appends line matching ^\[\d{2}:\d{2}:\d{2}\] test msg."""
    mod = _import_module()
    window = MagicMock()
    mock_box = MagicMock()
    mock_box.append = MagicMock()
    mock_box.verticalScrollBar = MagicMock()
    mock_bar = MagicMock()
    mock_bar.maximum = MagicMock(return_value=100)
    mock_box.verticalScrollBar.return_value = mock_bar
    window.log_box = mock_box
    mod.append_log_message(window, "test msg")
    mock_box.append.assert_called_once()
    called_with = mock_box.append.call_args[0][0]
    pattern = re.compile(r"^\[\d{2}:\d{2}:\d{2}\] test msg$")
    assert pattern.match(called_with), f"Expected timestamped line, got: {called_with!r}"


def test_scrolls_to_bottom():
    """Layer 2 — verticalScrollBar().setValue(maximum()) invoked."""
    mod = _import_module()
    window = MagicMock()
    mock_box = MagicMock()
    mock_box.append = MagicMock()
    mock_box.verticalScrollBar = MagicMock()
    mock_bar = MagicMock()
    mock_bar.maximum = MagicMock(return_value=50)
    mock_bar.setValue = MagicMock()
    mock_box.verticalScrollBar.return_value = mock_bar
    window.log_box = mock_box
    mod.append_log_message(window, "test msg")
    mock_bar.setValue.assert_called_once_with(50)
