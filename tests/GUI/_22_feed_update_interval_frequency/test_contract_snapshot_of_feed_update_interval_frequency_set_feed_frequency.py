"""Contract-drift tests for gui/_22_feed_update_interval_frequency/set_feed_frequency.py

CONTRACT SNAPSHOT
  module   : gui._22_feed_update_interval_frequency.set_feed_frequency
  function : set_feed_frequency(window, fid: str, hours) -> None
  imports  : gui._15_feed_config_save_to_disk.save_feeds.save_feeds
  effects  : sets feed["fetch_interval_hours"] = hours; calls save_feeds
  errors   : None — silently skips if fid not found
"""
# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the recorded CONTRACT of
# gui/_22_feed_update_interval_frequency/set_feed_frequency.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Search window.feeds for the first feed whose "id" equals fid. If found:
#     - set feed["fetch_interval_hours"] = hours
#     - call save_feeds(window)
#   If NO feed matches fid, the function does NOTHING — no mutation, no
#   save (silent no-op by contract).
#
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 — Structural: shape-of-the-code checks to catch refactor drift.
# Layer 2 — Behavioral Smoke: fake-window smoke tests that verify the happy
#                              path (interval updated, save called) and the
#                              no-op path (unknown fid, nothing happens).
#
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================
# Layer 1 — Structural:
#   test_signature       - exactly three params: "window", "fid", "hours"
#                          (all positional-or-keyword, no default), returns
#                          None.
#   test_source_imports  - module-level import includes save_feeds.
#   test_callables       - module exposes ONLY the public symbol
#                          "set_feed_frequency".
# Layer 2 — Behavioral Smoke:
#   test_sets_interval_and_calls_save   - known fid's interval flips to the
#                                         requested hours; save_feeds
#                                         called once.
#   test_unknown_fid_is_noop            - unknown fid causes no mutation and
#                                         no helper calls.
# ===========================================================================
# WHAT: Verifies the set_feed_frequency contract survives refactor drift.
# OPTIONS: window with feeds list; fid — feed ID; hours — int
# DEFAULTS: N/A
# OUTPUT/EFFECT: Interval updated in window.feeds; save_feeds called
# ERRORS/EDGE CASES: Unknown fid -> no-op
# HOW TO TEST: set_feed_frequency(window, "fid", 6); check feed.fetch_interval_hours

# sys = runtime controls; plants fake PyQt6 modules and extends import path.
import sys
# inspect = reads a function's declared parameters without running it.
import inspect
# Path = readable file-system paths.
from pathlib import Path
# MagicMock = fake call-recording object; patch = swap a name temporarily.
from unittest.mock import MagicMock, patch

# pytest = the test runner.
import pytest

# Ensure offscreen platform for headless Qt rendering
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

