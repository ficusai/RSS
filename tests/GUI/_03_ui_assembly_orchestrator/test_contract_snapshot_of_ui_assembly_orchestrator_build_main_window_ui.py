"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_03_ui_assembly_orchestrator/build_main_window_ui.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.
"""

# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# ==============================================================================
# This test file verifies the contract of build_main_window_ui, the orchestrator
# function that assembles the complete MainWindow UI. It creates the central
# widget, root QVBoxLayout, header bar, hidden progress bar, QTabWidget, and
# calls each of the five tab-builder functions (articles, subscriptions,
# operations, presets) to populate the tab container. The function acts as a
# thin coordination layer — it does not implement tab content itself but
# ensures every sub-builder is invoked exactly once with the window object.
# ==============================================================================

# ==============================================================================
# LAYER BREAKDOWN
# ==============================================================================
# Layer 1 (Structural):
#   - test_file_exists : verifies the source .py file exists on disk
#   - test_import_health : verifies the module can be imported without errors
#   - test_ast_imports : AST-parses the source to verify all expected imports are present
#   - test_build_main_window_ui_signature : verifies build_main_window_ui(window) -> None exact signature
#
# Layer 2 (Behavioral):
#   - test_build_calls_sub_builders : verifies all five tab builders are called exactly once with window
#   - test_creates_progress_bar : verifies QProgressBar is created with textVisible=False and visible=False
#   - test_creates_tabs_widget : verifies QTabWidget is created and stored as window.tabs
# ==============================================================================

# ==============================================================================
# LAYER WHAT EACH TEST CHECKS
# ==============================================================================
# Layer 1 tests confirm the structural contract: the module file is present,
# imports are correct, and the orchestrator function has the right signature.
# These catch regressions where a developer renames the function, drops an
# import, or changes parameter names.
#
# Layer 2 tests confirm behavioral contract: the orchestrator calls each
# sub-builder once (ensuring no tab is skipped), creates a hidden progress
# bar for download feedback, and constructs a QTabWidget stored on the window.
# These catch logic drift where the assembly order changes or a builder call
# is accidentally removed.
# ==============================================================================


# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# import ast: parses Python source code into an Abstract Syntax Tree (AST) so we can inspect imports without executing the module.
# import inspect: inspects function and class signatures at runtime — used to verify parameter names, kinds, defaults, and return annotations.
# import sys: manipulates the Python module search path (sys.path) so tests can import gui modules from the project root.
# from pathlib import Path: provides object-oriented filesystem path manipulation to locate the source module relative to this test file.
# from unittest.mock import MagicMock, patch: creates fake objects (MagicMock) and temporarily replaces real functions (patch) to isolate the unit under test.
# from PyQt6.QtWidgets import QApplication: required before any Qt widget construction; initializes the Qt application context for tests.
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
# PyQt6.QtWidgets.QApplication: Required before any Qt widget construction.
from PyQt6.QtWidgets import QApplication
_qapp = QApplication.instance() or QApplication([])

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    r"""Return the absolute Path to the source module being tested.

    WHAT:
      Constructs and returns the filesystem path to build_main_window_ui.py,
      the source module whose contract this test file verifies.

    OPTIONS:
      None. This function takes no arguments.

    DEFAULTS:
      None.

    OUTPUT:
      A pathlib.Path object pointing to:
        <project_root>/gui/_03_ui_assembly_orchestrator/build_main_window_ui.py

    EFFECT:
      No side effects. Pure function.

    ERRORS/EDGE CASES:
      None expected. Path resolution is deterministic given a fixed filesystem layout.

    HOW TO TEST:
      1. Run this test file.
      2. Assert the returned path exists with .exists().
      Example: p = _module_path(); assert p.exists()
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_03_ui_assembly_orchestrator" / "build_main_window_ui.py"


