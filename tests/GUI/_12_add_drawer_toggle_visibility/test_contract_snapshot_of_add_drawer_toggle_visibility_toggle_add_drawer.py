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
# The six headings below repeat the annotations used in the SOURCE module
# (WHAT / OPTIONS / DEFAULTS / OUTPUT/EFFECT / ERRORS/EDGE CASES /
# HOW TO TEST). Every sentence in this test file describes one of those for
# the function under test.
#
# What this file protects (source: gui/_12_add_drawer_toggle_visibility/toggle_add_drawer.py):
# The Subscriptions Hub tab has a collapsible "drawer" panel with the add-feed
# form and preset quick-import chips. Clicking the toggle button shows the
# drawer if hidden ("Hide Drawer" caption) or hides it if shown
# ("New Feed / Presets  caption). The function toggles window.drawer_box
# visibility and updates window.btn_toggle_drawer's text in one go.

# import ast — Python's "code reader": parses a Python file's text into a
#   structured tree so the test can inspect imports and layout WITHOUT running
#   the code.
import ast
# import inspect — a scope for Python functions: it lists the parameters and
#   the return annotation of a function exactly as declared.
import inspect
# import sys — Python runtime controls; here, to add the project folder to the
#   import search path so "import gui._12_..." can be resolved.
import sys
# import Path — readable file-system paths.
from pathlib import Path
# import MagicMock — a fake stand-in object that records method calls. Lets the
#   tests mimic a MainWindow without a real screen or real Qt.
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


===============================================================================
============== WHAT THIS TEST FILE VERIFIES ===============
This file protects the contract of
gui/_12_add_drawer_toggle_visibility/toggle_add_drawer.py. The source function
toggle_add_drawer(window) toggles the visibility of the collapsible "New Feed /
Presets" drawer panel. When called, it reads the current visibility state of
window.drawer_box, inverts it, and updates window.btn_toggle_drawer's caption
between "Hide Drawer" (when showing) and "New Feed / Presets  " (when hiding).
===============================================================================
============== LAYER BREAKDOWN ===============
Layer 1 (Structural):
  - test_file_exists                   : source file must still be at its contract path
  - test_import_health                 : source module must import without errors
  - test_ast_no_imports                : source must contain zero import statements
  - test_toggle_add_drawer_signature   : exactly toggle_add_drawer(window) -> None
Layer 2 (Behavioral):
  - test_first_call_shows_drawer          : first toggle call sets visible=True + hide caption
  - test_second_call_hides_drawer         : second toggle call sets visible=False + show caption
===============================================================================
============== LAYER WHAT EACH TEST CHECKS ===============
===============================================================================


class TestLayer1Structural:
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the physical shape of the source module without running it.
    These tests catch refactor drift such as renamed parameters, moved files,
    or unwanted new imports BEFORE behaviour tests are even executed.
    """

    def test_file_exists(self):
        """WHAT: Verifies the source file still exists at its contract path.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the file exists on disk; fails with a message
          showing the missing path.
        ERRORS/EDGE CASES: If a refactor moved or renamed toggle_add_drawer.py,
          this test fails and tells the developer to regenerate the snapshot.
        HOW TO TEST: Run `pytest tests/GUI/_12_add_drawer_toggle_visibility/`.
          A failure here means the source file is missing from the expected path.
        """
        # Compute the source path...
        p = _module_path()
        # ...and insist it is on disk, or print which path is missing.
        assert p.exists(), f"Source file missing: {p}"

    def test_import_health(self):
        """WHAT: Verifies the source module can be imported without errors.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the module loads and returns a non-None object.
        ERRORS/EDGE CASES: If the source has a syntax error or broken import,
          this test will fail before any behaviour is tested.
        HOW TO TEST: Run `pytest tests/GUI/_12_add_drawer_toggle_visibility/`.
          If this test fails, inspect the source module for syntax errors.
        """
        mod = _import_module()
        # A successful import returns a real module object, never None.
        assert mod is not None

    def test_ast_no_imports(self):
        """WHAT: Verifies the source module contains zero import statements.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the AST parser finds no import nodes in the
          source file. Any import found causes the test to fail.
        ERRORS/EDGE CASES: toggle_add_drawer only touches window.drawer_box and
          window.btn_toggle_drawer, so it must contain no import statements at
          all. If a new import appears, the contract is broken.
        HOW TO TEST: Run `pytest tests/GUI/_12_add_drawer_toggle_visibility/`.
          A failure lists the unexpected import names.
        """
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

    def test_toggle_add_drawer_signature(self):
        """WHAT: Verifies the exact signature of toggle_add_drawer(window) -> None.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the function has exactly one parameter named
          "window" (positional-or-keyword, no default) and returns None.
        ERRORS/EDGE CASES: If a developer renamed the parameter or added a
          second one, this test fails with the mismatched signature details.
        HOW TO TEST: Run `pytest tests/GUI/_12_add_drawer_toggle_visibility/`.
          A failure prints the expected vs. actual parameter list.
        """
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


class TestLayer2Behavioral:
    """Layer 2 — Behavioural smoke tests.

    WHAT: Calls the real source function against fakes and checks the visible
    side effects. These tests prove the function toggles the drawer correctly.
    """

    def test_first_call_shows_drawer(self):
        """WHAT: First toggle call shows the drawer and sets the hide caption.

        OPTIONS: window must have drawer_box (with isVisible/setVisible) and
          btn_toggle_drawer (with setText).
        DEFAULTS: N/A.
        OUTPUT/EFFECT: drawer_box.setVisible(True) and
          btn_toggle_drawer.setText("Hide Drawer") are each called once.
        ERRORS/EDGE CASES: None documented — the function assumes valid widgets.
        HOW TO TEST: In the app, with the drawer hidden, click the toggle
          button. The drawer panel should appear and the button should read
          "Hide Drawer".
        """
        mod = _import_module()
        window = MagicMock()                    # fake MainWindow
        mock_drawer = MagicMock()               # fake collapsible drawer panel
        # The fake drawer declares itself HIDDEN on the first read
        # (isVisible=False).
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

    def test_second_call_hides_drawer(self):
        """WHAT: Second toggle call hides the drawer and restores the show caption.

        OPTIONS: window must have drawer_box (with isVisible/setVisible) and
          btn_toggle_drawer (with setText).
        DEFAULTS: N/A.
        OUTPUT/EFFECT: drawer_box.setVisible(False) and
          btn_toggle_drawer.setText("New Feed / Presets  ") are issued.
        ERRORS/EDGE CASES: None documented — the function assumes valid widgets.
        HOW TO TEST: In the app, show the drawer (first toggle), then click the
          toggle button again. The drawer should disappear and the button
          caption should read "New Feed / Presets  ".
        """
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
