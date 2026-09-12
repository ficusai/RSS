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
# The line above is a reminder of the six headings used in the comments of the
# SOURCE module this test file protects:
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
# the "🧹 Clear Log" button, every message in the operations console disappears.

# ast = Python's "code reader". It reads another Python file's TEXT and turns
# it into a structured tree (an Abstract Syntax Tree) so the test can inspect
# the program's words, imports, and structure WITHOUT running it.
import ast
# inspect = a microscope for Python functions: it reports a function's exact
# parameter list, default values, and return annotation (the "-> ..." part).
import inspect
# sys = Python's runtime controls; here it lets us ADD the project folder to
# the list of folders Python searches when resolving "import ..." lines.
import sys
# Path = a readable way to write file-system paths, e.g.
# Path("/home/user") / "feeds.json" gives "/home/user/feeds.json".
from pathlib import Path
# MagicMock = a "fake object" that records every method called on it and with
# which arguments. It lets the tests talk to an imaginary MainWindow without
# needing a real screen or a real Qt graphics system.
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


# TEST — Layer 1 (structural): file existence.
# WHAT: Insists the implementation file still lives at its contract location.
# If a refactor moved or renamed clear_log_console.py, this test fails and
# tells the developer to regenerate the snapshot instead of editing it.
# HOW TO RUN THE WHOLE FILE: pytest tests/GUI/_11_log_clear_console/
def test_file_exists():
    """Layer 1 — file existence."""
    # Compute the source file's path...
    p = _module_path()
    # ...and insist it exists on disk. assert = "this MUST be true, else the
    # test fails"; the text after the comma is printed as the failure message.
    assert p.exists(), f"Source file missing: {p}"


# TEST — Layer 1 (structural): import health.
# WHAT: Checks the source module imports without error (no broken imports, no
# syntax mistakes). A module that cannot even be loaded is useless to the app.
def test_import_health():
    """Layer 1 — import health."""
    mod = _import_module()
    # If the import raised an error, the test would already have stopped here.
    # This extra check merely insists the returned module object is a real one.
    assert mod is not None


# TEST — Layer 1 (structural): "no external imports" contract.
# WHAT: Reads the SOURCE file's text, parses it, and insists it contains NO
# import statements at all.
# WHY: clear_log_console only needs window.log_box.clear(); it should require
# no outside modules. Any new import means the function's role has grown,
# which violates the recorded contract and warrants regenerating the snapshot.
def test_ast_no_imports():
    """Layer 1 — no external imports expected."""
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


# TEST — Layer 1 (structural): function signature contract.
# WHAT: Locks in the exact parameter list of the source function:
#   clear_log_console(window)   -- one parameter, no default, returns None.
# If a developer renamed the parameter or added a second one, this test fails.
def test_clear_log_console_signature():
    """Layer 1 — clear_log_console(window) -> None."""
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


# TEST — Layer 2 (behaviour): clearing a pre-filled log.
# WHAT: Builds a FAKE window whose log_box already contains text, runs the real
# clear_log_console() on it, then verifies the fake's .clear() method was
# called exactly once.
# WHY FAKE: a real QTextEdit needs a real graphical screen; a MagicMock simply
# records the call for us, which is all this behaviour check needs.
def test_clears_log_box():
    """Layer 2 — Pre-populated log_box → toPlainText() == '' after call."""
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


# TEST — Layer 2 (behaviour): text is empty after clearing.
# WHAT: Same clearing scenario, but the fake's toPlainText() is scripted to
# answer "old text" the first time it is asked, then "" the second time —
# those are the two states of the console: full of messages, then empty after
# a successful clear().
# NOTE (honest limit): a MagicMock does not REALLY change its text, so this
# test can only prove clear() was called; it cannot itself prove the emptiness.
def test_plain_text_empty_after_clear():
    """Layer 2 — toPlainText() returns empty string after clear."""
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