def _import_module():
    r"""Import and return the source module under test.

    WHAT:
      Dynamically imports gui._03_ui_assembly_orchestrator.build_main_window_ui
      and returns the module object so tests can access the build_main_window_ui function.

    OPTIONS:
      None. This function takes no arguments.

    DEFAULTS:
      None.

    OUTPUT:
      The imported module object (sys.modules entry for gui._03_ui_assembly_orchestrator.build_main_window_ui).

    EFFECT:
      The module is loaded into sys.modules. Any module-level side effects
      (e.g., Qt application initialization) will execute.

    ERRORS/EDGE CASES:
      - If the source module has a syntax error, ImportError or SyntaxError is raised.
      - If the module is already cached in sys.modules, the cached version is returned.
      - If PYTHONPATH or sys.path does not include the project root, ImportError is raised.

    HOW TO TEST:
      1. Call mod = _import_module().
      2. Assert mod is not None.
      3. Access mod.build_main_window_ui to verify the function is available.
      Example: mod = _import_module(); assert callable(mod.build_main_window_ui)
    """
    import gui._03_ui_assembly_orchestrator.build_main_window_ui as mod
    return mod


def test_file_exists():
    r"""Layer 1 — Source file must exist on disk.

    WHAT:
      Verifies that the source module file build_main_window_ui.py is present
      at the expected location in the project's gui/ directory.

    WHY:
      If the file is missing, all other tests in this suite will fail with
      ImportError, making diagnosis harder. Catching a missing file first
      gives a clear, actionable error message.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if the file exists; raises AssertionError with the file path
      if the file is missing.

    ERRORS/EDGE CASES:
      - File moved or deleted: assertion fails with the full path printed.
      - Symlink broken: assertion fails (Path.exists() returns False for broken symlinks).

    HOW TO TEST:
      1. Confirm the file exists at gui/_03_ui_assembly_orchestrator/build_main_window_ui.py.
      2. Rename or delete it temporarily — the test should fail with a clear path message.
      3. Restore the file — the test should pass again.
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    r"""Layer 1 — Module must import without raising any exception.

    WHAT:
      Verifies that importing the source module completes successfully with
      no SyntaxError, ImportError, or other exception.

    WHY:
      A module that cannot be imported is fundamentally broken. This test
      catches syntax errors, missing dependencies, or circular import issues
      before any deeper structural or behavioral tests run.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if import succeeds and returns a non-None module object.
      Raises any exception thrown during import if it occurs.

    ERRORS/EDGE CASES:
      - Missing dependency (e.g., PyQt6 not installed): ImportError propagates.
      - Circular import: ImportError or RecursionError propagates.
      - Module already cached: returns cached module (still valid).

    HOW TO TEST:
      1. Call mod = _import_module() — should not raise.
      2. Temporarily introduce a syntax error in the source — test should fail.
      3. Restore the source — test should pass again.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    r"""Layer 1 — All expected imports must be present in the source AST.

    WHAT:
      Parses the source file with Python's ast module and verifies that the
      following imports are present: PyQt6.QtCore, PyQt6.QtWidgets, and the
      five tab-builder functions from gui._04 through gui._08. Missing any
      of these would cause runtime import failures.

    WHY:
      Dynamic imports (importlib) could miss renamed or removed imports.
      AST parsing statically inspects the source text, catching import
      drift even before the module is executed.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if all expected import modules are found in the AST.
      Raises AssertionError listing the missing import names.

    ERRORS/EDGE CASES:
      - Import renamed (e.g., gui._04_ui_header_bar_top_section_build -> gui._04_header): assertion fails with missing import listed.
      - Import dropped entirely: assertion fails.
      - Import aliased (as X): still detected because AST checks node.module, not alias.name.

    HOW TO TEST:
      1. Remove one expected import from the source — test should fail listing the missing name.
      2. Add an extra unexpected import — test should still pass (only checks for expected set).
      3. Restore the source — test should pass again.
    """
    expected = {
        "PyQt6.QtCore",
        "PyQt6.QtWidgets",
        "gui._04_ui_header_bar_top_section_build.build_header_bar",
        "gui._05_ui_articles_explorer_tab_build.build_articles_tab",
        "gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab",
        "gui._07_ui_operations_system_tab_build.build_operations_tab",
        "gui._08_ui_presets_library_tab_build.build_presets_tab",
    }
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


