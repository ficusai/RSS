"""Contract snapshot: gui/_38_bootstrap_launch_window/bootstrap_launch_window.py v1.0.0

Structural contract:
  - Function name: launch_gui_window
  - Signature: () -> int
  - Source imports: sys, PyQt6.QtWidgets.QApplication,
                   gui._37_main_window_facade_assembly.main_window_facade.MainWindow
  - Module source must contain: sys.exit(app.exec()), QApplication(sys.argv), MainWindow()
  - No extra public callables beyond launch_gui_window
"""
# ==============================================================================
# WHAT: Verifies the bootstrap_launch_window structural contract ONLY — source
#       guards confirm sys.exit, QApplication(sys.argv), MainWindow() present.
#       launch_gui_window() is NOT called (it blocks on the event loop).
#
# LAYER BREAKDOWN:
#   Layer 1 (Structural):  test_signature, test_source_imports,
#                          test_source_contains_sys_exit_app_exec,
#                          test_source_contains_qapplication_and_mainwindow,
#                          test_module_has_only_one_public_callable,
#                          test_ast_parses_cleanly
#
# LAYER WHAT EACH TEST CHECKS:
#   test_signature                             — function has no params, returns int
#   test_source_imports                        — sys, QApplication, MainWindow imported via AST
#   test_source_contains_sys_exit_app_exec     — source text contains sys.exit and app.exec()
#   test_source_contains_qapplication_and_mainwindow — source text contains QApplication(sys.argv) and MainWindow()
#   test_module_has_only_one_public_callable   — module defines exactly one public callable
#   test_ast_parses_cleanly                    — source parses as valid Python AST with func def
#
# OPTIONS: N/A — structural/source inspection only.
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: N/A — no runtime behavior verified.
#
# ERRORS/EDGE CASES: N/A.
#
# HOW TO TEST: Run this test file; it inspects source without calling launch_gui_window
# ==============================================================================
import ast
import inspect
import importlib.util
import os

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


# offscreen platform for any PyQt6 imports in source inspection
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    r"""Structural / signature / import contract checks.

    WHAT: Verifies that bootstrap_launch_window is a clean entry-point module:
          the function has the correct no-arg signature returning int, required
          imports are declared, source text contains the expected boot sequence
          patterns, the module has exactly one public callable, and the source
          parses as valid Python AST.

    OPTIONS:
      None — all tests are static source inspection; no Qt event loop needed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Assertions pass if all six structural invariants hold.

    ERRORS/EDGE CASES: Any deviation from the declared contract raises AssertionError.

    HOW TO TEST: Run pytest on this class alone; all tests are fast and deterministic.
    """

    def test_signature(self):
        r"""WHAT: Confirm launch_gui_window accepts zero parameters and annotates
                  return type as int (the exit code from app.exec()).

        OPTIONS:
          None — inspects the real function object directly.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: params == [] and return_annotation is int asserted.

        ERRORS/EDGE CASES: Extra params or wrong return annotation → fail.

        HOW TO TEST: Import the function and call inspect.signature on it.
        """
        from gui._38_bootstrap_launch_window.bootstrap_launch_window import launch_gui_window
        sig = inspect.signature(launch_gui_window)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == []
        assert sig.return_annotation is int

    def test_source_imports(self):
        r"""WHAT: Ensure the source module imports sys, QApplication, and MainWindow,
                  confirming all three boot-sequence dependencies are declared.

        OPTIONS:
          None — uses assert_source_imports helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Assertion passes if all three module paths appear in source AST.

        ERRORS/EDGE CASES: Missing import → assert_source_imports raises AssertionError.

        HOW TO TEST: Run this test; it reads the .py file and walks the AST.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._38_bootstrap_launch_window.bootstrap_launch_window"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"sys", "PyQt6.QtWidgets", "gui._37_main_window_facade_assembly.main_window_facade"},
        )

    def test_source_contains_sys_exit_app_exec(self):
        r"""WHAT: The source of launch_gui_window must contain the strings
                  'sys.exit' and 'app.exec()', confirming the event loop is entered
                  and its return code is passed to the OS.

        OPTIONS:
          None — inspects the function source via inspect.getsource().

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Both substrings found in source text.

        ERRORS/EDGE CASES: Refactored naming (e.g. 'application.exec()') would break this check.

        HOW TO TEST: Call inspect.getsource(launch_gui_window), check substring membership.
        """
        import importlib.util
        from gui._38_bootstrap_launch_window.bootstrap_launch_window import launch_gui_window
        source = inspect.getsource(launch_gui_window)
        assert "sys.exit" in source, "CONTRACT DRIFT — sys.exit(app.exec()) missing from launch_gui_window"
        assert "app.exec()" in source, "CONTRACT DRIFT — app.exec() missing from launch_gui_window"

    def test_source_contains_qapplication_and_mainwindow(self):
        r"""WHAT: The source of launch_gui_window must contain 'QApplication(sys.argv)'
                  and 'MainWindow()', confirming the app and window are constructed
                  with the correct arguments.

        OPTIONS:
          None — inspects the function source via inspect.getsource().

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Both substring patterns found in source text.

        ERRORS/EDGE CASES: Refactored constructor calls would break this check.

        HOW TO TEST: Call inspect.getsource(launch_gui_window), check substring membership.
        """
        import inspect
        from gui._38_bootstrap_launch_window.bootstrap_launch_window import launch_gui_window
        source = inspect.getsource(launch_gui_window)
        assert "QApplication(sys.argv)" in source, "CONTRACT DRIFT — QApplication(sys.argv) missing"
        assert "MainWindow()" in source, "CONTRACT DRIFT — MainWindow() missing"

    def test_module_has_only_one_public_callable(self):
        r"""WHAT: The bootstrap module must define exactly one public callable
                  — launch_gui_window — to enforce the single-entry-point design.

        OPTIONS:
          None — uses assert_callables helper from conftest.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: assert_callables passes when the public callable set equals {"launch_gui_window"}.

        ERRORS/EDGE CASES: Additional public functions or classes would indicate contract drift.

        HOW TO TEST: Import the module and run assert_callables(mod, {"launch_gui_window"}).
        """
        from tests.GUI.conftest import assert_callables
        import importlib.util
        spec = importlib.util.find_spec("gui._38_bootstrap_launch_window.bootstrap_launch_window")
        import importlib
        mod = importlib.import_module("gui._38_bootstrap_launch_window.bootstrap_launch_window")
        assert_callables(mod, {"launch_gui_window"})

    def test_ast_parses_cleanly(self):
        r"""WHAT: The source file must parse as valid Python AST and contain at
                  least one FunctionDef node named 'launch_gui_window'.

        OPTIONS:
          None — uses ast.parse on the raw source file.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: AST parses without error; function name found in walk.

        ERRORS/EDGE CASES: Syntax errors or renamed function would break this check.

        HOW TO TEST: Open spec.origin, ast.parse the content, walk for FunctionDef nodes.
        """
        import importlib.util
        spec = importlib.util.find_spec("gui._38_bootstrap_launch_window.bootstrap_launch_window")
        assert spec is not None
        tree = ast.parse(open(spec.origin).read())
        # Must contain at least one function definition
        func_defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        names = [f.name for f in func_defs]
        assert "launch_gui_window" in names