# PROJECT_ROOT: three folders up from here = the RSS project root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Put the root on Python's import search path (once).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Shared helpers from conftest.py: structural assertions + the fake WindowStub.
from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
from gui._22_feed_update_interval_frequency.set_feed_frequency import set_feed_frequency


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:
    """Layer 1 — Structural sanity checks.

    WHAT: Verifies the source module's public shape (signature, imports,
         callable set) has not drifted from the recorded contract.
    OPTIONS: None — these are purely structural invariants.
    DEFAULTS: N/A
    OUTPUT/EFFECT: No runtime effect; raises AssertionError on drift.
    ERRORS/EDGE CASES: None — these are static invariants.
    HOW TO TEST: Run this class in isolation; all three tests must pass.
    """

    def test_signature(self):
        """WHAT: Verify set_feed_frequency accepts exactly three parameters.

        OPTIONS: None — contract is fixed at three parameters: 'window',
                 'fid', and 'hours' (all positional-or-keyword, no defaults),
                 returning None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts the signature matches
                       (window, fid, hours) -> None.
        ERRORS/EDGE CASES: If the source gains or loses parameters the test
                           fails, flagging refactor drift.
        HOW TO TEST: assert_signature(set_feed_frequency, [("window", 1, inspect.Parameter.empty),
                                                           ("fid", 1, inspect.Parameter.empty),
                                                           ("hours", 1, inspect.Parameter.empty)], None)
        """
        assert_signature(set_feed_frequency, [("window", 1, inspect.Parameter.empty),
                                               ("fid", 1, inspect.Parameter.empty),
                                               ("hours", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verify the source file imports required modules on disk.

        OPTIONS: None — the import set is a hard contract.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts AST-parsed source contains save_feeds.
        ERRORS/EDGE CASES: Renaming or removing the import causes failure.
        HOW TO TEST: assert_source_imports(module_path, {"gui._15_feed_config_save_to_disk.save_feeds"})
        """
        module_path = str(Path(__file__).resolve().parents[3]
                          / "gui" / "_22_feed_update_interval_frequency" / "set_feed_frequency.py")
        assert_source_imports(module_path, {"gui._15_feed_config_save_to_disk.save_feeds"})

    def test_callables(self):
        """WHAT: Verify the module exposes exactly one public callable.

        OPTIONS: None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts dir(mod) contains only
                       "set_feed_frequency" among user-defined callables.
        ERRORS/EDGE CASES: Extra or missing callables indicate drift.
        HOW TO TEST: assert_callables(mod, {"set_feed_frequency"})
        """
        import gui._22_feed_update_interval_frequency.set_feed_frequency as mod
        assert_callables(mod, {"set_feed_frequency"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:
    """Layer 2 — Behavioral smoke tests against a fake window.

    WHAT: Verifies the observable behaviour of set_feed_frequency: updating
         a known feed's interval and triggering save, and the no-op path when
         the fid is unknown.
    OPTIONS: window with feeds list; fid — feed ID; hours — int.
    DEFAULTS: N/A
    OUTPUT/EFFECT: Interval updated in window.feeds; save_feeds called.
    ERRORS/EDGE CASES: Unknown fid -> no-op.
    HOW TO TEST: set_feed_frequency(window, "fid", 6); check
                 feed.fetch_interval_hours.
    """

    def test_sets_interval_and_calls_save(self):
        """WHAT: Verify a known feed's interval updates and save fires.

        OPTIONS: window.feeds has two feeds ("a" at 12h, "b" at 6h);
                 fid = "b", hours = 24.
        DEFAULTS: None — both fid and hours are explicitly set.
        OUTPUT/EFFECT: window.feeds[1]["fetch_interval_hours"] becomes 24;
                       save_feeds called once with window.
        ERRORS/EDGE CASES: If the source skips the mutation or save the
                           assertion fails.
        HOW TO TEST: Patch save_feeds; call set_feed_frequency; assert the
                     interval value and mock call count.
        """
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "fetch_interval_hours": 12},
            {"id": "b", "name": "B", "url": "https://b.com/feed", "fetch_interval_hours": 6},
        ]
        with patch("gui._22_feed_update_interval_frequency.set_feed_frequency.save_feeds") as mock_save:
            set_feed_frequency(window, "b", 24)

        assert window.feeds[1]["fetch_interval_hours"] == 24
        mock_save.assert_called_once_with(window)

    def test_unknown_fid_is_noop(self):
        """WHAT: Verify an unknown fid causes no mutation or side effects.

        OPTIONS: window.feeds has one feed with id "a" at 12h;
                 fid = "nonexistent", hours = 1.
        DEFAULTS: None — the unknown fid is intentionally chosen.
        OUTPUT/EFFECT: window.feeds[0]["fetch_interval_hours"] stays 12;
                       save_feeds NOT called.
        ERRORS/EDGE CASES: If the source mutates or calls save on an unknown
                           fid the test fails.
        HOW TO TEST: Patch save_feeds; call set_feed_frequency; assert state
                     unchanged and mock not called.
        """
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "fetch_interval_hours": 12},
        ]
        with patch("gui._22_feed_update_interval_frequency.set_feed_frequency.save_feeds") as mock_save:
            set_feed_frequency(window, "nonexistent", 1)

        assert window.feeds[0]["fetch_interval_hours"] == 12
        mock_save.assert_not_called()
