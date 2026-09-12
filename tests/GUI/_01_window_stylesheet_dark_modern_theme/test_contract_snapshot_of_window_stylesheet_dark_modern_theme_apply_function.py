"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_01_window_stylesheet_dark_modern_theme/window_stylesheet_apply.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies that the dark modern QSS (Qt Style Sheet) stylesheet module
exposes exactly:
  1. A non-empty STYLESHEET string constant
  2. An apply_window_stylesheet(window) function with exact signature and behavior

The stylesheet is a GitHub Dark-inspired CSS-like theme applied to the entire
MainWindow. This test ensures the stylesheet string and the apply function
have not been accidentally modified.

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_file_exists            : Source file exists on disk
  - test_import_health          : Module imports without errors
  - test_ast_imports            : No imports expected (stylesheet is self-contained)
  - test_stylesheet_non_empty   : STYLESHEET is a non-empty string
  - test_apply_signature        : apply_window_stylesheet(window) -> None exact signature

Layer 2 (Behavioral):
  - test_apply_calls_setStyleSheet: Calling apply_window_stylesheet passes STYLESHEET to window.setStyleSheet()

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# ast: Parses source code into an Abstract Syntax Tree for import verification.
#   More reliable than text search because it understands Python syntax.
import ast
# inspect: Examines live Python objects (functions, methods, parameters, defaults).
#   Used here to verify the exact function signature of apply_window_stylesheet.
import inspect
# sys: Provides sys.path manipulation to add the project root to the import search path.
import sys
# pathlib.Path: Cross-platform filesystem path construction.
from pathlib import Path
# unittest.mock.MagicMock: Creates mock objects that record how they are called.
#   Used to verify that apply_window_stylesheet() actually calls window.setStyleSheet().
from unittest.mock import MagicMock

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# This prevents PyQt6 from trying to open a real display, which would fail in CI.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    """Return the absolute path to the source module under test.

    WHAT: Builds the filesystem path to window_stylesheet_apply.py by navigating
          up three directory levels from this test file's location.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns a Path object pointing to:
                   .../RSS/gui/_01_window_stylesheet_dark_modern_theme/window_stylesheet_apply.py

    ERRORS/EDGE CASES: None — Path construction is safe with any valid string.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_01_window_stylesheet_dark_modern_theme" / "window_stylesheet_apply.py"


