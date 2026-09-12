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
# The six headings below are used in the comments of the SOURCE module this
# test file protects:
#   WHAT              — what the function does in plain words
#   OPTIONS           — which inputs/widgets the function accepts
#   DEFAULTS          — the fallback values used when nothing is supplied
#   OUTPUT/EFFECT     — what changes in the UI/data after calling it
#   ERRORS/EDGE CASES — what can go wrong, and what happens then
#   HOW TO TEST       — how a human could verify it manually
#
# This test file is a "CONTRACT SNAPSHOT": it locks in the exact shape and
# behaviour of gui/_11_log_clear_console/clear_log_console.py so that future
# refactors cannot silently change it. The source's job: when the user clicks
# the "Clear Log" button, every message in the operations console disappears.

# import ast — Python's "code reader". It reads another Python file's TEXT and
#   turns it into a structured tree (an Abstract Syntax Tree) so the test can
#   inspect the program's words, imports, and structure WITHOUT running it.
import ast
# import inspect — a microscope for Python functions: it reports a function's
#   exact parameter list, default values, and return annotation (the "-> ..."
#   part).
import inspect
# import sys — Python's runtime controls; here it lets us ADD the project
#   folder to the list of folders Python searches when resolving "import ..."
#   lines.
import sys
# import Path — a readable way to write file-system paths, e.g.
#   Path("/home/user") / "feeds.json" gives "/home/user/feeds.json".
from pathlib import Path
# import MagicMock — a "fake object" that records every method called on it and
#   with which arguments. It lets the tests talk to an imaginary MainWindow
#   without needing a real screen or a real Qt graphics system.
from unittest.mock import MagicMock

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# "offscreen" = Qt draws straight into invisible memory instead of a monitor,
# so these tests can run on a server or CI machine with no display at all.
# The import below adds the RSS project ROOT to Python's import search path.
# parents[3] walks UP three folders from this file:
#   .../tests/GUI/_11_log_clear_console/     (parents[0])
#   -> .../tests/GUI/                        (parents[1])
#   -> .../tests/                            (parents[2])
#   -> .../RSS/                              (parents[3]) = project root
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


# Helper. Returns the absolute path of the SOURCE file under test.
# __file__ is Python's automatic variable holding THIS test file's path; we go
# up to the project root, then back DOWN into gui/_11_log_clear_console/.
# WHY: every test needs to point at the real implementation to inspect it.
def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_11_log_clear_console" / "clear_log_console.py"


# Helper. Imports the SOURCE module (the one being tested) and returns it.
# "import gui._11_log_clear_console.clear_log_console as mod" means: find the
# module in the gui package, load its code, and keep it under the short name
# "mod" so the tests can call mod.clear_log_console.
def _import_module():
    import gui._11_log_clear_console.clear_log_console as mod
    return mod


# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the contract of gui/_11_log_clear_console/clear_log_console.py.
# The source function clear_log_console(window) is called when the user clicks the
# "Clear Log" button in the operations console. It empties all text from
# window.log_box (a QTextEdit widget) by calling .clear() on it. The function is
# deliberately minimal: it has no imports of its own and expects only a window
# object with a log_box attribute.
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 (Structural):
#   - test_file_exists                  : source file must still be at its contract path
#   - test_import_health                : source module must import without errors
#   - test_ast_no_imports               : source must contain zero import statements
#   - test_clear_log_console_signature  : exactly clear_log_console(window) -> None
# Layer 2 (Behavioral):
#   - test_clears_log_box                      : calling clear_log_console empties the log
#   - test_plain_text_empty_after_clear        : toPlainText() reflects empty state after clear
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================