def test_build_main_window_ui_signature():
    r"""Layer 1 — build_main_window_ui must accept (window) and return None.

    WHAT:
      Verifies that build_main_window_ui has exactly one parameter named
      window (positional-or-keyword, no default) and that its return type
      annotation is None.

    WHY:
      The function signature is the public contract. The main window code
      calls build_main_window_ui(window) with the MainWindow instance.
      Changing the parameter name or adding required parameters would break
      the call site.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if the signature matches exactly.
      Raises AssertionError with expected vs. actual parameter list.

    ERRORS/EDGE CASES:
      - Parameter renamed (e.g., window -> main_win): assertion fails.
      - Default added (e.g., window=None): assertion fails (Parameter.empty vs None).
      - Extra parameter added: assertion fails (length mismatch).
      - Return annotation changed (e.g., -> int): assertion fails.

    HOW TO TEST:
      1. Rename the parameter in source — test should fail.
      2. Add a second parameter — test should fail.
      3. Change return annotation from None to int — test should fail.
      4. Restore — test should pass again.
    """
    mod = _import_module()
    func = mod.build_main_window_ui
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_build_calls_sub_builders():
    r"""Layer 2 — build_main_window_ui must call each sub-builder exactly once.

    WHAT:
      Mocks the five sub-builder functions (build_header_bar, build_articles_tab,
      build_subscriptions_tab, build_operations_tab, build_presets_tab) and
      calls build_main_window_ui. Verifies each mock was called exactly once
      with the window object as its sole argument.

    WHY:
      This is the core coordination contract. If a sub-builder is called zero
      times, that UI section is missing. If called more than once, it could
      create duplicate widgets. This test ensures the assembly order is correct
      and complete.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if all five mocks were called exactly once with (window).
      Raises AssertionError if any mock was called zero times, multiple times,
      or with wrong arguments.

    ERRORS/EDGE CASES:
      - Sub-builder missing from source (e.g., build_presets_tab removed): mock assert_called_once fails.
      - Extra sub-builder call added: mock assert_called_once fails (called twice).
      - Wrong argument passed: mock assert_called_once_with fails.

    HOW TO TEST:
      1. Patch all five sub-builders with MagicMock.
      2. Call build_main_window_ui(window) where window is MagicMock().
      3. Assert each mock.assert_called_once_with(window).
      Realistic example: mock_hdr.assert_called_once_with(window) where window is a MagicMock representing MainWindow
    """
    mod = _import_module()
    window = MagicMock()
    with patch.object(mod, "QWidget") as MockW, \
         patch.object(mod, "QVBoxLayout") as MockL, \
         patch.object(mod, "build_header_bar") as mock_hdr, \
         patch.object(mod, "build_articles_tab") as mock_art, \
         patch.object(mod, "build_subscriptions_tab") as mock_sub, \
         patch.object(mod, "build_operations_tab") as mock_ops, \
         patch.object(mod, "build_presets_tab") as mock_pre:
        MockW.return_value = MagicMock()
        mock_layout = MagicMock()
        mock_layout.setSpacing = MagicMock()
        mock_layout.setContentsMargins = MagicMock()
        mock_layout.addWidget = MagicMock()
        MockL.return_value = mock_layout
        mod.build_main_window_ui(window)
        mock_hdr.assert_called_once_with(window)
        mock_art.assert_called_once_with(window)
        mock_sub.assert_called_once_with(window)
        mock_ops.assert_called_once_with(window)
        mock_pre.assert_called_once_with(window)


