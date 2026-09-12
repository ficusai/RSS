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
# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# This test file verifies the contract of
# gui._10_log_append_timestamped_message.append_timestamped_log. It checks that
# the source module file exists, imports correctly, has the expected AST-import
# set (datetime), that append_log_message has the correct signature
# (window, msg: str) -> None, and that calling it with a MagicMock window
# appends a timestamped line matching ^\[\d{2}:\d{2}:\d{2}\] <msg>$ and scrolls
# the log console's vertical scrollbar to the bottom.
# ==============================================================================
# ==============================================================================
# LAYER BREAKDOWN
#   Layer 1 — Module-level contract checks:
#     * test_file_exists: source .py file is present on disk.
#     * test_import_health: the module can be imported without error.
#     * test_ast_imports: the expected datetime import is present via AST.
#     * test_append_log_message_signature: func(window, msg: str) -> None signature.
#   Layer 2 — Behavioural contract checks (mocked Qt):
#     * test_appends_timestamped_line: the appended line matches the timestamp regex.
#     * test_scrolls_to_bottom: verticalScrollBar().setValue(maximum()) is invoked.
# ==============================================================================
# ==============================================================================
# LAYER WHAT EACH TEST CHECKS
#   Layer 1 tests verify the module's structural contract (file presence, import
#   health, static import set, function signature).
#   Layer 2 tests verify the runtime behaviour contract by mocking the log box
#   and asserting on the exact text appended and the scrollbar scroll action.
# ==============================================================================
# OVERVIEW OF IMPORTS
# import ast: abstract syntax tree parser; used to verify source-module imports statically.
# import inspect: runtime introspection; used to inspect function signatures.
# import re: regular-expression engine; used to match the timestamp pattern in appended lines.
# import sys: Python runtime; used to prepend the repo root to sys.path.
# import Path from pathlib: filesystem path builder; used to resolve the source-module file path.
# import MagicMock from unittest.mock: test double; used to replace the MainWindow log_box during Layer 2 tests.
import ast
import inspect
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    r"""Return the absolute Path to the source module under test.

    WHAT: Builds the filesystem path to the source .py file.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: A pathlib.Path pointing to gui/_10_log_append_timestamped_message/append_timestamped_log.py.
    EFFECT: None (pure function).
    ERRORS/EDGE CASES: Should never fail; returns a Path even if the file does not exist.
    EDGE CASES: None.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_10_log_append_timestamped_message" / "append_timestamped_log.py"


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
    import gui._10_log_append_timestamped_message.append_timestamped_log as mod
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

    WHAT: Verifies the expected datetime import is present in the source AST.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if any expected import is missing.
    ERRORS/EDGE CASES: SyntaxError if source file has invalid Python.
    EDGE CASES: None.
    HOW TO TEST: Parse the source AST and walk for Import/ImportFrom nodes.
    """
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
    r"""Layer 1 — append_log_message(window, msg: str) -> None.

    WHAT: Verifies the exact function signature of append_log_message.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if signature differs.
    ERRORS/EDGE CASES: AttributeError if the function does not exist on the module.
    EDGE CASES: None.
    HOW TO TEST: Use inspect.signature and compare parameters + return annotation.
    """
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
    r"""Layer 2 — appends line matching ^\[\d{2}:\d{2}:\d{2}\] test msg.

    WHAT: Verifies that append_log_message prepends a HH:MM:SS timestamp in
          square brackets to the message and appends it to window.log_box.
    OPTIONS: window — MagicMock with log_box attribute. msg — the test string.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if the appended line does not match the regex.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Provide a MagicMock log_box with an append method; call the
                 function; assert append was called once and the argument matches
                 the compiled timestamp regex pattern.
    """
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
    r"""Layer 2 — verticalScrollBar().setValue(maximum()) invoked.

    WHAT: Verifies that append_log_message scrolls the log console to the
          bottom after appending a line by calling
          verticalScrollBar().setValue(verticalScrollBar().maximum()).
    OPTIONS: window — MagicMock with log_box attribute. msg — the test string.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if setValue was not called with maximum().
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Provide a MagicMock log_box with append and verticalScrollBar;
                 mock maximum() to return a known value; call the function;
                 assert setValue was called once with that maximum value.
    """
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
