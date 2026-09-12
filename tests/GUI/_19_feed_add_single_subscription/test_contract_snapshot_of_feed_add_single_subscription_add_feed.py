"""Contract-drift tests for gui/_19_feed_add_single_subscription/add_feed_subscription.py

CONTRACT SNAPSHOT
  module   : gui._19_feed_add_single_subscription.add_feed_subscription
  function : add_feed(window) -> None
  imports  : PyQt6.QtWidgets.QMessageBox
            , gui._09_feed_identifier_generate_from_name.generate_feed_id
            , gui._10_log_append_timestamped_message.append_timestamped_log
            , gui._15_feed_config_save_to_disk.save_feeds
            , gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_window
  effects  : validates; appends feed dict; calls save_feeds + refresh_window
  errors   : missing name/url → QMessageBox.warning; duplicate URL → logged
"""
# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the recorded CONTRACT of
# gui/_19_feed_add_single_subscription/add_feed_subscription.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Reads the drawer form: in_name, in_url, in_cat (defaults to "General"),
#   cb_freq (index maps to hours via [1,3,6,12,24]).
#   Validation:
#     - empty name OR url -> QMessageBox.warning popup, add aborted
#     - url without "http" prefix -> gets "https://" prepended
#     - url that already exists in window.feeds (trailing "/" ignored) ->
#       only a log message, NO duplicate appended
#   On success: generates a feed id, appends a feed dict with EXACT keys
#   (id, name, url, category, fetch_interval_hours, enabled), calls
#   save_feeds(window) + refresh_window(window), logs a success message, and
#   clears the name/url inputs.
#
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 — Structural: shape-of-the-code checks to catch refactor drift.
# Layer 2 — Behavioral Smoke: fake-window smoke tests that verify validation
#                              paths, feed-dict construction, duplicate
#                              detection, URL scheme normalization, and the
#                              index-to-hours mapping are all preserved.
#
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================
# Layer 1 — Structural:
#   test_signature       - exactly one param "window" (positional-or-keyword),
#                          no default, returns None.
#   test_source_imports  - module-level imports include QMessageBox,
#                          generate_feed_id, append_log_message, save_feeds,
#                          and refresh_window.
#   test_callables       - module exposes ONLY the public symbol "add_feed".
# Layer 2 — Behavioral Smoke:
#   test_missing_name_or_url_shows_warning             - empty name triggers
#                                                        QMessageBox.warning.
#   test_valid_feed_appended_with_exact_keys           - valid form produces
#                                                        a feed dict with
#                                                        all six required keys
#                                                        and correct values;
#                                                        save + refresh are
#                                                        called once; inputs
#                                                        are cleared.
#   test_url_gets_https_prefix_when_scheme_less        - bare domain URL gets
#                                                        "https://" prepended.
#   test_duplicate_url_not_appended                    - existing URL is
#                                                        rejected; save/refresh
#                                                        NOT called; log IS
#                                                        called.
#   test_duplicate_url_trailing_slash_normalized       - trailing-slash URL
#                                                        matches existing
#                                                        non-slash URL;
#                                                        duplicate detected.
#   test_interval_index_maps_correctly                 - cb_freq index 4 maps
#                                                        to 24 hours via
#                                                        [1,3,6,12,24].
# ===========================================================================
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
# SOURCE BEHAVIOUR (the contract being locked in):
#   Reads the drawer form: in_name, in_url, in_cat (defaults to "General"),
#   cb_freq (index maps to hours via [1,3,6,12,24]).
#   Validation:
#     - empty name OR url -> QMessageBox.warning popup, add aborted
#     - url without "http" prefix -> gets "https://" prepended
#     - url that already exists in window.feeds (trailing "/" ignored) ->
#       only a log message, NO duplicate appended
#   On success: generates a feed id, appends a feed dict with EXACT keys
#   (id, name, url, category, fetch_interval_hours, enabled), calls
#   save_feeds(window) + refresh_window(window), logs a success message, and
#   clears the name/url inputs.
# OPTIONS: window must expose in_name, in_url, in_cat, cb_freq, feeds.
# DEFAULTS: category = "General"; interval from cb_freq index via [1,3,6,12,24].
# OUTPUT/EFFECT: new feed dict appended; save + refresh called; inputs cleared.
# ERRORS/EDGE CASES: missing fields -> warning popup; duplicate URL -> log.
# HOW TO TEST: fill the form fields, call add_feed(window), inspect feeds list.

# sys = runtime controls; plants fake PyQt6 modules and extends import path.
import sys
# inspect = reads a function's declared parameters without running it.
import inspect
# Path = readable file-system paths.
from pathlib import Path
# MagicMock = fake call-recording object; patch = swap a name temporarily;
# call = an object that DESCRIBES one function call (arg tuple + kwargs dict),
# useful with mock.assert_has_calls / call_args_list.
from unittest.mock import MagicMock, patch, call

