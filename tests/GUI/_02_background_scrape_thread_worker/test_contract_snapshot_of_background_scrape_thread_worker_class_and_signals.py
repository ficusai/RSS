"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_02_background_scrape_thread_worker/scrape_thread_worker.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.
"""
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_02_background_scrape_thread_worker" / "scrape_thread_worker.py"


def _import_module():
    import gui._02_background_scrape_thread_worker.scrape_thread_worker as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence."""
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health."""
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports."""
    expected = {"copy", "PyQt6.QtCore", "core.fetcher.fetch_all_feeds", "core.storage.save_articles"}
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


def test_scrape_thread_class_exists():
    """Layer 1 — ScrapeThread(QThread) class exists."""
    mod = _import_module()
    assert hasattr(mod, "ScrapeThread")
    cls = mod.ScrapeThread
    assert inspect.isclass(cls)
    from PyQt6.QtCore import QThread
    assert issubclass(cls, QThread)


def test_log_signal_signature():
    """Layer 1 — log_signal = pyqtSignal(str)."""
    mod = _import_module()
    cls = mod.ScrapeThread
    obj = cls.__dict__.get("log_signal")
    assert obj is not None
    assert hasattr(obj, "signatures")
    sigs = obj.signatures
    assert len(sigs) >= 1
    # First param should be str
    assert str(sigs[0][0]) == "<class 'str'>", f"Expected str signal, got {sigs[0]}"


def test_finished_signal_signature():
    """Layer 1 — finished_signal = pyqtSignal(int, int, list)."""
    mod = _import_module()
    cls = mod.ScrapeThread
    obj = cls.__dict__.get("finished_signal")
    assert obj is not None
    assert hasattr(obj, "signatures")
    sigs = obj.signatures
    assert len(sigs) >= 1
    assert str(sigs[0][0]) == "<class 'int'>"
    assert str(sigs[0][1]) == "<class 'int'>"
    assert str(sigs[0][2]) == "<class 'list'>"


def test_init_signature():
    """Layer 1 — __init__(self, feeds, parent=None) exact."""
    mod = _import_module()
    func = mod.ScrapeThread.__init__
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [
        ("self", inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.empty),
        ("feeds", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ("parent", inspect.Parameter.POSITIONAL_OR_KEYWORD, None),
    ]
    assert params == expected, f"Expected {expected}, got {params}"


def test_run_signature_no_annotation():
    """Layer 1 — run(self) -> None (no annotation in source)."""
    mod = _import_module()
    func = mod.ScrapeThread.run
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    assert params == [("self", inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.empty)]
    assert sig.return_annotation is inspect.Parameter.empty


def test_deep_copy_isolation():
    """Layer 2 — mutating original feeds after construction does not affect thread.feeds."""
    mod = _import_module()
    original = [{"name": "CNN", "url": "http://cnn.com"}, {"name": "BBC", "url": "http://bbc.com"}]
    thread = mod.ScrapeThread(original)
    original.append({"name": "NEW", "url": "http://new.com"})
    original[0]["name"] = "MODIFIED"
    assert len(thread.feeds) == 2, "thread.feeds should not grow"
    assert thread.feeds[0]["name"] == "CNN", "thread.feeds should be deep-copied"
    assert thread.feeds[1]["name"] == "BBC"


def test_run_emits_finished_success():
    """Layer 2 — run emits finished_signal with correct args on success."""
    mod = _import_module()
    with patch("gui._02_background_scrape_thread_worker.scrape_thread_worker.fetch_all_feeds") as mock_fetch, \
         patch("gui._02_background_scrape_thread_worker.scrape_thread_worker.save_articles") as mock_save:
        mock_fetch.return_value = ([{"title": "test"}], [])
        mock_save.return_value = (1, 10)
        thread = mod.ScrapeThread([])
        results = []
        thread.finished_signal.connect(lambda n, t, e: results.append((n, t, e)))
        thread.run()
        assert results == [(1, 10, [])], f"Expected [(1, 10, [])], got {results}"


def test_run_emits_error_on_exception():
    """Layer 2 — run catches exceptions and emits error result."""
    mod = _import_module()
    with patch("gui._02_background_scrape_thread_worker.scrape_thread_worker.fetch_all_feeds") as mock_fetch:
        mock_fetch.side_effect = RuntimeError("fail")
        thread = mod.ScrapeThread([])
        results = []
        thread.finished_signal.connect(lambda n, t, e: results.append((n, t, e)))
        thread.run()
        assert len(results) == 1
        n, t, e = results[0]
        assert n == 0 and t == 0
        assert len(e) == 1
        assert e[0]["feed_name"] == "System"
        assert e[0]["error"] == "fail"