def test_creates_progress_bar():
    r"""Layer 2 — build_main_window_ui must create a hidden QProgressBar on window.progress.

    WHAT:
      Mocks QWidget, QVBoxLayout, and QProgressBar. Calls build_main_window_ui
      and verifies that:
        1. window.setCentralWidget was called once (with the central widget).
        2. The progress bar's setTextVisible was called with False.
        3. The progress bar's setVisible was called with False.

    WHY:
      The progress bar provides visual feedback during feed downloads but
      should be invisible when no download is in progress. If it is visible
      by default, the UI looks broken. If setCentralWidget is not called,
      the window has no root widget and Qt will crash.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if setCentralWidget, setTextVisible(False), and setVisible(False)
      are all called exactly once.
      Raises AssertionError if any call is missing or has wrong arguments.

    ERRORS/EDGE CASES:
      - Progress bar visible by default (setVisible(True)): test fails.
      - Progress bar text visible by default (setTextVisible(True)): test fails.
      - setCentralWidget not called: test fails.
      - Progress bar not stored on window.progress: test cannot verify.

    HOW TO TEST:
      1. Patch QProgressBar to return a MagicMock with setTextVisible and setVisible mocks.
      2. Call build_main_window_ui(window).
      3. Assert window.setCentralWidget called once, mock_bar.setTextVisible.called_once_with(False), mock_bar.setVisible.called_once_with(False).
      Realistic example: mock_bar.setTextVisible.assert_called_once_with(False)
    """
    mod = _import_module()
    window = MagicMock()
    with patch.object(mod, "QWidget") as MockW, \
         patch.object(mod, "QVBoxLayout") as MockL, \
         patch("gui._03_ui_assembly_orchestrator.build_main_window_ui.QProgressBar") as MockProgress:
        mock_central = MagicMock()
        MockW.return_value = mock_central
        mock_layout = MagicMock()
        mock_layout.setSpacing = MagicMock()
        mock_layout.setContentsMargins = MagicMock()
        mock_layout.addWidget = MagicMock()
        MockL.return_value = mock_layout
        mock_bar = MagicMock()
        mock_bar.setTextVisible = MagicMock()
        mock_bar.setVisible = MagicMock()
        MockProgress.return_value = mock_bar
        mod.build_main_window_ui(window)
        window.setCentralWidget.assert_called_once()
        mock_bar.setTextVisible.assert_called_once_with(False)
        mock_bar.setVisible.assert_called_once_with(False)


def test_creates_tabs_widget():
    r"""Layer 2 — build_main_window_ui must create a QTabWidget and store it on window.tabs.

    WHAT:
      Mocks QWidget, QVBoxLayout, and QTabWidget. Calls build_main_window_ui
      and verifies that QTabWidget was instantiated once and its return value
      was stored as window.tabs.

    WHY:
      window.tabs is the central container that all four tab builders add
      their pages to. If the QTabWidget is not created or not stored on the
      window, the tab builders will fail when they call window.tabs.addTab().

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if QTabWidget was called once and window.tabs equals the returned mock.
      Raises AssertionError if QTabWidget was not called or window.tabs is wrong.

    ERRORS/EDGE CASES:
      - QTabWidget constructor called with arguments: test only checks call count, not args.
      - window.tabs assigned a different object: assertion fails.
      - QTabWidget not instantiated at all: MockTabs.assert_called_once fails.

    HOW TO TEST:
      1. Patch QTabWidget to return a MagicMock.
      2. Call build_main_window_ui(window).
      3. Assert MockTabs.assert_called_once() and window.tabs is the mock_tabs object.
      Realistic example: mock_tabs = MagicMock(); MockTabs.return_value = mock_tabs; assert window.tabs is mock_tabs
    """
    mod = _import_module()
    window = MagicMock()
    with patch.object(mod, "QWidget") as MockW, \
         patch.object(mod, "QVBoxLayout") as MockL, \
         patch("gui._03_ui_assembly_orchestrator.build_main_window_ui.QTabWidget") as MockTabs:
        mock_central = MagicMock()
        MockW.return_value = mock_central
        mock_layout = MagicMock()
        mock_layout.setSpacing = MagicMock()
        mock_layout.setContentsMargins = MagicMock()
        mock_layout.addWidget = MagicMock()
        MockL.return_value = mock_layout
        mock_tabs = MagicMock()
        MockTabs.return_value = mock_tabs
        mod.build_main_window_ui(window)
        MockTabs.assert_called_once()
        assert window.tabs is mock_tabs
