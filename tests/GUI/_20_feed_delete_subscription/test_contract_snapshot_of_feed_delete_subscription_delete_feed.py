"""Contract-drift tests for gui/_20_feed_delete_subscription/delete_feed_subscription.py

CONTRACT SNAPSHOT
  module   : gui._20_feed_delete_subscription.delete_feed_subscription
  function : delete_feed(window, fid: str) -> None
  imports  : gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
            , gui._15_feed_config_save_to_disk.save_feeds.save_feeds
            , gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_window
  effects  : removes matching feed; calls save_feeds + refresh_window
  errors   : None — silently skips if fid not found
"""
# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the recorded CONTRACT of
# gui/_20_feed_delete_subscription/delete_feed_subscription.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Search window.feeds for the first feed whose "id" equals fid. If found:
#     - remember its name
#   - remove it with window.feeds.pop(index)
#   - save the list to disk (save_feeds)
#   - refresh every UI view (refresh_window, imported lazily inside the func)
#   - append an "Unsubscribed feed: <name>" log message
#   - return
#   If NO feed matches fid, the function does NOTHING — no save, no refresh,
#   no crash (it just falls out of the loop and returns quietly).
#
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 — Structural: shape-of-the-code checks to catch refactor drift.
# Layer 2 — Behavioral Smoke: fake-window smoke tests that verify the happy
#                              path (feed removed, save + refresh called) and
#                              the no-op path (unknown fid, nothing happens).
#
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================
# Layer 1 — Structural:
#   test_signature       - exactly two params: "window" and "fid"
#                          (both positional-or-keyword, no default), returns
#                          None.
#   test_source_imports  - module-level imports include append_log_message
#                          and save_feeds (refresh_window is lazy, not at
#                          module level).
#   test_callables       - module exposes ONLY the public symbol
#                          "delete_feed".
# Layer 2 — Behavioral Smoke:
#   test_removes_matching_feed_and_calls_save_refresh - known fid is removed
#                                                       from window.feeds;
#                                                       save + refresh are
#                                                       each called once.
#   test_unknown_fid_is_noop                          - unknown fid causes
#                                                       no change; save and
#                                                       refresh are NOT called.
# ===========================================================================
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
# SOURCE BEHAVIOUR (the contract being locked in):
#   Search window.feeds for the first feed whose "id" equals fid. If found:
#     - remember its name
#   - remove it with window.feeds.pop(index)
#   - save the list to disk (save_feeds)
#   - refresh every UI view (refresh_window, imported lazily inside the func)
#   - append an "Unsubscribed feed: <name>" log message
#   - return
#   If NO feed matches fid, the function does NOTHING — no save, no refresh,
#   no crash (it just falls out of the loop and returns quietly).
# OPTIONS: window with a feeds list; fid — the feed ID string to remove.
# DEFAULTS: N/A — both parameters are required.
# OUTPUT/EFFECT: matching feed removed; save + refresh triggered; log appended.
# ERRORS/EDGE CASES: unknown fid -> a no-op (nothing saved, nothing refreshed).
# HOW TO TEST: delete_feed(window, "some-fid"); then assert the feed is gone.

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
# Plant fake PyQt6 packages before any real import so no screen is needed.
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
# Import the REAL source function being guarded.
from gui._20_feed_delete_subscription.delete_feed_subscription import delete_feed


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================
# Shape-of-the-code checks to catch refactor drift. The separator bars below
# are the file's original formatting and are kept verbatim.

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
        """WHAT: Verify delete_feed accepts exactly two parameters.

        OPTIONS: None — contract is fixed at two parameters: 'window' and
                 'fid' (both positional-or-keyword, no defaults), returning
                 None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts the signature matches
                       (window, fid) -> None.
        ERRORS/EDGE CASES: If the source gains or loses parameters the test
                           fails, flagging refactor drift.
        HOW TO TEST: assert_signature(delete_feed, [("window", 1, inspect.Parameter.empty),
                                                    ("fid", 1, inspect.Parameter.empty)], None)
        """
        # Contract: TWO parameters —
        #   "window" (kind 1 = positional-or-keyword, no default) and
        #   "fid"    (kind 1 = positional-or-keyword, no default),
        # returning None. (The source page types fid as str but does not
        # annotate the return value.)
        assert_signature(delete_feed, [("window", 1, inspect.Parameter.empty),
                                       ("fid", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verify the source file imports required modules on disk.

        OPTIONS: None — the import set is a hard contract.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts AST-parsed source contains append_log_message
                       and save_feeds. NOTE: refresh_window is imported
                       LAZILY inside the function body so it is intentionally
                       NOT required at module level.
        ERRORS/EDGE CASES: Renaming or removing either required import causes
                           failure.
        HOW TO TEST: assert_source_imports(module_path, expected_import_set)
        """
        # Point at the real source file on disk.
        module_path = str(Path(__file__).resolve().parents[3]
                          / "gui" / "_20_feed_delete_subscription" / "delete_feed_subscription.py")
        # The source's MODULE-LEVEL imports must be the log module (for
        # append_log_message) and the save module (for save_feeds). NOTE:
        # refresh_window is imported LAZY — inside the function body — so it
        # is intentionally NOT required here at module level.
        assert_source_imports(module_path, {
            "gui._10_log_append_timestamped_message.append_timestamped_log",
            "gui._15_feed_config_save_to_disk.save_feeds",
        })

    def test_callables(self):
        """WHAT: Verify the module exposes exactly one public callable.

        OPTIONS: None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts dir(mod) contains only "delete_feed" among
                       user-defined callables.
        ERRORS/EDGE CASES: Extra or missing callables indicate drift.
        HOW TO TEST: assert_callables(mod, {"delete_feed"})
        """
        # The module must define EXACTLY the public function "delete_feed".
        import gui._20_feed_delete_subscription.delete_feed_subscription as mod
        assert_callables(mod, {"delete_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests run delete_feed against a fake window with recording fakes in
# place of save_feeds / refresh_window / append_log_message, and check both
# the happy path (a feed is removed) and the no-op path (unknown id).

class TestLayer2Behavioral:
    """Layer 2 — Behavioral smoke tests against a fake window.

    WHAT: Verifies the observable behaviour of delete_feed: removing a
         known feed and triggering save+refresh, and the no-op path when
         the fid is unknown.
    OPTIONS: window with a feeds list; fid — the feed ID string to remove.
    DEFAULTS: N/A — both parameters are required.
    OUTPUT/EFFECT: Matching feed removed; save + refresh triggered; log appended.
    ERRORS/EDGE CASES: unknown fid -> a no-op (nothing saved, nothing refreshed).
    HOW TO TEST: delete_feed(window, "some-fid"); then assert the feed is gone.
    """

    def test_removes_matching_feed_and_calls_save_refresh(self):
        """WHAT: Verify a known feed is removed and persistence is triggered.

        OPTIONS: window.feeds contains three feeds with ids "a", "b", "c";
                 fid = "b".
        DEFAULTS: None — the target feed is explicitly chosen.
        OUTPUT/EFFECT: window.feeds shrinks from 3 to 2; "b" is absent from
                       the remaining list; save_feeds called once with window;
                       refresh_window called once with window.
        ERRORS/EDGE CASES: If the source fails to remove the feed, skips save,
                           or skips refresh the assertion fails.
        HOW TO TEST: Patch save_feeds and refresh_window; call delete_feed;
                     assert len(feeds)==2, feed "b" absent, and mock counts.
        """
        # Fake window holding three feeds with ids "a", "b", "c".
        window = WindowStub()
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
            {"id": "b", "name": "Feed B", "url": "https://b.com/feed"},
            {"id": "c", "name": "Feed C", "url": "https://c.com/feed"},
        ]
        # Replace the helpers: save_feeds, refresh_window (note: refresh_window
        # is imported inside the source function, so we patch it at the same
        # module namespace), and append_log_message — all with recorders.
        with patch("gui._20_feed_delete_subscription.delete_feed_subscription.save_feeds") as mock_save, \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_window") as mock_refresh, \
             patch("gui._20_feed_delete_subscription.delete_feed_subscription.append_log_message"):
            # Ask to delete the feed whose id is "b".
            delete_feed(window, "b")

        # The list shrank from 3 to 2 feeds...
        assert len(window.feeds) == 2
        # ...and the deleted feed ("b") is gone from every remaining entry.
        assert all(f["id"] != "b" for f in window.feeds)
        # Because a deletion happened, the config was saved once...
        mock_save.assert_called_once_with(window)
        # ...and the whole UI was refreshed once (tables + badges rebuild).
        mock_refresh.assert_called_once_with(window)

    def test_unknown_fid_is_noop(self):
        """WHAT: Verify an unknown fid causes no side effects.

        OPTIONS: window.feeds contains one feed with id "a"; fid = "nonexistent".
        DEFAULTS: None — the unknown fid is intentionally chosen.
        OUTPUT/EFFECT: window.feeds length unchanged; save_feeds NOT called;
                       refresh_window NOT called.
        ERRORS/EDGE CASES: If the source crashes or mutates state on an unknown
                           fid the test fails.
        HOW TO TEST: Patch save and refresh; call delete_feed; assert length
                     unchanged and both mocks not called.
        """
        window = WindowStub()
        # One feed with id "a".
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
        ]
        # Remember how many feeds existed before the call.
        original_len = len(window.feeds)
        # Replace the helpers with recorders (nothing should be triggered).
        with patch("gui._20_feed_delete_subscription.delete_feed_subscription.save_feeds") as mock_save, \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_window") as mock_refresh:
            # Ask to delete a feed id that does NOT exist anywhere in the list.
            delete_feed(window, "nonexistent")

        # The number of feeds is unchanged (nothing was removed).
        assert len(window.feeds) == original_len
        # Nothing was saved...
        mock_save.assert_not_called()
        # ...and nothing was refreshed: the loop simply found no match and the
        # function returned quietly (silent no-op by contract).
        mock_refresh.assert_not_called()
