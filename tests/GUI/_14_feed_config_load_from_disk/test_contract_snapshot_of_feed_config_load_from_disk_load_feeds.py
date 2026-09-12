"""Contract-drift tests for gui/_14_feed_config_load_from_disk/load_feeds.py

CONTRACT SNAPSHOT
  module   : gui._14_feed_config_load_from_disk.load_feeds
  function : load_feeds(window) -> None
  imports  : gui._00_paths_config_constant_definitions.paths_config_constants.CONFIG_PATH
  effects  : sets window.feeds from config/feeds.json
  errors   : missing/malformed file → window.feeds == []
"""
# WHAT: This file protects the recorded CONTRACT of the source function
# gui/_14_feed_config_load_from_disk/load_feeds.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Reads the RSS feed subscriptions file (config/feeds.json, whose path comes
#   from the constant CONFIG_PATH) and stores the result in window.feeds.
#   Accepted file shapes: {"feeds": [...]} (wrapped) or [...] (raw list).
#   If the file is missing or unparseable, window.feeds becomes [].
# OPTIONS: window must have a 'feeds' attribute; CONFIG_PATH patched to fake
#            files in the behavioural tests below.
# DEFAULTS: missing or corrupt file -> empty list [].
# OUTPUT/EFFECT: window.feeds is a list of feed dicts loaded from disk JSON.
# ERRORS/EDGE CASES: no file -> []; malformed JSON -> []; dict with a "feeds"
#            key -> that list extracted; bare top-level list -> used directly.
# HOW TO TEST: load_feeds(window); then assert isinstance(window.feeds, list).

# import json — Python's standard library for reading/writing JSON data files
#   (JSON is the text format used to store the feed subscription list).
import json
# import sys — runtime controls; here we plant fake PyQt6 modules and extend the
#   import search path so the source modules can be reached.
import sys
# import inspect — reads a function's declared parameters without running it.
import inspect
# import Path — readable file-system paths.
from pathlib import Path
# import NamedTemporaryFile — creates a real throwaway FILE on disk for a test;
#   we write test JSON into it, point CONFIG_PATH at it, and delete it after.
from tempfile import NamedTemporaryFile
# import MagicMock, patch — fake objects that record calls, and the tool to swap
#   a name inside a module temporarily for the duration of a test.
from unittest.mock import MagicMock, patch

# import pytest — the test runner (turns failing asserts into readable reports).
import pytest

# Ensure offscreen platform for headless Qt rendering
# Plant fake PyQt6 packages into the module registry BEFORE anything imports
# the real ones, so no real screen/Qt is needed to run these tests.
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

# PROJECT_ROOT: three folders up from this test file = the RSS project root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Make sure the root is on Python's import search path (one time only).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Shared helpers from conftest.py (see _13 test file comments for a full
# breakdown of each helper): structural assertions + the fake WindowStub.
from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
# Import the REAL source function being guarded.
from gui._14_feed_config_load_from_disk.load_feeds import load_feeds


===============================================================================
============== WHAT THIS TEST FILE VERIFIES ===============
This file protects the contract of
gui/_14_feed_config_load_from_disk/load_feeds.py. The source function
load_feeds(window) reads the RSS feed subscriptions from config/feeds.json
(the path comes from CONFIG_PATH) and stores the result in window.feeds.
It accepts both wrapped format {"feeds": [...]} and bare list format [...].
If the file is missing or contains invalid JSON, window.feeds becomes [].
===============================================================================
============== LAYER BREAKDOWN ===============
Layer 1 (Structural):
  - test_signature               : exactly load_feeds(window) -> None
  - test_source_imports          : source must import the paths constants module
  - test_callables               : module defines exactly one public function
Layer 2 (Behavioral):
  - test_missing_file_yields_empty_list       : absent file -> window.feeds == []
  - test_malformed_json_yields_empty_list     : corrupt JSON -> window.feeds == []
  - test_dict_with_feeds_key_extracted        : {"feeds": [...]} -> inner list assigned
  - test_raw_list_used_directly               : [...] -> list used as-is
