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

# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# ==============================================================================
# This test file verifies the contract of the ScrapeThread class, which is a
# background worker that downloads RSS/Atom feeds without freezing the GUI.
# ScrapeThread inherits from PyQt6's QThread and runs feed downloads in a
# separate OS thread, emitting progress messages and final results back to
# the main window via PyQt6 signals. It deep-copies the feeds list on init
# so that changes made by the user during a download do not corrupt the job.
# ==============================================================================

# ==============================================================================
# LAYER BREAKDOWN
# ==============================================================================
# Layer 1 (Structural):
#   - test_file_exists : verifies the source .py file exists on disk
#   - test_import_health : verifies the module can be imported without errors
#   - test_ast_imports : AST-parses the source to verify all expected imports are present
#   - test_scrape_thread_class_exists : verifies ScrapeThread class exists and subclasses QThread
#   - test_log_signal_signature : verifies log_signal is a pyqtSignal(str)
#   - test_finished_signal_signature : verifies finished_signal is a pyqtSignal(int, int, list)
#   - test_init_signature : verifies __init__(self, feeds, parent=None) exact signature
#   - test_run_signature_no_annotation : verifies run(self) has no return type annotation
#
# Layer 2 (Behavioral):
#   - test_deep_copy_isolation : verifies mutations to the original feeds list do not affect thread.feeds
#   - test_run_emits_finished_success : verifies run() emits finished_signal(new, total, []) on success
#   - test_run_emits_error_on_exception : verifies run() catches exceptions and emits an error result
# ==============================================================================

# ==============================================================================
# LAYER WHAT EACH TEST CHECKS
# ==============================================================================
# Layer 1 tests confirm the structural contract: the module file is present,
# imports are correct, the class exists with the right base class, signals have
# the right types, and method signatures match exactly. These catch regressions
# where a developer renames a class, drops an import, or changes a signal type.
#
# Layer 2 tests confirm behavioral contract: the deep-copy isolation prevents
# race conditions, successful runs emit the correct success tuple, and any
# exception during the run is caught and reported as a structured error dict.
# These catch logic drift where the behavior changes even if signatures stay the same.
# ==============================================================================


# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# import ast: parses Python source code into an Abstract Syntax Tree (AST) so we can inspect imports without executing the module.
# import inspect: inspects function and class signatures at runtime — used to verify parameter names, kinds, defaults, and return annotations.
# import sys: manipulates the Python module search path (sys.path) so tests can import gui modules from the project root.
# from pathlib import Path: provides object-oriented filesystem path manipulation to locate the source module relative to this test file.
# from unittest.mock import MagicMock, patch: creates fake objects (MagicMock) and temporarily replaces real functions (patch) to isolate the unit under test.
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    r"""Return the absolute Path to the source module being tested.

    WHAT:
      Constructs and returns the filesystem path to scrape_thread_worker.py,
      the source module whose contract this test file verifies.

    OPTIONS:
      None. This function takes no arguments.

    DEFAULTS:
      None.

    OUTPUT:
      A pathlib.Path object pointing to:
        <project_root>/gui/_02_background_scrape_thread_worker/scrape_thread_worker.py

    EFFECT:
      No side effects. Pure function.

    ERRORS/EDGE CASES:
      None expected. Path resolution is deterministic given a fixed filesystem layout.

    HOW TO TEST:
      1. Run this test file.
      2. Assert the returned path exists with .exists().
      Example: p = _module_path(); assert p.exists()
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_02_background_scrape_thread_worker" / "scrape_thread_worker.py"


def _import_module():
    r"""Import and return the source module under test.

    WHAT:
      Dynamically imports gui._02_background_scrape_thread_worker.scrape_thread_worker
      and returns the module object so tests can access classes and functions.

    OPTIONS:
      None. This function takes no arguments.

    DEFAULTS:
      None.

    OUTPUT:
      The imported module object (sys.modules entry for gui._02_background_scrape_thread_worker.scrape_thread_worker).

    EFFECT:
      The module is loaded into sys.modules. Any module-level side effects
      (e.g., import-time network calls) will execute.

    ERRORS/EDGE CASES:
      - If the source module has a syntax error, ImportError or SyntaxError is raised.
      - If the module is already cached in sys.modules, the cached version is returned.
      - If PYTHONPATH or sys.path does not include the project root, ImportError is raised.

    HOW TO TEST:
      1. Call mod = _import_module().
      2. Assert mod is not None.
      3. Access mod.ScrapeThread to verify the class is available.
      Example: mod = _import_module(); assert hasattr(mod, 'ScrapeThread')
    """
    import gui._02_background_scrape_thread_worker.scrape_thread_worker as mod
    return mod


def test_file_exists():
    r"""Layer 1 — Source file must exist on disk.

    WHAT:
      Verifies that the source module file scrape_thread_worker.py is present
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
      1. Confirm the file exists at gui/_02_background_scrape_thread_worker/scrape_thread_worker.py.
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
      following four imports are present: copy, PyQt6.QtCore, core.fetcher,
      and core.storage. Missing any of these would cause runtime failures.

    WHY:
      Dynamic imports (importlib) could miss renamed or removed imports.
      AST parsing statically inspects the source text, catching import
      drift even before the module is executed.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if all four expected import modules are found in the AST.
      Raises AssertionError listing the missing import names.

    ERRORS/EDGE CASES:
      - Import renamed (e.g., PyQt6.QtCore -> PyQt5.QtCore): assertion fails with missing import listed.
      - Import dropped entirely: assertion fails.
      - Import aliased (as X): still detected because AST checks node.module, not alias.name.

    HOW TO TEST:
      1. Remove one expected import from the source — test should fail listing the missing name.
      2. Add an extra unexpected import — test should still pass (only checks for expected set).
      3. Restore the source — test should pass again.
    """
    expected = {"copy", "PyQt6.QtCore", "core.fetcher", "core.storage"}
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
    r"""Layer 1 — ScrapeThread must be a class that subclasses QThread.

    WHAT:
      Verifies that the imported module exposes a ScrapeThread attribute,
      that it is a class (not a function or instance), and that it inherits
      from PyQt6.QtCore.QThread.

    WHY:
      ScrapeThread's inheritance from QThread is fundamental to its purpose:
      running feed downloads in a background OS thread. If someone replaced
      the class with a regular function or changed the base class, the
      entire threading model would break.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if ScrapeThread exists, is a class, and is a subclass of QThread.
      Raises AssertionError if any condition fails.

    ERRORS/EDGE CASES:
      - Class renamed (e.g., ScrapeThread -> FeedWorker): hasattr returns False.
      - Base class changed (e.g., QThread -> object): issubclass fails.
      - Attribute is a function instead of class: inspect.isclass returns False.

    HOW TO TEST:
      1. Rename ScrapeThread in the source to something else — test should fail.
      2. Change the base class from QThread to object — test should fail.
      3. Restore both — test should pass again.
    """
    mod = _import_module()
    assert hasattr(mod, "ScrapeThread")
    cls = mod.ScrapeThread
    assert inspect.isclass(cls)
    from PyQt6.QtCore import QThread
    assert issubclass(cls, QThread)


def test_log_signal_signature():
    r"""Layer 1 — log_signal must be a pyqtSignal accepting a single str argument.

    WHAT:
      Verifies that ScrapeThread defines a class attribute named log_signal
      which is a PyQt6 signal object with at least one signature variant
      that includes "QString" (PyQt6's internal name for the str signal type).

    WHY:
      The log_signal is how the background thread sends progress messages
      back to the GUI thread. If the signal type changes (e.g., to int or
      disappears entirely), the GUI will stop receiving progress updates.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if log_signal exists on the class, has signatures, and the
      first signature contains "QString".
      Raises AssertionError otherwise.

    ERRORS/EDGE CASES:
      - Signal renamed (e.g., log_signal -> progress_signal): getattr returns None.
      - Signal type changed to int: "QString" not found in signatures.
      - Signal removed entirely: obj is None, assertion fails.

    HOW TO TEST:
      1. Rename log_signal in the source — test should fail with obj is None.
      2. Change pyqtSignal(str) to pyqtSignal(int) — test should fail ("QString" not in signature).
      3. Restore — test should pass again.
    """
    mod = _import_module()
    cls = mod.ScrapeThread
    obj = cls.__dict__.get("log_signal")
    assert obj is not None
    assert hasattr(obj, "signatures")
    sigs = obj.signatures
    assert len(sigs) >= 1
    # First param should be QString (PyQt6's string type alias for str)
    assert "QString" in sigs[0], f"Expected str signal (QString), got {sigs[0]}"


def test_finished_signal_signature():
    r"""Layer 1 — finished_signal must be a pyqtSignal(int, int, list).

    WHAT:
      Verifies that ScrapeThread defines a class attribute named finished_signal
      which is a PyQt6 signal object whose first signature contains both
      "int" and "QVariantList" (PyQt6's encoding for list arguments in signals).

    WHY:
      The finished_signal carries the scrape results back to the main window.
      Its three parameters — new article count, total count, and error list —
      are consumed by the GUI's on_done handler. A wrong signature would
      cause signal-slot connection failures at runtime.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if finished_signal exists, has signatures, and the first signature
      contains both "int" and "QVariantList".
      Raises AssertionError otherwise.

    ERRORS/EDGE CASES:
      - Signal renamed: getattr returns None.
      - Signal type changed to pyqtSignal(str): "int" not found.
      - Extra parameter added (e.g., pyqtSignal(int, int, list, str)): test may still pass if first sig still contains int and QVariantList.

    HOW TO TEST:
      1. Change pyqtSignal(int, int, list) to pyqtSignal(str) in source — test should fail.
      2. Remove the signal entirely — test should fail with obj is None.
      3. Restore — test should pass again.
    """
    mod = _import_module()
    cls = mod.ScrapeThread
    obj = cls.__dict__.get("finished_signal")
    assert obj is not None
    assert hasattr(obj, "signatures")
    sigs = obj.signatures
    assert len(sigs) >= 1
    # PyQt6 encodes int as 'i' and list as 'QVariantList' in signal signatures
    assert "int" in sigs[0]
    assert "QVariantList" in sigs[0]


def test_init_signature():
    r"""Layer 1 — __init__ must accept (self, feeds, parent=None) exactly.

    WHAT:
      Verifies that ScrapeThread.__init__ has exactly three parameters:
      self (positional-or-keyword, no default), feeds (positional-or-keyword,
      no default), and parent (positional-or-keyword, default None).

    WHY:
      The constructor signature is part of the public contract. External code
      (the main window) creates ScrapeThread instances with specific arguments.
      Changing parameter names, order, or defaults would break callers.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if the signature matches exactly.
      Raises AssertionError with expected vs. actual parameter list.

    ERRORS/EDGE CASES:
      - Parameter reordered (e.g., parent before feeds): assertion fails.
      - Default changed (e.g., parent=None -> parent="default"): assertion fails.
      - Extra parameter added: assertion fails (length mismatch).
      - Missing parameter: assertion fails (length mismatch).

    HOW TO TEST:
      1. Add a new parameter to __init__ — test should fail.
      2. Change parent's default from None to "" — test should fail.
      3. Restore — test should pass again.
    """
    mod = _import_module()
    func = mod.ScrapeThread.__init__
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [
        ("self", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ("feeds", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ("parent", inspect.Parameter.POSITIONAL_OR_KEYWORD, None),
    ]
    assert params == expected, f"Expected {expected}, got {params}"


def test_run_signature_no_annotation():
    r"""Layer 1 — run(self) must have no return type annotation in source.

    WHAT:
      Verifies that ScrapeThread.run has exactly one parameter (self) and
      that its return annotation is unset (inspect.Parameter.empty), meaning
      the source code does not include a -> None or any other annotation.

    WHY:
      PyQt6's QThread.run() is conventionally untyped in source. Adding a
      return annotation could interfere with PyQt6's signal/slot introspection
      or confuse static analysis tools that expect the standard QThread pattern.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if run has one parameter (self) and no return annotation.
      Raises AssertionError if annotation is present or parameters differ.

    ERRORS/EDGE CASES:
      - Return annotation added (-> None): sig.return_annotation is None, not empty.
      - Extra parameter added: parameter count mismatch.
      - Parameter renamed: name mismatch.

    HOW TO TEST:
      1. Add "-> None" to the run method signature in source — test should fail.
      2. Add an extra parameter to run — test should fail.
      3. Restore — test should pass again.
    """
    mod = _import_module()
    func = mod.ScrapeThread.run
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    assert params == [("self", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert sig.return_annotation is inspect.Parameter.empty


def test_deep_copy_isolation():
    r"""Layer 2 — Mutating the original feeds list after construction must not affect thread.feeds.

    WHAT:
      Creates a ScrapeThread with a list of feed dicts, then mutates the
      original list (append and in-place dict modification). Verifies that
      thread.feeds remains unchanged, proving that __init__ performs a
      deep copy.

    WHY:
      Without deep-copy isolation, the background thread and the main GUI
      thread would share the same list and dict objects. If the user adds
      or edits a feed in the GUI while a scrape is running, the thread
      could see inconsistent data, miss feeds, or crash.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if thread.feeds has length 2 and the first two entries retain
      their original names ("CNN" and "BBC") despite mutations to original.
      Raises AssertionError if any mutation leaked into thread.feeds.

    ERRORS/EDGE CASES:
      - shallow copy used instead of deepcopy: mutating original[0]["name"] leaks into thread.feeds[0].
      - No copy at all: all mutations leak.
      - Empty feeds list passed: thread.feeds should be [] (no mutations to apply).

    HOW TO TEST:
      1. Create thread = ScrapeThread([{"name":"CNN","url":"http://cnn.com"}, {"name":"BBC","url":"http://bbc.com"}]).
      2. Append a new dict to the original list and change original[0]["name"] to "MODIFIED".
      3. Assert thread.feeds[0]["name"] == "CNN" and len(thread.feeds) == 2.
      Realistic example: feeds = [{"name":"CNN","url":"http://cnn.com"}]; thread = ScrapeThread(feeds); feeds.append({"name":"NEW","url":"http://new.com"}); feeds[0]["name"]="MODIFIED"; assert thread.feeds[0]["name"]=="CNN" and len(thread.feeds)==1
    """
    mod = _import_module()
    original = [{"name": "CNN", "url": "http://cnn.com"}, {"name": "BBC", "url": "http://bbc.com"}]
    thread = mod.ScrapeThread(original)
    original.append({"name": "NEW", "url": "http://new.com"})
    original[0]["name"] = "MODIFIED"
    assert len(thread.feeds) == 2, "thread.feeds should not grow"
    assert thread.feeds[0]["name"] == "CNN", "thread.feeds should be deep-copied"
    assert thread.feeds[1]["name"] == "BBC"


def test_run_emits_finished_success():
    r"""Layer 2 — run() must emit finished_signal with (new_count, total_count, []) on success.

    WHAT:
      Mocks fetch_all_feeds to return ([{"title":"test"}], []) and save_articles
      to return (1, 10). Starts a ScrapeThread with an empty feeds list,
      connects to finished_signal, calls run(), and verifies the emitted
      tuple is exactly (1, 10, []).

    WHY:
      This is the happy-path contract for the background thread. The GUI's
      on_done handler expects exactly this tuple shape. If the thread emits
      wrong values or the wrong number of values, the UI will display
      incorrect statistics.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if results == [(1, 10, [])].
      Raises AssertionError if the emitted tuple differs.

    ERRORS/EDGE CASES:
      - fetch_all_feeds returns empty articles: new=0, total should reflect save_articles output.
      - save_articles returns different counts: emitted values match save_articles return.
      - Signal emitted multiple times: results list has more than one entry.

    HOW TO TEST:
      1. Patch fetch_all_feeds to return ([{"title":"x"}], []), patch save_articles to return (1, 10).
      2. Create thread = ScrapeThread([]), connect a lambda to finished_signal.
      3. Call thread.run().
      4. Assert results == [(1, 10, [])].
      Realistic example: mock_fetch.return_value = ([{"title":"Breaking: AI news"}], []); mock_save.return_value = (1, 100); thread.run(); assert results == [(1, 100, [])]
    """
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
    r"""Layer 2 — run() must catch exceptions and emit finished_signal(0, 0, [error_dict]).

    WHAT:
      Mocks fetch_all_feeds to raise RuntimeError("fail"). Creates a
      ScrapeThread, connects to finished_signal, calls run(), and verifies
      that the emitted result is (0, 0, [{"feed_name":"System","error":"fail"}]).

    WHY:
      The background thread must never let exceptions propagate to the Qt
      event loop, which would crash the application. Instead, it catches
      all errors and emits a structured failure result so the GUI can
      display the error message to the user gracefully.

    OPTIONS:
      None. This test requires no optional parameters.

    DEFAULTS:
      None.

    OUTPUT/EFFECT:
      Passes if results[0] == (0, 0, [{"feed_name":"System","error":"fail"}]).
      Raises AssertionError if the error is not caught or emitted correctly.

    ERRORS/EDGE CASES:
      - Exception type other than RuntimeError (e.g., ValueError, TypeError): should still be caught.
      - Exception with no message (e.g., RuntimeError()): str(e) is empty string.
      - Exception raised by save_articles instead of fetch_all_feeds: same catch behavior.

    HOW TO TEST:
      1. Patch fetch_all_feeds to raise RuntimeError("fail").
      2. Create thread = ScrapeThread([]), connect lambda to finished_signal.
      3. Call thread.run().
      4. Assert len(results)==1, results[0][0]==0, results[0][1]==0, results[0][2][0]["feed_name"]=="System", results[0][2][0]["error"]=="fail".
      Realistic example: mock_fetch.side_effect = ConnectionError("timeout"); thread.run(); assert results[0][2][0]["error"] == "timeout"
    """
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