def _import_module():
    """Import the source module and return it.

    WHAT: Loads gui._01_window_stylesheet_dark_modern_theme.window_stylesheet_apply
          using Python's standard import system.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns the module object with attributes:
                   - mod.STYLESHEET (str): the QSS stylesheet string
                   - mod.apply_window_stylesheet (function): the apply function

    ERRORS/EDGE CASES:
      - ImportError if the module has syntax errors
      - ModuleNotFoundError if the package structure changed
    """
    import gui._01_window_stylesheet_dark_modern_theme.window_stylesheet_apply as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence.

    WHAT: Asserts the source .py file exists at the expected filesystem path.
          This is the most basic gate — if the file is missing, the module
          cannot be imported and all other tests are meaningless.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if file exists; raises AssertionError with path if not.

    ERRORS/EDGE CASES:
      - File was deleted or moved: AssertionError with file path in message

    HOW TO TEST: Delete window_stylesheet_apply.py, then run this test.
                 It should fail with "Source file missing: /path/to/file.py"
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health.

    WHAT: Verifies the module can be imported without raising any exceptions.
          A module might exist but contain syntax errors, undefined names, or
          circular dependencies that only surface at import time.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns the imported module object. If import succeeds,
                   the module object is truthy (not None).

    ERRORS/EDGE CASES:
      - SyntaxError: source code has invalid Python syntax
      - ImportError: a required dependency is missing
      - RecursionError: circular import between modules

    HOW TO TEST: Add an invalid syntax token (e.g., "def foo(:" missing closing paren)
                 to the source file. Run this test — it should fail with SyntaxError.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports (none expected besides builtin).

    WHAT: Parses the source file's AST and verifies that the module has NO
          explicit imports at all. This module is intentionally self-contained —
          it only defines a string constant and a function, with no dependencies.

    WHY NO IMPORTS: The STYLESHEET string is hardcoded directly in this file.
                    The apply_window_stylesheet function only calls methods on
                    the passed-in window object (no imports needed).

    HOW IT WORKS:
      1. ast.parse() builds a syntax tree from the source code
      2. ast.walk() visits every node in the tree
      3. We collect all import names (both "import X" and "from X import Y")
      4. The resulting set must be empty

    OPTIONS: The expected set is empty {}. No imports should be present.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if no imports are found; fails listing any unexpected ones.

    ERRORS/EDGE CASES:
      - If someone adds "import PyQt6" to the source: "Unexpected imports: ['PyQt6']"
      - Multi-line or parenthesised imports are correctly handled by AST

    HOW TO TEST: Add "from PyQt6.QtWidgets import QWidget" to the source.
                 Run this test — it should fail with "Unexpected imports: ['PyQt6.QtWidgets']".
    """
    tree = ast.parse(_module_path().read_text())
    # found: set of all import module names discovered in the source
    found = set()
    for node in ast.walk(tree):
        # ast.Import: matches "import os", "import os, sys"
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        # ast.ImportFrom: matches "from pathlib import Path"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    # No external imports expected — this module is self-contained
    assert not found, f"Unexpected imports: {sorted(found)}"


def test_stylesheet_non_empty():
    """Layer 1 — STYLESHEET is a non-empty string.

    WHAT: Verifies that the module defines a STYLESHEET attribute that is:
          1. Present (hasattr check)
          2. A Python string type (isinstance check)
          3. Non-empty (len > 0)

    WHY THIS MATTERS:
          The STYLESHEET constant contains the entire GitHub Dark QSS theme.
          If it were empty, the window would render with Qt's default (ugly) style.
          If it were not a string (e.g., accidentally set to None), calling
          window.setStyleSheet(STYLESHEET) would raise a TypeError.

    OPTIONS: None — STYLESHEET must always be a non-empty string.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if STYLESHEET is a non-empty string.

    ERRORS/EDGE CASES:
      - STYLESHEET = "" (empty): fails len() > 0 check
      - STYLESHEET = None: fails isinstance() check
      - STYLESHEET missing entirely: fails hasattr() check

    HOW TO TEST: Set STYLESHEET = "" in the source. Run this test — it should
                 fail the len() > 0 assertion.
    """
    mod = _import_module()
    # hasattr(mod, "STYLESHEET"): checks whether the module has an attribute named "STYLESHEET"
    # If someone renamed the constant, this catches it immediately.
    assert hasattr(mod, "STYLESHEET")
    # isinstance(mod.STYLESHEET, str): ensures the value is a string, not None or a list
    assert isinstance(mod.STYLESHEET, str)
    # len(mod.STYLESHEET) > 0: ensures the stylesheet is not an empty string
    # An empty stylesheet would cause Qt to use default (non-dark) styling
    assert len(mod.STYLESHEET) > 0


def test_apply_signature():
    """Layer 1 — apply_window_stylesheet(window) -> None exact signature.

    WHAT: Uses Python's inspect module to verify that apply_window_stylesheet
          has exactly the right parameter list and return type annotation:
            - One parameter named "window" (required, no default)
            - Return type annotation is None

    WHY SIGNATURE MATTERS:
          Other modules call this function as apply_window_stylesheet(window).
          If the parameter name changed to "app" or "main_win", all callers would
          break with a TypeError. If the return type annotation changed, static
          type checkers (mypy) would flag it.

    HOW inspect.signature Works:
      1. inspect.signature(func) returns a Signature object describing the function's parameters
      2. We iterate over sig.parameters.values() to get each parameter's info
      3. For each param, we extract (name, kind, default) as a tuple
      4. We compare this tuple list against the expected contract

    OPTIONS:
      - Parameter name must be exactly "window"
      - Parameter kind must be POSITIONAL_OR_KEYWORD (can be passed by position or name)
      - No default value (inspect.Parameter.empty means required)
      - Return annotation must be None (not omitted, not str, not anything else)

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if signature matches exactly; fails listing expected vs actual.

    ERRORS/EDGE CASES:
      - Parameter renamed to "app": params mismatch
      - Added default: parent=None: default mismatch
      - Return type changed to "str": return_annotation mismatch

    HOW TO TEST: Change the parameter name from "window" to "app" in the source.
                 Run this test — it should fail with the params mismatch message.
    """
    mod = _import_module()
    # Get the function object from the module
    func = mod.apply_window_stylesheet
    # inspect.signature(func): returns a Signature object describing func's parameters
    sig = inspect.signature(func)
    # Build a list of (name, kind, default) tuples for each parameter
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    # Expected: exactly one parameter named "window", required (no default)
    expected_params = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    # Compare actual parameters against the contract
    assert params == expected_params, f"Expected {expected_params}, got {params}"
    # sig.return_annotation: the type annotation after "->" in the function definition
    # Must be None (not inspect.Parameter.empty which means no annotation)
    assert sig.return_annotation is not inspect.Parameter.empty
    assert sig.return_annotation is None


def test_apply_calls_setStyleSheet():
    """Layer 2 — Calls window.setStyleSheet(STYLESHEET).

    WHAT: Verifies that apply_window_stylesheet actually passes the STYLESHEET
          string to window.setStyleSheet() when called. This is the only behavior
          the function performs — everything else is verified by the signature test.

    HOW MOCKS WORK:
      1. MagicMock() creates a fake object that records all method calls
      2. We pass this fake as the "window" argument
      3. After calling apply_window_stylesheet(window), we check:
         - That window.setStyleSheet was called exactly once
         - That it was called with mod.STYLESHEET as the argument

    OPTIONS: None — the function must call setStyleSheet with STYLESHEET exactly once.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if window.setStyleSheet.assert_called_once_with(mod.STYLESHEET) succeeds.

    ERRORS/EDGE CASES:
      - Function calls setStyleSheet with wrong argument: AssertionError on assert_called_once_with
      - Function calls setStyleSheet twice: AssertionError (assert_called_once requires exactly once)
      - Function doesn't call setStyleSheet at all: AssertionError (mock was never called)

    HOW TO TEST:
      1. Change the function to call window.setStyleSheet("wrong") instead of STYLESHEET
      2. Run this test — it should fail because the argument doesn't match
      3. Change the function to not call setStyleSheet at all
      4. Run this test — it should fail because the mock was never called
    """
    mod = _import_module()
    # MagicMock(): creates a fake object that simulates a QMainWindow.
    # It records every method call so we can verify behavior without a real Qt window.
    window = MagicMock()
    # Call the function under test, passing our mock window
    mod.apply_window_stylesheet(window)
    # assert_called_once_with(mod.STYLESHEET): verifies that setStyleSheet was called
    # exactly once with the STYLESHEET constant as its argument.
    # If called 0 times, 2+ times, or with a different argument, this raises AssertionError.
    window.setStyleSheet.assert_called_once_with(mod.STYLESHEET)
