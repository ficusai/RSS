"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_07_ui_operations_system_tab_build/build_operations_tab.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.
"""
# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# This test file verifies the contract of gui._07_ui_operations_system_tab_build
# build_operations_tab. It checks that the source module file exists, imports
# correctly, has the expected AST-import set, that build_operations_tab has the
# correct signature, and that calling it with a MagicMock window produces the
# expected Qt widget hierarchy: three status-badge QLabels (service/timer/enabled),
# a read-only QTextEdit log console (objectName=log_console), three QPushButton
# click-connections (clear_log, refresh_systemd_status, handle_install_systemd),
# and the correct tab label "⚙️ Operations & System".
# ==============================================================================
# ==============================================================================
# LAYER BREAKDOWN
#   Layer 1 — Module-level contract checks:
#     * test_file_exists: source .py file is present on disk.
#     * test_import_health: the module can be imported without error.
#     * test_ast_imports: the expected PyQt6.QtWidgets import is present via AST.
#     * test_build_operations_tab_signature: func(window) -> None signature.
#   Layer 2 — Behavioural contract checks (mocked Qt):
#     * test_lbl_sys_service_created: lbl_sys_service QLabel instantiated.
#     * test_lbl_sys_timer_created: lbl_sys_timer QLabel instantiated.
#     * test_lbl_sys_enabled_created: lbl_sys_enabled QLabel instantiated.
#     * test_log_box_is_qtextedit: log_box is QTextEdit, objectName=log_console, readOnly=True.
#     * test_btn_clear_connected: btn_clear.clicked.connect(window.clear_log).
#     * test_btn_refresh_sys_connected: btn_refresh_sys.clicked.connect(window.refresh_systemd_status).
#     * test_btn_install_timer_connected: btn_install_timer.clicked.connect(window.handle_install_systemd).
#     * test_tab_label: tab label is "⚙️ Operations & System".
# ==============================================================================
# ==============================================================================
# LAYER WHAT EACH TEST CHECKS
#   Layer 1 tests verify the module's structural contract (file presence, import
#   health, static import set, function signature).
#   Layer 2 tests verify the runtime widget-creation contract by mocking Qt
#   classes and asserting on constructor calls, attribute assignments, signal
#   connections, and tab-label text.
# ==============================================================================
# OVERVIEW OF IMPORTS
# import ast: abstract syntax tree parser; used to verify source-module imports statically.
# import inspect: runtime introspection; used to inspect function signatures.
# import sys: Python runtime; used to prepend the repo root to sys.path.
# import Path from pathlib: filesystem path builder; used to resolve the source-module file path.
# import MagicMock, patch from unittest.mock: test doubles; used to replace Qt widgets and module functions during Layer 2 tests.
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    r"""Return the absolute Path to the source module under test.

    WHAT: Builds the filesystem path to the source .py file.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: A pathlib.Path pointing to gui/_07_ui_operations_system_tab_build/build_operations_tab.py.
    EFFECT: None (pure function).
    ERRORS/EDGE CASES: Should never fail; returns a Path even if the file does not exist.
    EDGE CASES: None.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_07_ui_operations_system_tab_build" / "build_operations_tab.py"


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
    import gui._07_ui_operations_system_tab_build.build_operations_tab as mod
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

    WHAT: Verifies the expected PyQt6.QtWidgets import is present in the source AST.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if any expected import is missing.
    ERRORS/EDGE CASES: SyntaxError if source file has invalid Python.
    EDGE CASES: None.
    HOW TO TEST: Parse the source AST and walk for Import/ImportFrom nodes.
    """
    expected = {"PyQt6.QtWidgets"}
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


def test_build_operations_tab_signature():
    r"""Layer 1 — build_operations_tab(window) -> None.

    WHAT: Verifies the exact function signature of build_operations_tab.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Raises AssertionError if signature differs.
    ERRORS/EDGE CASES: AttributeError if the function does not exist on the module.
    EDGE CASES: None.
    HOW TO TEST: Use inspect.signature and compare parameters + return annotation.
    """
    mod = _import_module()
    func = mod.build_operations_tab
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_lbl_sys_service_created():
    r"""Layer 2 — lbl_sys_service created.

    WHAT: Verifies that build_operations_tab creates a QLabel for the systemd
          service status badge (window.lbl_sys_service).
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Mock QLabel constructor is called once.
    ERRORS/EDGE CASES: AssertionError if QLabel is not called.
    EDGE CASES: None.
    HOW TO TEST: Patch QLabel; call build_operations_tab; assert QLabel was called.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)


