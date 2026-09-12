"""Contract-drift tests for gui/_21_feed_toggle_enabled_state/toggle_feed_state.py

CONTRACT SNAPSHOT
  module   : gui._21_feed_toggle_enabled_state.toggle_feed_state
  function : toggle_feed(window, fid: str, on: bool) -> None
  imports  : gui._15_feed_config_save_to_disk.save_feeds.save_feeds
            , gui._13_stats_badges_update_live.update_stats_badges.update_stats_badges
  effects  : sets feed["enabled"] = on; calls save_feeds + update_stats_badges
  errors   : None — silently skips if fid not found
"""
# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the recorded CONTRACT of
# gui/_21_feed_toggle_enabled_state/toggle_feed_state.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Search window.feeds for the first feed whose "id" equals fid. If found:
#     - set feed["enabled"] = on
#     - call save_feeds(window)
#     - call update_stats_badges(window)
#   If NO feed matches fid, the function does NOTHING — no mutation, no
#   save, no badge update (silent no-op by contract).
#
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 — Structural: shape-of-the-code checks to catch refactor drift.
# Layer 2 — Behavioral Smoke: fake-window smoke tests that verify the happy
#                              path (enabled state flips, save + stats called)
#                              and the no-op path (unknown fid, nothing happens).
#
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================
# Layer 1 — Structural:
#   test_signature       - exactly three params: "window", "fid", "on"
#                          (all positional-or-keyword, no default), returns
#                          None.
#   test_source_imports  - module-level imports include save_feeds and
#                          update_stats_badges.
#   test_callables       - module exposes ONLY the public symbol
#                          "toggle_feed".
# Layer 2 — Behavioral Smoke:
#   test_sets_enabled_and_calls_save_and_stats - known fid's enabled flag
#                                                flips to the requested bool;
#                                                save + stats each called
#                                                once.
#   test_unknown_fid_is_noop                          - unknown fid causes
#                                                       no mutation and no
#                                                       helper calls.
# ===========================================================================
# WHAT: Verifies the toggle_feed contract survives refactor drift.
# OPTIONS: window with feeds list; fid — feed ID; on — bool
# DEFAULTS: N/A
# OUTPUT/EFFECT: Feed enabled state changed; save_feeds + update_stats_badges called
# ERRORS/EDGE CASES: Unknown fid -> no-op
# HOW TO TEST: toggle_feed(window, "fid", False); check feed.enabled and calls

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
from gui._21_feed_toggle_enabled_state.toggle_feed_state import toggle_feed


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
        """WHAT: Verify toggle_feed accepts exactly three parameters.

        OPTIONS: None — contract is fixed at three parameters: 'window',
                 'fid', and 'on' (all positional-or-keyword, no defaults),
                 returning None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts the signature matches
                       (window, fid, on) -> None.
        ERRORS/EDGE CASES: If the source gains or loses parameters the test
                           fails, flagging refactor drift.
        HOW TO TEST: assert_signature(toggle_feed, [("window", 1, inspect.Parameter.empty),
                                                    ("fid", 1, inspect.Parameter.empty),
                                                    ("on", 1, inspect.Parameter.empty)], None)
        """
        assert_signature(toggle_feed, [("window", 1, inspect.Parameter.empty),
                                       ("fid", 1, inspect.Parameter.empty),
                                       ("on", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verify the source file imports required modules on disk.

        OPTIONS: None — the import set is a hard contract.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts AST-parsed source contains save_feeds and
                       update_stats_badges.
        ERRORS/EDGE CASES: Renaming or removing either import causes failure.
        HOW TO TEST: assert_source_imports(module_path, expected_import_set)
        """
        module_path = str(Path(__file__).resolve().parents[3]
                          / "gui" / "_21_feed_toggle_enabled_state" / "toggle_feed_state.py")
        assert_source_imports(module_path, {
            "gui._15_feed_config_save_to_disk.save_feeds",
            "gui._13_stats_badges_update_live.update_stats_badges",
        })

    def test_callables(self):
        """WHAT: Verify the module exposes exactly one public callable.

        OPTIONS: None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts dir(mod) contains only "toggle_feed" among
                       user-defined callables.
        ERRORS/EDGE CASES: Extra or missing callables indicate drift.
        HOW TO TEST: assert_callables(mod, {"toggle_feed"})
        """
        import gui._21_feed_toggle_enabled_state.toggle_feed_state as mod
        assert_callables(mod, {"toggle_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:
    """Layer 2 — Behavioral smoke tests against a fake window.

    WHAT: Verifies the observable behaviour of toggle_feed: flipping a
         known feed's enabled flag and triggering save + stats update, and
         the no-op path when the fid is unknown.
    OPTIONS: window with feeds list; fid — feed ID; on — bool.
    DEFAULTS: N/A
    OUTPUT/EFFECT: Feed enabled state changed; save_feeds + update_stats_badges called.
    ERRORS/EDGE CASES: Unknown fid -> no-op.
    HOW TO TEST: toggle_feed(window, "fid", False); check feed.enabled and calls.
    """

    def test_sets_enabled_and_calls_save_and_stats(self):
        """WHAT: Verify a known feed's enabled flag flips and helpers fire.

        OPTIONS: window.feeds has two feeds ("a" enabled, "b" enabled);
                 fid = "b", on = False.
        DEFAULTS: None — both fid and on are explicitly set.
        OUTPUT/EFFECT: window.feeds[1]["enabled"] becomes False; save_feeds
                       called once with window; update_stats_badges called
                       once with window.
        ERRORS/EDGE CASES: If the source skips the mutation, save, or stats
                           update the assertion fails.
        HOW TO TEST: Patch save_feeds and update_stats_badges; call toggle_feed;
                     assert feed["enabled"] is False and both mocks called once.
        """
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "enabled": True},
            {"id": "b", "name": "B", "url": "https://b.com/feed", "enabled": True},
        ]
        with patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.save_feeds") as mock_save, \
             patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.update_stats_badges") as mock_stats:
            toggle_feed(window, "b", False)

        assert window.feeds[1]["enabled"] is False
        mock_save.assert_called_once_with(window)
        mock_stats.assert_called_once_with(window)

    def test_unknown_fid_is_noop(self):
        """WHAT: Verify an unknown fid causes no mutation or side effects.

        OPTIONS: window.feeds has one feed with id "a"; fid = "nonexistent",
                 on = False.
        DEFAULTS: None — the unknown fid is intentionally chosen.
        OUTPUT/EFFECT: window.feeds[0]["enabled"] stays True; save_feeds NOT
                       called; update_stats_badges NOT called.
        ERRORS/EDGE CASES: If the source mutates or calls helpers on an unknown
                           fid the test fails.
        HOW TO TEST: Patch save and stats; call toggle_feed; assert state
                     unchanged and both mocks not called.
        """
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "A", "url": "https://a.com/feed", "enabled": True},
        ]
        with patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.save_feeds") as mock_save, \
             patch("gui._21_feed_toggle_enabled_state.toggle_feed_state.update_stats_badges") as mock_stats:
            toggle_feed(window, "nonexistent", False)

        assert window.feeds[0]["enabled"] is True
        mock_save.assert_not_called()
        mock_stats.assert_not_called()
