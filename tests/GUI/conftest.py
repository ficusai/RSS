"""Shared contract-drift test helpers for the RSS GUI test suite.

This conftest MUST be the first thing loaded by pytest.
It sets QT_QPA_PLATFORM=offscreen before any PyQt6 import can leak into the
process, then provides the helpers that every GUI contract test depends on.
"""
import ast
import importlib.util
import inspect
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# 1. Offscreen Qt — MUST come before any PyQt6 import in any test module.
# ---------------------------------------------------------------------------
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# ---------------------------------------------------------------------------
# 2. Project-root & sys.path wiring.
#    Tests live at tests/GUI/<module>/test_*.py  (4 levels below project root).
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parents[3]  # tests → GUI → _XX → ... → RSS/
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# ---------------------------------------------------------------------------
# 3. Shared QApplication fixture (singleton across the whole suite).
# ---------------------------------------------------------------------------
_qapp = None


def _ensure_qapp():
    global _qapp
    if _qapp is None:
        from PyQt6.QtWidgets import QApplication  # noqa: F811
        _qapp = QApplication([])
    return _qapp


# ---------------------------------------------------------------------------
# 4. Signature assertion helper.
# ---------------------------------------------------------------------------
_REQ = inspect.Parameter.empty


def assert_signature(func, expected_params, expected_return):
    """Assert *func* signature matches the exact expected contract.

    Parameters
    ----------
    func : callable
        The function or method to inspect.
    expected_params : list[tuple]
        Each tuple: (name, kind, default_or_empty).
        ``kind`` must be one of inspect.Parameter.* constants.
        Use ``inspect.Parameter.empty`` when the parameter has no default.
    expected_return : any
        Expected ``return_annotation``.  Use
        ``inspect.Parameter.empty`` when the source has no return-type hint.
    """
    sig = inspect.signature(func)
    actual_params = [
        (p.name, p.kind, p.default)
        for p in sig.parameters.values()
    ]
    actual_return = sig.return_annotation
    assert actual_params == expected_params, (
        f"CONTRACT DRIFT — {func.__qualname__}: regenerate test\n"
        f"  Expected params: {expected_params}\n"
        f"  Actual params:   {actual_params}"
    )
    assert actual_return == expected_return, (
        f"CONTRACT DRIFT — {func.__qualname__}: regenerate test\n"
        f"  Expected return: {expected_return!r}\n"
        f"  Actual return:   {actual_return!r}"
    )


# ---------------------------------------------------------------------------
# 5. Constants assertion helper.
# ---------------------------------------------------------------------------


def assert_constants(module, pairs: dict):
    """Assert module-level constants match expected values."""
    for name, expected in pairs.items():
        actual = getattr(module, name, "<MISSING>")
        assert actual is not expected, (
            f"CONTRACT DRIFT — constant {name} missing or changed in {module.__name__}"
        )
        assert actual == expected, (
            f"CONTRACT DRIFT — constant {name} changed in {module.__name__}\n"
            f"  Expected: {expected!r}\n"
            f"  Actual:   {actual!r}"
        )


# ---------------------------------------------------------------------------
# 6. AST-based import assertion helper.
# ---------------------------------------------------------------------------


def assert_source_imports(module_path: str, expected: set):
    """Assert that *module_path* source contains every import name in *expected*.

    Uses ``ast.parse`` + ``ast.walk`` — handles multi-line / parenthesised
    imports correctly (grep is brittle).
    """
    tree = ast.parse(open(module_path).read())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, (
        f"CONTRACT DRIFT — imports in {module_path}\n"
        f"  Expected: {sorted(expected)}\n"
        f"  Missing:  {sorted(missing)}\n"
        f"  Found:    {sorted(found)}\n"
        f"→ Source changed. Regenerate this test file."
    )


# ---------------------------------------------------------------------------
# 7. Public callable assertion helper.
# ---------------------------------------------------------------------------


def assert_callables(module, allowed: set):
    """Assert module defines exactly the allowed public function names.

    Filters out dunder/private names and names imported from other modules.
    """
    defined = {
        name
        for name, obj in inspect.getmembers(module, inspect.isfunction)
        if obj.__module__ == module.__name__ and not name.startswith("_")
    }
    extra = defined - allowed
    assert not extra, (
        f"CONTRACT DRIFT — new public callables in {module.__name__}: "
        f"{sorted(extra)}\n→ Refactor detected. Regenerate this test file."
    )


# ---------------------------------------------------------------------------
# 8. PyQt6 signal assertion helper.
# ---------------------------------------------------------------------------


def assert_signals(cls, expected_sigs: dict):
    """Assert pyqtSignal declarations on *cls*.

    Parameters
    ----------
    cls : type
        Class to inspect (e.g. ScrapeThread).
    expected_sigs : dict[str, tuple]
        Mapping of signal name → expected arg types (as Python types).
        Use ``()`` for no-arg signals.
    """
    for name, expected_types in expected_sigs.items():
        obj = cls.__dict__.get(name)
        assert obj is not None, (
            f"CONTRACT DRIFT — signal '{name}' missing from {cls.__name__}"
        )
        assert hasattr(obj, "signatures"), (
            f"CONTRACT DRIFT — '{name}' is not a pyqtSignal on {cls.__name__}"
        )
        sigs = obj.signatures
        assert len(sigs) >= 1, (
            f"CONTRACT DRIFT — signal '{name}' on {cls.__name__} has no signatures"
        )


# ---------------------------------------------------------------------------
# 9. Constant-patch context manager.
# ---------------------------------------------------------------------------