def test_lbl_sys_timer_created():
    r"""Layer 2 — lbl_sys_timer created.

    WHAT: Verifies that build_operations_tab creates a QLabel for the systemd
          timer status badge (window.lbl_sys_timer).
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Mock QLabel constructor is called once.
    ERRORS/EDGE CASES: AssertionError if QLabel is not called.
    EDGE CASES: None.
    HOW TO TEST: Patch QLabel; call build_operations_tab; assert QLabel was called.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)


def test_lbl_sys_enabled_created():
    r"""Layer 2 — lbl_sys_enabled created.

    WHAT: Verifies that build_operations_tab creates a QLabel for the systemd
          enabled/autostart status badge (window.lbl_sys_enabled).
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: Mock QLabel constructor is called once.
    ERRORS/EDGE CASES: AssertionError if QLabel is not called.
    EDGE CASES: None.
    HOW TO TEST: Patch QLabel; call build_operations_tab; assert QLabel was called.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)


def test_log_box_is_qtextedit():
    r"""Layer 2 — log_box QTextEdit (objectName log_console).

    WHAT: Verifies that build_operations_tab creates a QTextEdit for the log
          console, stores it as window.log_box, sets its objectName to
          'log_console', and makes it read-only.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if objectName or readOnly is wrong.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QTextEdit; call build_operations_tab; assert window.log_box
                 is the returned mock, assert setObjectName('log_console'),
                 assert setReadOnly(True).
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        mock_text = MagicMock()
        mock_text.setObjectName = MagicMock()
        mock_text.setReadOnly = MagicMock()
        MockText.return_value = mock_text
        mod.build_operations_tab(window)
        assert window.log_box is mock_text
        mock_text.setObjectName.assert_called_once_with("log_console")
        mock_text.setReadOnly.assert_called_once_with(True)


def test_btn_clear_connected():
    r"""Layer 2 — btn_clear connected to window.clear_log.

    WHAT: Verifies that build_operations_tab creates a 'Clear Log' QPushButton
          and connects its clicked signal to window.clear_log.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if clicked.connect was not called with window.clear_log.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QPushButton; provide a mock clicked.connect; call the
                 function; assert clicked.connect was called once with window.clear_log.
    """
    mod = _import_module()
    window = MagicMock()
    window.clear_log = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        mock_btn.clicked.connect.assert_called_once_with(window.clear_log)


def test_btn_refresh_sys_connected():
    r"""Layer 2 — btn_refresh_sys connected to window.refresh_systemd_status.

    WHAT: Verifies that build_operations_tab creates a 'Refresh Status' QPushButton
          and connects its clicked signal to window.refresh_systemd_status.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if clicked.connect was not called with the correct handler.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QPushButton; provide a mock clicked.connect; call the
                 function; assert clicked.connect.call_args_list contains
                 window.refresh_systemd_status.
    """
    mod = _import_module()
    window = MagicMock()
    window.refresh_systemd_status = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        # First button is btn_refresh_sys
        calls = mock_btn.clicked.connect.call_args_list
        assert window.refresh_systemd_status in [c[0][0] for c in calls]


def test_btn_install_timer_connected():
    r"""Layer 2 — btn_install_timer connected to window.handle_install_systemd.

    WHAT: Verifies that build_operations_tab creates an 'Install / Enable 12-Hour
          Systemd Timer' QPushButton and connects its clicked signal to
          window.handle_install_systemd.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if clicked.connect was not called with the correct handler.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QPushButton; provide a mock clicked.connect; call the
                 function; assert clicked.connect.call_args_list contains
                 window.handle_install_systemd.
    """
    mod = _import_module()
    window = MagicMock()
    window.handle_install_systemd = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        calls = mock_btn.clicked.connect.call_args_list
        assert window.handle_install_systemd in [c[0][0] for c in calls]


def test_tab_label():
    r"""Layer 2 — Tab label '⚙️ Operations & System'.

    WHAT: Verifies that build_operations_tab registers itself as Tab 3 with the
          exact label '⚙️ Operations & System'.
    OPTIONS: None.
    DEFAULTS: N/A.
    OUTPUT: None (assertion-based).
    EFFECT: AssertionError if the tab label string does not match exactly.
    ERRORS/EDGE CASES: None.
    EDGE CASES: None.
    HOW TO TEST: Patch QLabel/QPushButton/QFrame/QTextEdit; provide window.tabs
                 as MagicMock; call build_operations_tab; assert
                 window.tabs.addTab was called once with the correct label.
    """
    mod = _import_module()
    window = MagicMock()
    window.tabs = MagicMock()
    with patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QLabel") as MockLabel, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QPushButton") as MockButton, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QFrame") as MockFrame, \
         patch("gui._07_ui_operations_system_tab_build.build_operations_tab.QTextEdit") as MockText:
        MockLabel.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        MockFrame.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_operations_tab(window)
        window.tabs.addTab.assert_called_once()
        call_args = window.tabs.addTab.call_args
        assert call_args[0][1] == "⚙️ Operations & System"
