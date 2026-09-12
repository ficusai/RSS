"""Contract-drift tests for gui/_13_stats_badges_update_live/update_stats_badges.py

CONTRACT SNAPSHOT
  module   : gui._13_stats_badges_update_live.update_stats_badges
  function : update_stats_badges(window) -> None
  imports  : core.storage.get_stats
  effects  : sets window.lbl_articles_stat.setText / window.lbl_feeds_stat.setText
  errors   : exception -> badges unchanged (silent)
"""
# WHAT: This file protects the recorded CONTRACT of the source function
# gui/_13_stats_badges_update_live/update_stats_badges.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Reads the article count from the SQLite database via core.storage.get_stats(),
#   counts total vs. enabled feeds from window.feeds, then updates two header
#   badges: "Articles" and "Feeds Active".
#   If anything raises, it does nothing silently (the except clause passes).
# OPTIONS: window must expose lbl_articles_stat, lbl_feeds_stat (QLabels) and
#            a feeds list where each feed dict may have an 'enabled' key.
# DEFAULTS: missing 'enabled' key counts the feed as ACTIVE (True); missing
#            'total_articles' stat falls back to 0.
# OUTPUT/EFFECT: two label setText calls with the formatted badge strings.
# ERRORS/EDGE CASES: get_stats() raising -> pass (badges keep old text);
#            a feed missing its 'enabled' key -> treated as enabled.
# HOW TO TEST: call update_stats_badges(window) and inspect the setText calls.

# import json — Python's standard library for JSON data files. Not directly used
#   in this test module but listed for completeness of the import overview.
import json
# import sys — Python runtime controls; here we plant fake PyQt6 modules into
#   the registry (sys.modules) and add the project root to the import search path.
import sys
# import inspect — reads a function's declared parameters without running the code.
import inspect
# import Path — readable file-system paths.
from pathlib import Path
# import MagicMock, patch — fake objects that record calls, and the tool to swap a
#   name inside a module temporarily for the duration of a test, then restore it.
from unittest.mock import MagicMock, patch

# import pytest — the test runner: every def test_*() is discovered and run; an
#   assert that fails turns into a readable failure report.
import pytest

# Ensure offscreen platform for headless Qt rendering
# sys.modules is the dictionary "modules Python already knows about".
# setdefault(key, value) inserts our fake Qt packages ONLY IF they are not
# already loaded. Planting MagicMock stand-ins for the PyQt6 packages BEFORE
# the real source module is imported means any downstream Qt import (e.g.
# core.storage pulling in QtWidgets) receives a harmless fake, so the tests
# run on machines with no screen and no Qt installation at all.
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())

# PROJECT_ROOT: three folders up from this file is the RSS project root
# (test file -> _13... -> GUI -> tests -> RSS/).
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Add the root to Python's import search path (once), so the imports below
# ("from gui._13... import" and "from tests.GUI.conftest import") resolve.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import the shared test helpers that conftest.py provides for the whole suite:
#   assert_signature(func, expected_params, expected_return)
#       compares a function's real parameters + return annotation to the
#       recorded contract snapshot.
#   assert_constants(module, pairs)
#       checks module-level constants against expected values.
#   assert_source_imports(module_path, expected_set)
#       parses the source file and insists the expected import names appear.
#   assert_callables(module, allowed_set)
#       insists the module defines exactly the expected public functions.
#   WindowStub
#       a fake MainWindow: every attribute the GUI handlers touch (badges,
#       tables, combo boxes, log box, ...) is a MagicMock, and window.feeds /
#       window.current_articles are real plain lists.
from tests.GUI.conftest import assert_signature, assert_constants, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
# Import the REAL source function we are guarding. Note this import happens
# AFTER the fake-PyQt6 and sys.path setup above on purpose.
from gui._13_stats_badges_update_live.update_stats_badges import update_stats_badges


# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the contract of
# gui/_13_stats_badges_update_live/update_stats_badges.py. The source function
# update_stats_badges(window) reads article statistics from the SQLite database
# via core.storage.get_stats(), counts total and active feeds from window.feeds,
# and updates two header badges: "Articles" and "Feeds Active". If anything
# raises an exception, the function silently passes — the badges keep their
# previous text.
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 (Structural):
#   - test_signature             : exactly update_stats_badges(window) -> None
#   - test_source_imports        : source must import core.storage
#   - test_callables             : module defines exactly one public function
# Layer 2 (Behavioral):
#   - test_sets_article_and_feed_badges    : correct badge text from fake stats
#   - test_exception_preserves_badges      : exception leaves badges unchanged
#   - test_missing_enabled_key_defaults_true: missing 'enabled' key counts as active
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================
# "LAYER 1" tests are STRUCTURAL: they inspect the SHAPE of the code (file,
# signature, imports, callables) without running any behaviour. If a refactor
# renamed a parameter, moved a file, or added imports, these tests fail early
# and point the developer at the drift. The separator bars below are original
# file formatting and are kept verbatim.

class TestLayer1Structural:
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the physical shape of the source module without running it.
    These tests catch refactor drift such as renamed parameters, moved files,
    or unwanted new imports BEFORE behaviour tests are even executed.
    """

    def test_signature(self):
        r"""WHAT: Verifies the exact signature of update_stats_badges(window) -> None.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the function has exactly one parameter named
          "window" (positional-or-keyword, no default) and returns None.
        ERRORS/EDGE CASES: If a developer renamed the parameter, added a second
          one, or changed the return type, this test fails with the mismatch.
        HOW TO TEST: Run `pytest tests/GUI/_13_stats_badges_update_live/`. A
          failure prints the expected vs. actual parameter list.
        """
        # Recorded contract: exactly one parameter, name "window", kind 1
        # (1 = inspect.Parameter.POSITIONAL_OR_KEYWORD: passable by position
        # OR by keyword), with no default value (inspect.Parameter.empty),
        # and the function returns None.
        assert_signature(update_stats_badges, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        r"""WHAT: Verifies the source imports core.storage (for get_stats).

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if ast.parse finds "core.storage" in the source.
        ERRORS/EDGE CASES: If the import disappears, the contract is broken and
          the function can no longer read statistics from the database.
        HOW TO TEST: Run `pytest tests/GUI/_13_stats_badges_update_live/`. A
          failure lists the missing import names.
        """
        # Point assert_source_imports at the real source file on disk
        # (three folders up, then down into gui/_13_stats_badges_update_live/).
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_13_stats_badges_update_live" / "update_stats_badges.py")
        # The source MUST import 'core.storage' (it provides get_stats).
        # If that import disappears, the contract is broken.
        assert_source_imports(module_path, {"core.storage"})

    def test_callables(self):
        r"""WHAT: Verifies the module defines exactly one public function.

        OPTIONS: None.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes if the only public function is "update_stats_badges".
        ERRORS/EDGE CASES: If a developer accidentally adds a new public
          function, this test fails and warrants regenerating the snapshot.
        HOW TO TEST: Run `pytest tests/GUI/_13_stats_badges_update_live/`. A
          failure lists the unexpected public function names.
        """
        # Import the module and insist it defines EXACTLY one public function
        # named "update_stats_badges" (no new public functions added, none
        # removed). Private names and re-imported names are filtered out.
        import gui._13_stats_badges_update_live.update_stats_badges as mod
        assert_callables(mod, {"update_stats_badges"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# "LAYER 2" tests actually CALL the source function against fakes and check
# the visible side effects. "Smoke" = quick sanity checks that the function
# basically works and handles its documented edge cases.

class TestLayer2Behavioral:
    """Layer 2 — Behavioural smoke tests.

    WHAT: Calls the real source function against fakes and checks the visible
    side effects. These tests prove the function updates badges correctly.
    """

    def test_sets_article_and_feed_badges(self):
        r"""WHAT: Verifies correct badge text from fake stats and feed list.

        OPTIONS: window must expose lbl_articles_stat, lbl_feeds_stat (with
          setText), and a feeds list where each feed dict may have an 'enabled'
          key.
        DEFAULTS: missing 'enabled' key counts the feed as ACTIVE (True);
          missing 'total_articles' stat falls back to 0.
        OUTPUT/EFFECT: lbl_articles_stat.setText("150 Articles") and
          lbl_feeds_stat.setText("2/3 Feeds Active") are each called once.
        ERRORS/EDGE CASES: None — this is the happy path with explicit fakes.
        HOW TO TEST: In the app, ensure the database has 150 articles and the
          feed list has 2 active + 1 disabled feed. The header badges should
          read "150 Articles" and "2/3 Feeds Active".
        """
        # Build a fake window and give it a 3-feed list where feeds "a" and
        # "c" are enabled and "b" is disabled (2 active out of 3 total).
        window = WindowStub()
        window.feeds = [
            {"id": "a", "enabled": True},
            {"id": "b", "enabled": False},
            {"id": "c", "enabled": True},
        ]
        # patch(...) temporarily REPLACES the name get_stats inside the SOURCE
        # module's namespace with a fake that returns {"total_articles": 150}.
        # This lets us test the formatting without a real SQLite database.
        with patch("gui._13_stats_badges_update_live.update_stats_badges.get_stats",
                   return_value={"total_articles": 150}):
            update_stats_badges(window)

        # WindowStub's badges are MagicMocks: setText must have been called
        # exactly once with "150 Articles" (150 comes from the fake stats).
        window.lbl_articles_stat.setText.assert_called_once_with("📰 150 Articles")
        # 2 enabled out of 3 total -> "2/3 Feeds Active".
        window.lbl_feeds_stat.setText.assert_called_once_with("📡 2/3 Feeds Active")

    def test_exception_preserves_badges(self):
        r"""WHAT: Verifies exceptions leave badge text unchanged.

        OPTIONS: window must expose lbl_articles_stat and lbl_feeds_stat (with
          setText).
        DEFAULTS: N/A.
        OUTPUT/EFFECT: No setText calls succeed; badges keep their previous text.
        ERRORS/EDGE CASES: get_stats() raising -> pass (badges keep old text);
          a setText call raising -> pass (the try/except catches it).
        HOW TO TEST: In the app, break the database connection and call
          update_stats_badges. The badges should retain their previous text
          rather than showing an error or blank.
        """
        window = WindowStub()
        # side_effect = "whenever setText runs, it EXPLODES with this error".
        # This simulates a broken/unreachable widget.
        window.lbl_articles_stat.setText.side_effect = Exception("boom")
        # Should not propagate
        # The source wraps ALL its work in "try: ... except Exception: pass",
        # so even when the fake widget explodes, no error escapes this call
        # and the function completes silently (badges keep whatever they had).
        update_stats_badges(window)
        # Badges should not have been set (exception inside try is caught)
        # Now remove the "boom" from the article badge...
        window.lbl_articles_stat.setText.side_effect = None
        # ...and plant the explosion on the FEED badge instead.
        window.lbl_feeds_stat.setText.side_effect = Exception("boom")
        update_stats_badges(window)

    def test_missing_enabled_key_defaults_true(self):
        r"""WHAT: Verifies a feed without 'enabled' is counted as active.

        OPTIONS: window must expose lbl_feeds_stat (with setText) and a feeds
          list where a dict may lack an 'enabled' key.
        DEFAULTS: missing 'enabled' key counts the feed as ACTIVE (True).
        OUTPUT/EFFECT: lbl_feeds_stat.setText("1/1 Feeds Active") is called.
        ERRORS/EDGE CASES: A feed dict with no 'enabled' key is treated as
          enabled (f.get("enabled", True) returns the fallback True).
        HOW TO TEST: In the app, add a feed without an 'enabled' field to the
          list. The badge should show it as active, e.g. "1/1 Feeds Active".
        """
        window = WindowStub()
        # A feed dict with NO "enabled" key at all. In the source,
        # f.get("enabled", True) returns the fallback True for such a feed,
        # i.e. the feed is assumed to be ACTIVE.
        window.feeds = [{"id": "x"}]
        with patch("gui._13_stats_badges_update_live.update_stats_badges.get_stats",
                   return_value={"total_articles": 0}):
            update_stats_badges(window)
        # 1 feed present, no "enabled" key -> counted as enabled, so the badge
        # must read "1/1 Feeds Active".
        window.lbl_feeds_stat.setText.assert_called_once_with("📡 1/1 Feeds Active")
