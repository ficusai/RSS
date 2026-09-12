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

# json = Python's JSON reader/writer (json.dump serialises objects to text).
import json
# sys = runtime controls; plants fake PyQt6 modules and extends import path.
import sys
# inspect = reads a function's declared parameters without running it.
import inspect
# Path = readable file-system paths.
from pathlib import Path
# TemporaryDirectory = creates a real throwaway FOLDER. When the "with" block
# ends, the folder and everything inside it are deleted automatically.
from tempfile import TemporaryDirectory
# MagicMock / patch = fake objects that record calls + tool to swap a name
# inside a module temporarily for a test.
from unittest.mock import patch, MagicMock

# pytest = the test runner.
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
# Layer 1 — Structural
# ===========================================================================
# Shape-of-the-code checks to catch refactor drift. The separator bars below
# are the file's original formatting and are kept verbatim.

class TestLayer1Structural:

    def test_signature(self):
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, returns None.
        assert_signature(save_feeds, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
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
        # The module must define EXACTLY the public function "save_feeds".
        import gui._15_feed_config_save_to_disk.save_feeds as mod
        assert_callables(mod, {"save_feeds"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests run save_feeds against temporary folders on disk and inspect
# the actual files produced, plus the error-logging fallback.

class TestLayer2Behavioral:

    def test_writes_config_json_with_two_space_indent(self):
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