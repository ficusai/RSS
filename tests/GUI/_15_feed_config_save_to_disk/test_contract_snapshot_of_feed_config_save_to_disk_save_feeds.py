"""Contract-drift tests for gui/_15_feed_config_save_to_disk/save_feeds.py

CONTRACT SNAPSHOT
  module   : gui._15_feed_config_save_to_disk.save_feeds
  function : save_feeds(window) -> None
  imports  : gui._00_paths_config_constant_definitions.paths_config_constants.CONFIG_PATH
             , gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
  effects  : writes config/feeds.json with {"feeds": [...]} + 2-space indent
  errors   : logs via append_log_message on exception
"""
# WHAT: This file protects the recorded CONTRACT of the source function
# gui/_15_feed_config_save_to_disk/save_feeds.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Writes the current feed list window.feeds to config/feeds.json as the JSON
#   object {"feeds": [...]} with 2-space indentation, creating the config/
#   parent folder automatically if it does not exist.
#   If anything fails (permissions, disk full, ...), NO error escapes the
#   function: a message is appended to the operations log instead, using
#   append_log_message(window, "Save error: ...").
# OPTIONS: window.feeds must be a list of feed dicts; CONFIG_PATH patched to
#            temp folders in the tests below.
# DEFAULTS: parent directories are created automatically on save.
# OUTPUT/EFFECT: the JSON config file exists on disk with the feed list.
# ERRORS/EDGE CASES: write failure -> logged, function completes silently.
# HOW TO TEST: save_feeds(window), then load the file back and compare.

# import json — Python's JSON reader/writer (json.dump serialises objects to
#   text). Used to read back the saved file and verify its contents.
import json
# import sys — runtime controls; plants fake PyQt6 modules and extends import path.
import sys
# import inspect — reads a function's declared parameters without running it.
import inspect
# import Path — readable file-system paths.
from pathlib import Path
# import TemporaryDirectory — creates a real throwaway FOLDER. When the "with"
#   block ends, the folder and everything inside it are deleted automatically.
from tempfile import TemporaryDirectory
# import MagicMock, patch — fake objects that record calls + tool to swap a name
#   inside a module temporarily for a test.
from unittest.mock import patch, MagicMock

# import pytest — the test runner.
import pytest

# Ensure offscreen platform for headless Qt rendering
# Plant fake PyQt6 packages BEFORE any real Qt import so no screen is needed.
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

# PROJECT_ROOT: three folders up from this test file = the RSS project root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Put the root on Python's import search path (once).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Shared helpers from conftest.py: structural assertions + the fake WindowStub.
from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
# Import the REAL source function being guarded.
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds


# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the contract of
# gui/_15_feed_config_save_to_disk/save_feeds.py. The source function
# save_feeds(window) writes the current feed list window.feeds to
# config/feeds.json as the JSON object {"feeds": [...]} with 2-space indentation,
# creating parent directories automatically if needed. On any write failure, the
# function logs the error via append_log_message instead of raising.
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 (Structural):
#   - test_signature               : exactly save_feeds(window) -> None
#   - test_source_imports          : source must import paths constants + log module
#   - test_callables               : module defines exactly one public function
# Layer 2 (Behavioral):
#   - test_writes_config_json_with_two_space_indent  : saved JSON has correct shape + indent
#   - test_creates_config_parent_directory           : parent dirs created automatically
#   - test_error_logs_via_append_log_message         : write failure logs instead of raising
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================
# Shape-of-the-code checks to catch refactor drift. The separator bars below
# are the file's original formatting and are kept verbatim.

