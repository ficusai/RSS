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

# offscreen platform for any PyQt6 imports in source inspection
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert launch_gui_window() -> int."""
        from gui._38_bootstrap_launch_window.bootstrap_launch_window import launch_gui_window
        sig = inspect.signature(launch_gui_window)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == []
        assert sig.return_annotation is int

    def test_source_imports(self):
        """Source must import sys, QApplication, MainWindow."""
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._38_bootstrap_launch_window.bootstrap_launch_window"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {"sys", "PyQt6.QtWidgets", "gui._37_main_window_facade_assembly.main_window_facade"},
        )

    def test_source_contains_sys_exit_app_exec(self):
        """Source must contain 'sys.exit(app.exec())' pattern."""
        import importlib.util
        from gui._38_bootstrap_launch_window.bootstrap_launch_window import launch_gui_window
        source = inspect.getsource(launch_gui_window)
        assert "sys.exit" in source, "CONTRACT DRIFT — sys.exit(app.exec()) missing from launch_gui_window"
        assert "app.exec()" in source, "CONTRACT DRIFT — app.exec() missing from launch_gui_window"

    def test_source_contains_qapplication_and_mainwindow(self):
        """Source must contain QApplication(sys.argv) and MainWindow()."""
        import inspect
        from gui._38_bootstrap_launch_window.bootstrap_launch_window import launch_gui_window
        source = inspect.getsource(launch_gui_window)
        assert "QApplication(sys.argv)" in source, "CONTRACT DRIFT — QApplication(sys.argv) missing"
        assert "MainWindow()" in source, "CONTRACT DRIFT — MainWindow() missing"

    def test_module_has_only_one_public_callable(self):
        """Module defines exactly one public callable: launch_gui_window."""
        from tests.GUI.conftest import assert_callables
        import importlib.util
        spec = importlib.util.find_spec("gui._38_bootstrap_launch_window.bootstrap_launch_window")
        import importlib
        mod = importlib.import_module("gui._38_bootstrap_launch_window.bootstrap_launch_window")
        assert_callables(mod, {"launch_gui_window"})

    def test_ast_parses_cleanly(self):
        """Source must parse as valid Python AST."""
        import importlib.util
        spec = importlib.util.find_spec("gui._38_bootstrap_launch_window.bootstrap_launch_window")
        assert spec is not None
        tree = ast.parse(open(spec.origin).read())
        # Must contain at least one function definition
        func_defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        names = [f.name for f in func_defs]
        assert "launch_gui_window" in names