===============================================================================
============== LAYER WHAT EACH TEST CHECKS ===============
===============================================================================


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================
# Level-1 tests check the SHAPE of the code (signature, imports, callables)
# to catch refactor drift before behaviour is even considered. The separator
# bars below are the file's original formatting and are kept verbatim.

class TestLayer1Structural:
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the physical shape of the source module without running it.
    These tests catch refactor drift such as renamed parameters, moved files,
    or unwanted new imports BEFORE behaviour tests are even executed.
    """

    def test_signature(self):
        """WHAT: Verifies the exact signature of load_feeds(window) -> None.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the function has exactly one parameter named
          "window" (positional-or-keyword, no default) and returns None.
        ERRORS/EDGE CASES: If a developer renamed the parameter or added a
          second one, this test fails with the mismatched signature details.
        HOW TO TEST: Run `pytest tests/GUI/_14_feed_config_load_from_disk/`.
          A failure prints the expected vs. actual parameter list.
        """
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, function returns None.
        assert_signature(load_feeds, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verifies the source imports the paths constants module.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if ast.parse finds the paths constants import
          in the source file.
        ERRORS/EDGE CASES: If the import disappears, the function can no
          longer locate the config file on disk.
        HOW TO TEST: Run `pytest tests/GUI/_14_feed_config_load_from_disk/`.
          A failure lists the missing import names.
        """
        # Point at the real source file (project root + gui/_14...).
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_14_feed_config_load_from_disk" / "load_feeds.py")
        # The source MUST import the paths module (it provides CONFIG_PATH).
        assert_source_imports(module_path, {"gui._00_paths_config_constant_definitions.paths_config_constants"})

    def test_callables(self):
        """WHAT: Verifies the module defines exactly one public function.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the only public function is "load_feeds".
        ERRORS/EDGE CASES: If a developer accidentally adds a new public
          function, this test fails and warrants regenerating the snapshot.
        HOW TO TEST: Run `pytest tests/GUI/_14_feed_config_load_from_disk/`.
          A failure lists the unexpected public function names.
        """
        # The module must define EXACTLY the public function "load_feeds".
        import gui._14_feed_config_load_from_disk.load_feeds as mod
        assert_callables(mod, {"load_feeds"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests actually run load_feeds against fake files on disk and check
# which feed list ends up in window.feeds.

class TestLayer2Behavioral:
    """Layer 2 — Behavioural smoke tests.

    WHAT: Calls the real source function against fake files on disk and checks
    which feed list ends up in window.feeds. These tests prove the function
    handles all documented file shapes and error cases.
    """

    def test_missing_file_yields_empty_list(self):
        """WHAT: A missing config file leaves window.feeds as an empty list.

        OPTIONS: window must have a 'feeds' attribute; CONFIG_PATH patched to
          a fake path whose .exists() returns False.
        DEFAULTS: missing file -> empty list [].
        OUTPUT/EFFECT: window.feeds is set to [].
        ERRORS/EDGE CASES: The source checks config_path.exists() first; if
          False, it sets window.feeds = [] and returns immediately.
        HOW TO TEST: In the app, rename or delete config/feeds.json, then
          restart. The feed list should be empty (no feeds loaded).
        """
        # Headless window stub.
        window = WindowStub()
        # Patch: replace the constant CONFIG_PATH INSIDE the source module's
        # namespace with a fake object whose .exists() answers False, i.e.
        # "the feeds.json file does not exist".
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH") as fake_path:
            fake_path.exists.return_value = False
            load_feeds(window)
        # Contract: a missing config file must NOT crash the app; the window
        # simply ends up with an empty feed list [].
        assert window.feeds == []

    def test_malformed_json_yields_empty_list(self):
        """WHAT: Malformed JSON in the config file leaves window.feeds as [].

        OPTIONS: window must have a 'feeds' attribute; CONFIG_PATH patched to
          a temporary file containing invalid JSON.
        DEFAULTS: malformed file -> empty list [].
        OUTPUT/EFFECT: window.feeds is set to [].
        ERRORS/EDGE CASES: json.load inside the source raises on invalid text;
          the source's "except Exception:" catches it and sets window.feeds = [].
        HOW TO TEST: In the app, write garbage text into config/feeds.json,
          then restart. The feed list should be empty (no crash).
        """
        window = WindowStub()
        # Create a real temporary file and write BROKEN JSON text into it
        # (missing quotes/brackets — json.load cannot parse this).
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{not valid json")
            tmp = f.name          # remember the temporary file's full path
        # Path as P: short alias so the patched CONFIG_PATH can be given a
        # real pathlib.Path pointing at the corrupt temp file.
        from pathlib import Path as P
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH", P(tmp)):
            load_feeds(window)
        # json.load inside the source raises on this text; the source's
        # "except Exception:" catches it and sets window.feeds = [].
        assert window.feeds == []
        # Clean up: delete the temporary file (missing_ok=True = don't error
        # if somebody already removed it).
        Path(tmp).unlink(missing_ok=True)

    def test_dict_with_feeds_key_extracted(self):
        """WHAT: A {"feeds": [...]} file extracts the inner list into window.feeds.

        OPTIONS: window must have a 'feeds' attribute; CONFIG_PATH patched to
          a temporary file containing valid wrapped JSON.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: window.feeds is set to the inner list from the JSON.
        ERRORS/EDGE CASES: None — this is the standard wrapped format.
        HOW TO TEST: In the app, ensure config/feeds.json contains
          {"feeds": [{"name": "Tech", "url": "https://t.com/feed", "enabled": true}]}.
          Restart and verify the feed appears in the list.
        """
        window = WindowStub()
        # The subscribed-feed data we will encode as JSON.
        feeds_data = [{"id": "t", "name": "Tech", "url": "https://t.com/feed", "enabled": True}]
        # Encode it in the WRAPPED format: a dict holding a "feeds" key whose
        # value is the feed list. Example of the file on disk: {"feeds": [...]}.
        content = json.dumps({"feeds": feeds_data})
        # Write that content into a temporary JSON file.
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(content)
            tmp = f.name
        from pathlib import Path as P
        # Point CONFIG_PATH at the temp file and run the real function.
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH", P(tmp)):
            load_feeds(window)
        # The source saw a dict, called data.get("feeds", data), and assigned
        # exactly the inner list to window.feeds.
        assert window.feeds == feeds_data
        Path(tmp).unlink(missing_ok=True)

    def test_raw_list_used_directly(self):
        """WHAT: A bare [...] JSON file is used directly as window.feeds.

        OPTIONS: window must have a 'feeds' attribute; CONFIG_PATH patched to
          a temporary file containing valid bare-list JSON.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: window.feeds is set to the top-level list from the JSON.
        ERRORS/EDGE CASES: None — this is the legacy bare-list format.
        HOW TO TEST: In the app, write a bare list like
          [{"name": "API", "url": "https://a.com/feed", "enabled": false}]
          into config/feeds.json. Restart and verify the feed appears.
        """
        window = WindowStub()
        feeds_data = [{"id": "a", "name": "API", "url": "https://a.com/feed", "enabled": False}]
        # Encode the SAME data in the LEGACY format: a bare top-level list with
        # NO "feeds" wrapper dict at all.
        content = json.dumps(feeds_data)
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(content)
            tmp = f.name
        from pathlib import Path as P
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH", P(tmp)):
            load_feeds(window)
        # Because the parsed data is NOT a dict, the source uses the list
        # itself (data.get shortcut is skipped) -> identical list assigned.
        assert window.feeds == feeds_data
        Path(tmp).unlink(missing_ok=True)
