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
# WHAT: This file protects the recorded CONTRACT of
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

    def test_signature(self):
        # Contract: TWO parameters —
        #   "window" (kind 1 = positional-or-keyword, no default) and
        #   "fid"    (kind 1 = positional-or-keyword, no default),
        # returning None. (The source page types fid as str but does not
        # annotate the return value.)
        assert_signature(delete_feed, [("window", 1, inspect.Parameter.empty),
                                       ("fid", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        # Point at the real source file on disk.
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_20_feed_delete_subscription" / "delete_feed_subscription.py")
        # The source's MODULE-LEVEL imports must be the log module (for
        # append_log_message) and the save module (for save_feeds). NOTE:
        # refresh_window is imported LAZILY — inside the function body — so it
        # is intentionally NOT required here at module level.
        assert_source_imports(module_path, {
            "gui._10_log_append_timestamped_message.append_timestamped_log",
            "gui._15_feed_config_save_to_disk.save_feeds",
        })

    def test_callables(self):
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

    def test_removes_matching_feed_and_calls_save_refresh(self):
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
             patch("gui._20_feed_delete_subscription.delete_feed_subscription.refresh_window") as mock_refresh, \
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
        window = WindowStub()
        # One feed with id "a".
        window.feeds = [
            {"id": "a", "name": "Feed A", "url": "https://a.com/feed"},
        ]
        # Remember how many feeds existed before the call.
        original_len = len(window.feeds)
        # Replace the helpers with recorders (nothing should be triggered).
        with patch("gui._20_feed_delete_subscription.delete_feed_subscription.save_feeds") as mock_save, \
             patch("gui._20_feed_delete_subscription.delete_feed_subscription.refresh_window") as mock_refresh:
            # Ask to delete a feed id that does NOT exist anywhere in the list.
            delete_feed(window, "nonexistent")

        # The number of feeds is unchanged (nothing was removed).
        assert len(window.feeds) == original_len
        # Nothing was saved...
        mock_save.assert_not_called()
        # ...and nothing was refreshed: the loop simply found no match and the
        # function returned quietly (silent no-op by contract).
        mock_refresh.assert_not_called()