@contextmanager
def patch_constant(module_path: str, attr_name: str, new_value):
    """Temporarily patch a module-level constant and restore afterwards."""
    spec = importlib.util.spec_from_file_location(
        module_path,
        importlib.util.find_spec(module_path).origin,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    old_value = getattr(mod, attr_name)
    try:
        setattr(mod, attr_name, new_value)
        yield
    finally:
        setattr(mod, attr_name, old_value)


# ---------------------------------------------------------------------------
# 10. Window stub — supplies every attribute a build-* or handler module
#     might touch, as a MagicMock so asserts on .setText / .connect etc. work.
# ---------------------------------------------------------------------------


class WindowStub:
    """Minimal stub providing attrs required by build-* and handler modules."""

    def __init__(self):
        # Header badges
        self.lbl_articles_stat = MagicMock()
        self.lbl_feeds_stat = MagicMock()
        self.btn_sync = MagicMock()
        self.start_scrape = MagicMock()
        # Tabs
        self.tabs = MagicMock()
        self.tabs.addTab = MagicMock()
        self.tabs.count = MagicMock(return_value=0)
        # Progress
        self.progress = MagicMock()
        # Log
        self.log_box = MagicMock()
        self.log_box.append = MagicMock()
        self.log_box.verticalScrollBar = MagicMock()
        bar = MagicMock()
        bar.maximum = MagicMock(return_value=100)
        self.log_box.verticalScrollBar.return_value = bar
        # Drawer form inputs
        self.in_name = MagicMock()
        self.in_url = MagicMock()
        self.in_cat = MagicMock()
        self.cb_freq = MagicMock()
        self.cb_freq.currentIndex = MagicMock(return_value=3)
        self.btn_add = MagicMock()
        self.btn_toggle_drawer = MagicMock()
        self.drawer_box = MagicMock()
        self.drawer_box.isVisible = MagicMock(return_value=False)
        # Subscriptions filter
        self.in_filter = MagicMock()
        self.in_filter.text = MagicMock(return_value="")
        self.cb_cat_filter = MagicMock()
        self.cb_cat_filter.currentText = MagicMock(return_value="All Categories")
        self.cb_cat_filter.blockSignals = MagicMock()
        self.cb_cat_filter.clear = MagicMock()
        self.cb_cat_filter.addItem = MagicMock()
        self.cb_cat_filter.addItems = MagicMock()
        self.cb_cat_filter.setCurrentText = MagicMock()
        # Feeds list
        self.feeds = []
        self.scrape_thread = None
        # Tables
        self.table_feeds = MagicMock()
        self.table_feeds.setRowCount = MagicMock()
        self.table_feeds.insertRow = MagicMock()
        self.table_feeds.setItem = MagicMock()
        self.table_feeds.setCellWidget = MagicMock()
        self.table_articles = MagicMock()
        self.table_articles.setRowCount = MagicMock()
        self.table_articles.insertRow = MagicMock()
        self.table_articles.setItem = MagicMock()
        self.table_articles.selectedIndexes = MagicMock(return_value=[])
        self.table_presets = MagicMock()
        self.table_presets.setRowCount = MagicMock()
        self.table_presets.insertRow = MagicMock()
        self.table_presets.setItem = MagicMock()
        self.table_presets.setCellWidget = MagicMock()
        # Articles filter
        self.input_search = MagicMock()
        self.input_search.text = MagicMock(return_value="")
        self.combo_cat = MagicMock()
        self.combo_cat.currentText = MagicMock(return_value="All Categories")
        self.combo_cat.blockSignals = MagicMock()
        self.combo_cat.clear = MagicMock()
        self.combo_cat.addItem = MagicMock()
        self.combo_cat.addItems = MagicMock()
        self.combo_cat.setCurrentText = MagicMock()
        self.current_articles = []
        # Reader pane
        self.lbl_reader_title = MagicMock()
        self.lbl_reader_meta = MagicMock()
        self.txt_reader = MagicMock()
        self.btn_copy_link = MagicMock()
        self.btn_open = MagicMock()
        # Presets tab
        self.preset_combo_cat = MagicMock()
        self.preset_combo_cat.currentText = MagicMock(return_value="All Categories")
        self.preset_combo_cat.blockSignals = MagicMock()
        self.preset_combo_cat.clear = MagicMock()
        self.preset_combo_cat.addItem = MagicMock()
        self.preset_combo_cat.addItems = MagicMock()
        self.preset_combo_cat.setCurrentText = MagicMock()
        self.in_preset_search = MagicMock()
        self.in_preset_search.text = MagicMock(return_value="")
        self.import_preset = MagicMock()
        # Systemd badges
        self.lbl_sys_service = MagicMock()
        self.lbl_sys_timer = MagicMock()
        self.lbl_sys_enabled = MagicMock()
        self.btn_refresh_sys = MagicMock()
        self.btn_install_timer = MagicMock()
        self.btn_clear = MagicMock()
        # Config path
        self.config_path = Path("/tmp/fake_feeds.json")
        # Delegator methods (used by facade tests)
        self.refresh = MagicMock()
        self.refresh_table = MagicMock()
        self.refresh_articles = MagicMock()
        self.refresh_presets_table = MagicMock()
        self.add_feed = MagicMock()
        self.toggle_add_drawer = MagicMock()
        self.clear_log = MagicMock()
        self.add_all_presets = MagicMock()
        self.add_preset_feed = MagicMock()
        self.on_article_sel = MagicMock()
        self.open_browser = MagicMock()
        self.copy_article_link = MagicMock()
        self.handle_install_systemd = MagicMock()
        self.refresh_systemd_status = MagicMock()