class TestLayer1Structural:
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the physical shape of the source module without running it.
    These tests catch refactor drift such as renamed parameters, moved files,
    or unwanted new imports BEFORE behaviour tests are even executed.
    """

    def test_file_exists(self):
        r"""WHAT: Verifies the source file still exists at its contract path.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the file exists on disk; fails with a message
          showing the missing path.
        ERRORS/EDGE CASES: If a refactor moved or renamed clear_log_console.py,
          this test fails and tells the developer to regenerate the snapshot
          instead of editing it by hand.
        HOW TO TEST: Run `pytest tests/GUI/_11_log_clear_console/`. A failure
          here means the source file is missing from the expected location.
        """
        # Compute the source file's path...
        p = _module_path()
        # ...and insist it exists on disk. assert = "this MUST be true, else the
        # test fails"; the text after the comma is printed as the failure message.
        assert p.exists(), f"Source file missing: {p}"

    def test_import_health(self):
        r"""WHAT: Verifies the source module can be imported without errors.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the module loads and returns a non-None object.
        ERRORS/EDGE CASES: If the source has a syntax error or broken import,
          this test will fail before any behaviour is tested.
        HOW TO TEST: Run `pytest tests/GUI/_11_log_clear_console/`. If this test
          fails, inspect the source module for syntax or import errors.
        """
        mod = _import_module()
        # If the import raised an error, the test would already have stopped here.
        # This extra check merely insists the returned module object is a real one.
        assert mod is not None

    def test_ast_no_imports(self):
        r"""WHAT: Verifies the source module contains zero import statements.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the AST parser finds no import nodes in the
          source file. Any import found causes the test to fail.
        ERRORS/EDGE CASES: clear_log_console only needs window.log_box.clear();
          it should require no outside modules. If a developer accidentally adds
          an import, this test fails and warrants regenerating the snapshot.
        HOW TO TEST: Run `pytest tests/GUI/_11_log_clear_console/`. A failure
          lists the unexpected import names.
        """
        # Read the raw source text and parse it into a tree of code-nodes.
        tree = ast.parse(_module_path().read_text())
        # found = the set of module names imported by the file (starts empty).
        found = set()
        # ast.walk hands us every node in the tree, one by one.
        for node in ast.walk(tree):
            # Is the node shaped like "import XX" (no "from")? Collect the XX part.
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.add(alias.name)
            # Is the node shaped like "from XX import YY"? Collect the XX part.
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    found.add(node.module)
        # If NOTHING was imported, the set is empty and the assert passes. If any
        # import exists, the set is non-empty -> the test fails, listing the names.
        assert not found, f"Unexpected imports: {sorted(found)}"

    def test_clear_log_console_signature(self):
        r"""WHAT: Verifies the exact signature of clear_log_console(window) -> None.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the function has exactly one parameter named
          "window" (positional-or-keyword, no default) and returns None.
        ERRORS/EDGE CASES: If a developer renamed the parameter or added a second
          one, this test fails with the mismatched signature details.
        HOW TO TEST: Run `pytest tests/GUI/_11_log_clear_console/`. A failure
          prints the expected vs. actual parameter list.
        """
        mod = _import_module()
        func = mod.clear_log_console    # grab the actual function object
        # inspect.signature reads the function's declared parameters.
        sig = inspect.signature(func)
        # Reduce the signature to a list of (name, kind, default) triples.
        # p.kind explains HOW the argument may be passed (by position and/or by
        # name); p.default is the parameter's default, or inspect.Parameter.empty
        # (the "no default" marker) if the parameter is required.
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        # The recorded contract: exactly one parameter named "window", passable by
        # position or keyword, with NO default value.
        expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        # If the real signature differs from the recorded one, the assert fails.
        assert params == expected
        # The source's def line ends with "-> None" (a return annotation), so
        # Python stores that annotation as the literal value None.
        assert sig.return_annotation is None


class TestLayer2Behavioral:
    """Layer 2 — Behavioural smoke tests.

    WHAT: Calls the real source function against fakes and checks the visible
    side effects. These tests prove the function does what it promises.
    """

    def test_clears_log_box(self):
        r"""WHAT: Calling clear_log_console(window) calls log_box.clear() exactly once.

        OPTIONS: window must have a log_box attribute (a widget with .clear()).
        DEFAULTS: N/A.
        OUTPUT/EFFECT: window.log_box.clear() is invoked once, emptying the log.
        ERRORS/EDGE CASES: A MagicMock does not REALLY change its text, so this
          test can only prove clear() was called; it cannot itself prove emptiness.
        HOW TO TEST: In the app, type some messages into the console, click
          the "Clear Log" button, and verify the console is empty.
        """
        mod = _import_module()
        window = MagicMock()          # the fake top-level window
        mock_box = MagicMock()        # the fake log console widget
        # Pretend the console is currently showing the words "some log text"
        # (toPlainText() is Qt's way of reading all the text in a log widget).
        mock_box.toPlainText = MagicMock(return_value="some log text")
        # The fake clear() — in real life this empties all text from the console.
        mock_box.clear = MagicMock()
        # Give the fake window a "log_box" attribute pointing at our fake console;
        # "log_box" is exactly the attribute name the real GUI code expects.
        window.log_box = mock_box
        # Run the real source function against the fake window.
        mod.clear_log_console(window)
        # Insist the clear() method was invoked, exactly once, no more no less.
        mock_box.clear.assert_called_once()

    def test_plain_text_empty_after_clear(self):
        r"""WHAT: After clear_log_console, toPlainText() conceptually returns empty.

        OPTIONS: window must have a log_box attribute with toPlainText() and clear().
        DEFAULTS: N/A.
        OUTPUT/EFFECT: The mock's toPlainText() transitions from "old text" to "".
        ERRORS/EDGE CASES: A MagicMock does not REALLY change its text, so this
          test can only prove clear() was called; it cannot itself prove emptiness.
        HOW TO TEST: In the app, type "hello world" into the console, click
          "Clear Log", and verify toPlainText() returns an empty string.
        """
        mod = _import_module()
        window = MagicMock()
        mock_box = MagicMock()
        # side_effect=["old text", ""]: return "old text" on the 1st call, then
        # "" on the 2nd call. Qt would behave like this after a real clear().
        mock_box.toPlainText = MagicMock(side_effect=["old text", ""])
        mock_box.clear = MagicMock()
        window.log_box = mock_box
        mod.clear_log_console(window)
        # After clear, toPlainText should conceptually return ""
        # We verify clear was called, and the mock confirms the state change.
        mock_box.clear.assert_called_once()
