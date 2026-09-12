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
# The line above repeats the six headings used in the comments of the SOURCE
# module (WHAT / OPTIONS / DEFAULTS / OUTPUT/EFFECT / ERRORS/EDGE CASES /
# HOW TO TEST). Every sentence in this test file describes one of those for
# the function under test.
#
# What this file protects (source: gui/_12_add_drawer_toggle_visibility/toggle_add_drawer.py):
# The Subscriptions Hub tab has a collapsible "drawer" panel with the add-feed
# form and preset quick-import chips. Clicking the toggle button shows the
# drawer if hidden ("➖ Hide Drawer" caption) or hides it if shown
# ("➕ New Feed / Presets ▾" caption). The function toggles window.drawer_box
# visibility and updates window.btn_toggle_drawer's text in one go.

# ast = Python's "code reader": parses a Python file's text into a structured
# tree so the test can inspect imports and layout WITHOUT running the code.
import ast
# inspect = a scope for Python functions: it lists the parameters and the
# return annotation of a function exactly as declared.
import inspect
# sys = Python runtime controls; here, to add the project folder to the import
# search path so "import gui._12_..." can be resolved.
import sys
# Path = readable file-system paths.
from pathlib import Path
# MagicMock = a fake stand-in object that records method calls. Lets the tests
# mimic a MainWindow without a real screen or real Qt.
from unittest.mock import MagicMock

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# "offscreen" keeps Qt painting into invisible memory so tests run headlessly.
# Add the RSS project root (three folders up) to Python's import search path.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


# Helper. Returns the absolute path of the SOURCE file under test.
# From this test file we go UP to the project root, then back DOWN into
# gui/_12_add_drawer_toggle_visibility/toggle_add_drawer.py.
def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_12_add_drawer_toggle_visibility" / "toggle_add_drawer.py"


# Helper. Imports the SOURCE module being tested and returns it under the
# short alias "mod" so tests can call mod.toggle_add_drawer.
def _import_module():
    import gui._12_add_drawer_toggle_visibility.toggle_add_drawer as mod
    return mod


# TEST — Layer 1 (structural): file existence.
# The implementation file must still live at its contract location.
def test_file_exists():
    """Layer 1 — file existence."""
    # Compute the source path...
    p = _module_path()
    # ...and insist it is on disk, or print which path is missing.
    assert p.exists(), f"Source file missing: {p}"


# TEST — Layer 1 (structural): import health.
# The module must import without errors (no broken imports, no syntax errors).
def test_import_health():
    """Layer 1 — import health."""
    mod = _import_module()
    # A successful import returns a real module object, never None.
    assert mod is not None


# TEST — Layer 1 (structural): "no external imports" contract.
# The source toggle_add_drawer only touches window.drawer_box and
# window.btn_toggle_drawer, so it must contain NO import statements at all.
def test_ast_no_imports():
    """Layer 1 — no external imports expected."""
    # Read the source file's text and parse it into a tree of code-nodes.
    tree = ast.parse(_module_path().read_text())
    # found = set of module names imported by the source file.
    found = set()
    # Walk every node in the tree; node.isinstance checks its shape.
    for node in ast.walk(tree):
        # "import XX" statement (no "from"):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        # "from XX import YY" statement:
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    # An empty set passes; any discovered import fails the test.
    assert not found, f"Unexpected imports: {sorted(found)}"


# TEST — Layer 1 (structural): function signature contract.
# The source must declare exactly: toggle_add_drawer(window) -> None,
# one required parameter without a default, no return value.
def test_toggle_add_drawer_signature():
    """Layer 1 — toggle_add_drawer(window) -> None."""
    mod = _import_module()
    func = mod.toggle_add_drawer      # the actual source function object
    sig = inspect.signature(func)     # read its declared parameters
    # Reduce the signature to (name, kind, default) triples. POSITIONAL_OR_KEYWORD
    # means the caller may pass the argument by position or by keyword.
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    # Recorded contract: one parameter "window", no default value.
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    # The source's def line ends with "-> None": no return value is expected.
    assert sig.return_annotation is None


# TEST — Layer 2 (behaviour): first toggle call SHOWS the drawer.
# Simulates the drawer being HIDDEN, calls the real function once, and checks
# the two side effects: setVisible(True) + the "hide" button caption.
def test_first_call_shows_drawer():
    """Layer 2 — First call: visible=True + text '➖ Hide Drawer'."""
    mod = _import_module()
    window = MagicMock()                    # fake MainWindow
    mock_drawer = MagicMock()               # fake collapsible drawer panel
    # The fake drawer declares itself HIDDEN on the first read (isVisible=False).
    mock_drawer.isVisible = MagicMock(return_value=False)
    mock_drawer.setVisible = MagicMock()    # records the show/hide instruction
    window.drawer_box = mock_drawer
    mock_btn = MagicMock()                  # fake toggle button
    mock_btn.setText = MagicMock()          # records label changes
    window.btn_toggle_drawer = mock_btn
    # Run the real toggle logic: the source computes visible = not False = True,
    # calls setVisible(True), and flips the button label accordingly.
    mod.toggle_add_drawer(window)
    # The drawer was told to become visible exactly once, with the value True.
    mock_drawer.setVisible.assert_called_once_with(True)
    # The button's label was set exactly once, to the "hide" caption.
    mock_btn.setText.assert_called_once_with("➖ Hide Drawer")


# TEST — Layer 2 (behaviour): second toggle call HIDES the drawer again.
# Simulates "drawer was hidden, first call shows it, second call hides it",
# and checks that setVisible(False) was issued and that the caption switched
# back to "➕ New Feed / Presets ▾".
def test_second_call_hides_drawer():
    """Layer 2 — Second call: visible=False + text '➕ New Feed / Presets ▾'."""
    mod = _import_module()
    window = MagicMock()
    mock_drawer = MagicMock()
    # side_effect=[False, True]: the FIRST isVisible() read returns False
    # (used inside call #1 while the drawer is hidden), and the SECOND read
    # returns True (used inside call #2, after call #1 made it visible).
    mock_drawer.isVisible = MagicMock(side_effect=[False, True])
    mock_drawer.setVisible = MagicMock()
    window.drawer_box = mock_drawer
    mock_btn = MagicMock()
    mock_btn.setText = MagicMock()
    window.btn_toggle_drawer = mock_btn
    # Toggle #1: hidden -> shown.
    mod.toggle_add_drawer(window)
    # Toggle #2: shown -> hidden.
    mod.toggle_add_drawer(window)
    # Across all calls, setVisible must have been used with False at least
    # once (hiding the drawer). assert_called_with checks ANY call matched.
    mock_drawer.setVisible.assert_called_with(False)
    # Extract every label text ever handed to setText, in call order.
    calls = [c[0][0] for c in mock_btn.setText.call_args_list]
    # The button must at some point carry the "show the drawer" caption again
    # (because the final toggle left the drawer hidden).
    assert "➕ New Feed / Presets ▾" in calls