class TestLayer1Structural:
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the physical shape of the source module without running it.
    These tests catch refactor drift such as renamed parameters, moved files,
    or unwanted new imports BEFORE behaviour tests are even executed.
    """

    def test_signature(self):
        r"""WHAT: Verifies the exact signature of save_feeds(window) -> None.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the function has exactly one parameter named
          "window" (positional-or-keyword, no default) and returns None.
        ERRORS/EDGE CASES: If a developer renamed the parameter or added a
          second one, this test fails with the mismatched signature details.
        HOW TO TEST: Run `pytest tests/GUI/_15_feed_config_save_to_disk/`.
          A failure prints the expected vs. actual parameter list.
        """
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, returns None.
        assert_signature(save_feeds, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        r"""WHAT: Verifies the source imports the paths constants and log modules.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if ast.parse finds both imports in the source.
        ERRORS/EDGE CASES: If either import disappears, the function can no
          longer locate the config file or report save errors.
        HOW TO TEST: Run `pytest tests/GUI/_15_feed_config_save_to_disk/`.
          A failure lists the missing import names.
        """
        # Point at the real source file on disk.
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_15_feed_config_save_to_disk" / "save_feeds.py")
        # The source MUST import the paths module (CONFIG_PATH) AND the log
        # module (append_log_message, used to report save errors).
        assert_source_imports(module_path, {
            "gui._00_paths_config_constant_definitions.paths_config_constants",
            "gui._10_log_append_timestamped_message.append_timestamped_log",
        })

    def test_callables(self):
        r"""WHAT: Verifies the module defines exactly one public function.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the only public function is "save_feeds".
        ERRORS/EDGE CASES: If a developer accidentally adds a new public
          function, this test fails and warrants regenerating the snapshot.
        HOW TO TEST: Run `pytest tests/GUI/_15_feed_config_save_to_disk/`.
          A failure lists the unexpected public function names.
        """
        # The module must define EXACTLY the public function "save_feeds".
        import gui._15_feed_config_save_to_disk.save_feeds as mod
        assert_callables(mod, {"save_feeds"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests run save_feeds against temporary folders on disk and inspect
# the actual files produced, plus the error-logging fallback.

class TestLayer2Behavioral:
    """Layer 2 — Behavioural smoke tests.

    WHAT: Calls the real source function against temporary folders on disk and
    inspects the actual files produced, plus the error-logging fallback. These
    tests prove the function writes correct JSON and handles failures gracefully.
    """

    def test_writes_config_json_with_two_space_indent(self):
        r"""WHAT: Verifies save_feeds writes correct JSON with 2-space indent.

        OPTIONS: window.feeds must be a list of feed dicts; CONFIG_PATH patched
          to a temporary location.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: The config file exists on disk, contains
          {"feeds": <window.feeds>}, and uses 2-space indentation.
        ERRORS/EDGE CASES: None — this is the happy path with a writable temp dir.
        HOW TO TEST: In the app, add a couple of feeds and click "Save". Open
          config/feeds.json and verify it contains the feeds with 2-space
          indentation, e.g. '  "feeds"'.
        """
        # TemporaryDirectory makes a fresh throwaway folder; at the end of the
        # with block, the whole folder (and any files written inside) vanishes.
        with TemporaryDirectory() as tmpdir:
            # Pretend the config file lives at <temp>/config/feeds.json.
            fake_config = Path(tmpdir) / "config" / "feeds.json"
            window = WindowStub()
            # The feed list the fake window is told to save to disk.
            window.feeds = [
                {"id": "a", "name": "Feed A", "url": "https://a.com/feed", "enabled": True},
                {"id": "b", "name": "Feed B", "url": "https://b.com/feed", "enabled": False},
            ]
            # Redirect the module's CONFIG_PATH to the fake location, run the
            # function, then automatically restore CONFIG_PATH afterwards.
            with patch("gui._15_feed_config_save_to_disk.save_feeds.CONFIG_PATH", fake_config):
                save_feeds(window)

            # The file must now physically exist. store_text() reads it back.
            assert fake_config.exists()
            data = json.loads(fake_config.read_text())
            # The saved JSON must be EXACTLY {"feeds": <window's feed list>}.
            assert data == {"feeds": window.feeds}

            # Verify 2-space indent
            # Look at the RAW text: it must contain '  "feeds"' — the "feeds"
            # key preceded by exactly TWO spaces. That proves json.dump used
            # indent=2 (not tabs, not 4 spaces, not one space).
            raw = fake_config.read_text()
            assert '  "feeds"' in raw

    def test_creates_config_parent_directory(self):
        r"""WHAT: Verifies save_feeds creates parent directories automatically.

        OPTIONS: window.feeds must be a list; CONFIG_PATH patched to a deep
          temporary path whose parent folders do not exist yet.
        DEFAULTS: parent directories are created automatically on save.
        OUTPUT/EFFECT: The deepest parent folder exists after the call.
        ERRORS/EDGE CASES: None — mkdir(parents=True, exist_ok=True) handles
          this case gracefully.
        HOW TO TEST: In the app, point CONFIG_PATH at a nested path that does
          not exist yet (e.g. config/deep/nested/feeds.json), then save. The
          parent folders should be created automatically.
        """
        with TemporaryDirectory() as tmpdir:
            # A deliberately DEEP config path whose parent folders ("deep" and
            # "deep/nested") do NOT exist yet.
            fake_config = Path(tmpdir) / "deep" / "nested" / "feeds.json"
            window = WindowStub()
            window.feeds = []            # an empty list is still valid data
            with patch("gui._15_feed_config_save_to_disk.save_feeds.CONFIG_PATH", fake_config):
                save_feeds(window)
            # The source calls config_path.parent.mkdir(parents=True,
            # exist_ok=True) BEFORE the write, so the deepest parent folder
            # must exist after the call succeeds.
            assert fake_config.parent.exists()

    def test_error_logs_via_append_log_message(self):
        r"""WHAT: Verifies write failures are logged instead of raised.

        OPTIONS: window.feeds must be a list; CONFIG_PATH patched to an
          unwritable path; append_log_message patched to a recording fake.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: append_log_message is called once with an error string;
          no exception escapes the function.
        ERRORS/EDGE CASES: Write failure (e.g. permission denied, disk full)
          -> logged via append_log_message(window, "Save error: ...").
        HOW TO TEST: In the app, make config/feeds.json read-only or point it
          at a path you lack write permission for, then save. The operation
          should not crash; instead, an error message should appear in the
          operations log.
        """
        window = WindowStub()
        window.feeds = []
        # Point CONFIG_PATH at a folder that cannot realistically be created
        # on a normal system (/nonexistent/path/...), forcing a failure. ALSO
        # replace append_log_message (imported into the source module) with a
        # recording fake, so the error report is captured, not really logged.
        with patch("gui._15_feed_config_save_to_disk.save_feeds.CONFIG_PATH", Path("/nonexistent/path/feeds.json")):
            with patch("gui._15_feed_config_save_to_disk.save_feeds.append_log_message") as mock_log:
                save_feeds(window)
                # On failure the source must call append_log_message once
                # (with "Save error: ..."); no exception may escape the call.
                mock_log.assert_called_once()