# pytest = the test runner.
import pytest

# Ensure offscreen platform for headless Qt rendering
# Plant fake PyQt6 packages before any real import so no screen is needed.
# QMessageBox (the popup dialog) is one of the things mocked out: the tests
# check that .warning is *called*, never that a real dialog appears.
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
from gui._19_feed_add_single_subscription.add_feed_subscription import add_feed


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
        """WHAT: Verify add_feed accepts exactly one parameter.

        OPTIONS: None — contract is fixed at one parameter named 'window'.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts the signature is
                       (window: POSITIONAL_OR_KEYWORD, no default) -> None.
        ERRORS/EDGE CASES: If the source gains or loses parameters the test
                           fails, flagging refactor drift.
        HOW TO TEST: assert_signature(add_feed, [("window", 1, inspect.Parameter.empty)], None)
        """
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, returns None.
        assert_signature(add_feed, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verify the source file imports required modules on disk.

        OPTIONS: None — the import set is a hard contract.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts AST-parsed source contains QMessageBox,
                       generate_feed_id, append_log_message, save_feeds,
                       and refresh_window.
        ERRORS/EDGE CASES: Renaming or removing any import causes failure.
        HOW TO TEST: assert_source_imports(module_path, expected_import_set)
        """
        # Point at the real source file on disk.
        module_path = str(Path(__file__).resolve().parents[3]
                          / "gui" / "_19_feed_add_single_subscription" / "add_feed_subscription.py")
        # The source MUST import PyQt6.QtWidgets (the QMessageBox popup) plus
        # the four gui modules it depends on (id generator, log, save, refresh).
        assert_source_imports(module_path, {
            "PyQt6.QtWidgets",
            "gui._09_feed_identifier_generate_from_name.generate_feed_id",
            "gui._10_log_append_timestamped_message.append_timestamped_log",
            "gui._15_feed_config_save_to_disk.save_feeds",
            "gui._16_refresh_all_views_pipeline.refresh_all_views",
        })

    def test_callables(self):
        """WHAT: Verify the module exposes exactly one public callable.

        OPTIONS: None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts dir(mod) contains only "add_feed" among
                       user-defined callables.
        ERRORS/EDGE CASES: Extra or missing callables indicate drift.
        HOW TO TEST: assert_callables(mod, {"add_feed"})
        """
        # The module must define EXACTLY the public function "add_feed".
        import gui._19_feed_add_single_subscription.add_feed_subscription as mod
        assert_callables(mod, {"add_feed"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests run add_feed with fake form inputs (MagicMocks supply .text()
# / .currentIndex() values) and replace the helper functions (QMessageBox,
# save_feeds, refresh_window, append_log_message, generate_feed_id) with
# recording fakes, then inspect what was appended/ called.

class TestLayer2Behavioral:
    """Layer 2 — Behavioral smoke tests against a fake window.

    WHAT: Verifies the observable behaviour of add_feed: validation paths,
         feed-dict construction, duplicate detection, URL normalization, and
         the index-to-hours interval mapping.
    OPTIONS: window must expose in_name, in_url, in_cat, cb_freq, feeds.
    DEFAULTS: category defaults to "General"; interval derived from cb_freq
              index via [1,3,6,12,24].
    OUTPUT/EFFECT: Feed dict appended; save_feeds + refresh_window called;
                   inputs cleared on success.
    ERRORS/EDGE CASES: Missing name/url -> warning popup; duplicate URL ->
                       silent log, no append.
    HOW TO TEST: fill form fields, call add_feed(window), inspect feeds list.
    """

    def test_missing_name_or_url_shows_warning(self):
        """WHAT: Verify empty name triggers QMessageBox.warning.

        OPTIONS: window.in_name.text() returns ""; window.in_url.text() returns
                 a valid URL.
        DEFAULTS: None — the name is intentionally empty to trigger the error
                  branch.
        OUTPUT/EFFECT: QMessageBox.warning is called exactly once (the
                       validation branch fires and aborts the add).
        ERRORS/EDGE CASES: If the source drops the empty-name check or calls
                           warning more/less than once this test fails.
        HOW TO TEST: Patch QMessageBox.warning; call add_feed(window); assert
                     mock_warn.assert_called_once().
        """
        window = WindowStub()
        # The NAME input is empty (MagicMock returns ""), the URL has text.
        window.in_name.text.return_value = ""
        window.in_url.text.return_value = "https://example.com/feed"
        # Replace QMessageBox.warning in the source module with a recording fake
        # so no real popup dialog is shown (it would hang a headless test).
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.QMessageBox.warning") as mock_warn:
            add_feed(window)
            # The validation branch ("not name") must have triggered a warning
            # popup exactly once.
            mock_warn.assert_called_once()

    def test_valid_feed_appended_with_exact_keys(self):
        """WHAT: Verify a valid form produces a correctly keyed feed dict.

        OPTIONS: in_name="TechCrunch", in_url="https://techcrunch.com/feed",
                 in_cat="Technology", cb_freq.currentIndex()=2.
        DEFAULTS: None — all form fields are explicitly set.
        OUTPUT/EFFECT: window.feeds grows by one dict with keys {id, name,
                       url, category, fetch_interval_hours, enabled};
                       save_feeds and refresh_window each called once;
                       in_name and in_url are cleared.
        ERRORS/EDGE CASES: Wrong key count, wrong interval value, or missing
                           save/refresh calls indicate drift.
        HOW TO TEST: Patch helpers; call add_feed; assert feed dict equality,
                     mock call counts, and input clears.
        """
        window = WindowStub()
        # Fill the fake form: name "TechCrunch", URL with http-prefix, category
        # "Technology", frequency dropdown index 2 (= the 3rd option, 6h).
        window.in_name.text.return_value = "TechCrunch"
        window.in_url.text.return_value = "https://techcrunch.com/feed"
        window.in_cat.text.return_value = "Technology"
        window.cb_freq.currentIndex.return_value = 2
        window.feeds = []        # start from an empty subscription list
        # Replace helpers: generate_feed_id returns a STABLE id "techcrunch";
        # save_feeds / refresh_window / append_log_message become recorders.
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.generate_feed_id",
                   return_value="techcrunch") as mock_gid, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds") as mock_save, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window") as mock_refresh, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message"):
            add_feed(window)

        # Exactly one feed must have been appended.
        assert len(window.feeds) == 1
        feed = window.feeds[0]
        # And that dict must have EXACTLY these six keys and values:
        #   id                    = the generated id "techcrunch"
        #   name                  = "TechCrunch"
        #   url                   = "https://techcrunch.com/feed" (already https)
        #   category              = "Technology" (given, not the default)
        #   fetch_interval_hours  = 6   (cb_freq index 2 -> [1,3,6,12,24][2])
        #   enabled               = True (turned on by default)
        assert feed == {
            "id": "techcrunch",
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed",
            "category": "Technology",
            "fetch_interval_hours": 6,
            "enabled": True,
        }
        # The persisted save + UI refresh must each have been triggered once.
        mock_save.assert_called_once_with(window)
        mock_refresh.assert_called_once_with(window)
        # After success the name and URL input boxes are cleared once each.
        window.in_name.clear.assert_called_once()
        window.in_url.clear.assert_called_once()

    def test_url_gets_https_prefix_when_scheme_less(self):
        """WHAT: Verify bare-domain URLs get 'https://' prepended.

        OPTIONS: in_name="Example", in_url="example.com/feed" (no scheme),
                 in_cat="" (empty -> falls back to default "General"),
                 cb_freq.currentIndex()=3.
        DEFAULTS: category falls back to "General" when empty.
        OUTPUT/EFFECT: window.feeds[0]["url"] == "https://example.com/feed".
        ERRORS/EDGE CASES: If the source does not prepend the scheme the
                           assertion fails.
        HOW TO TEST: Call add_feed; assert window.feeds[0]["url"] starts with
                     "https://".
        """
        window = WindowStub()
        # The user typed a URL WITHOUT any "http" prefix ("example.com/feed").
        window.in_name.text.return_value = "Example"
        window.in_url.text.return_value = "example.com/feed"
        # Category left empty -> must fall back to the default "General".
        window.in_cat.text.return_value = ""
        window.cb_freq.currentIndex.return_value = 3   # index 3 -> 12 hours
        window.feeds = []
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.generate_feed_id",
                   return_value="example"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message"):
            add_feed(window)

        # The source prepended "https://" to the scheme-less URL.
        assert window.feeds[0]["url"] == "https://example.com/feed"

    def test_duplicate_url_not_appended(self):
        """WHAT: Verify a duplicate URL is rejected without appending.

        OPTIONS: in_name="Duplicate", in_url="https://duplicate.com/feed",
                 in_cat="Tech", cb_freq.currentIndex()=0.
                 window.feeds already contains the same URL.
        DEFAULTS: None — the duplicate is pre-loaded into window.feeds.
        OUTPUT/EFFECT: window.feeds stays at length 1; save_feeds NOT called;
                       refresh_window NOT called; append_log_message IS called
                       once (the "already subscribed" log).
        ERRORS/EDGE CASES: If the source appends the duplicate or skips the
                           log the test fails.
        HOW TO TEST: Call add_feed; assert len(feeds)==1 and mock counts.
        """
        window = WindowStub()
        window.in_name.text.return_value = "Duplicate"
        # The same URL the window already subscribes to.
        window.in_url.text.return_value = "https://duplicate.com/feed"
        window.in_cat.text.return_value = "Tech"
        window.cb_freq.currentIndex.return_value = 0   # index 0 -> 1 hour
        # The existing feed list already contains ONE feed with the same URL.
        window.feeds = [{"id": "x", "name": "Existing", "url": "https://duplicate.com/feed",
                        "enabled": True}]
        # Patch save/refresh/log (NOT generate_feed_id — that branch is never
        # reached, because the duplicate check runs BEFORE id generation).
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds") as mock_save, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window") as mock_refresh, \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message") as mock_log:
            add_feed(window)

        # No duplicate was appended: still exactly 1 feed.
        assert len(window.feeds) == 1
        # Because nothing changed, nothing was saved...
        mock_save.assert_not_called()
        # ...and nothing was refreshed (the table didn't need rebuilding)...
        mock_refresh.assert_not_called()
        # ...but a log message was appended exactly once, explaining that the
        # feed is already subscribed.
        mock_log.assert_called_once()

    def test_duplicate_url_trailing_slash_normalized(self):
        """WHAT: Verify trailing-slash URLs are normalized before dedup check.

        OPTIONS: in_name="Dup", in_url="https://dup.com/feed/" (with trailing
                 slash), in_cat="Tech", cb_freq.currentIndex()=0.
                 window.feeds contains "https://dup.com/feed" (no slash).
        DEFAULTS: The source strips trailing slashes on BOTH sides before
                  comparing.
        OUTPUT/EFFECT: window.feeds stays at length 1; append_log_message
                       called once (the duplicate warning).
        ERRORS/EDGE CASES: If the source does not normalize slashes the
                           duplicate is missed and the feed is appended.
        HOW TO TEST: Call add_feed; assert len(feeds)==1 and mock_log called.
        """
        window = WindowStub()
        window.in_name.text.return_value = "Dup"
        # Notice the TRAILING SLASH on this URL: "https://dup.com/feed/" vs the
        # existing feed's "https://dup.com/feed". The source strips trailing
        # slashes on BOTH sides before comparing, so these count as equal.
        window.in_url.text.return_value = "https://dup.com/feed/"
        window.in_cat.text.return_value = "Tech"
        window.cb_freq.currentIndex.return_value = 0
        # The existing feed has the SAME URL but WITHOUT the trailing slash.
        window.feeds = [{"id": "x", "name": "X", "url": "https://dup.com/feed",
                        "enabled": True}]
        # Only the log is patched here — save/refresh would directly reveal a
        # duplicate append, but we assert on the log call instead.
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message") as mock_log:
            add_feed(window)
        # Still exactly one feed (no duplicate appended thanks to slash-normalization).
        assert len(window.feeds) == 1
        # The "already subscribed" message was logged exactly once.
        mock_log.assert_called_once()

    def test_interval_index_maps_correctly(self):
        """WHAT: Verify cb_freq index maps to the correct hour value.

        OPTIONS: in_name="F", in_url="https://f.com/feed", in_cat="G",
                 cb_freq.currentIndex()=4.
        DEFAULTS: The index-to-hours mapping is [1, 3, 6, 12, 24]; index 4
                  maps to 24 hours.
        OUTPUT/EFFECT: window.feeds[0]["fetch_interval_hours"] == 24.
        ERRORS/EDGE CASES: If the source changes the mapping list or reads the
                           wrong index this test fails.
        HOW TO TEST: Call add_feed; assert the interval value equals 24.
        """
        window = WindowStub()
        window.in_name.text.return_value = "F"
        window.in_url.text.return_value = "https://f.com/feed"
        window.in_cat.text.return_value = "G"
        # Frequency dropdown index 4 = the FIFTH option.
        window.cb_freq.currentIndex.return_value = 4
        window.feeds = []
        with patch("gui._19_feed_add_single_subscription.add_feed_subscription.generate_feed_id",
                   return_value="f"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.save_feeds"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.refresh_window"), \
             patch("gui._19_feed_add_single_subscription.add_feed_subscription.append_log_message"):
            add_feed(window)

        # The source reads hours from the list [1, 3, 6, 12, 24] at the chosen
        # index: index 4 -> 24 hours. This locks the index-to-hours mapping.
        assert window.feeds[0]["fetch_interval_hours"] == 24
