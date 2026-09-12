"""
==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the add_preset_feed function — the GUI handler that adds a
single preset feed from the Presets Library tab (Tab 4) to the user's active
subscriptions. It:
  - Checks whether the preset is already subscribed (skips if yes)
  - Validates that the preset has a non-empty name and URL
  - Generates a unique feed ID from the name
  - Appends the feed to window.feeds with default settings (12h interval, enabled)
  - Saves the config to disk and refreshes all UI views

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_signature              : add_preset_feed(window, preset) -> None with
                                   exact parameter names, kinds, and return type
  - test_source_imports         : Source imports feed_already_present,
                                   generate_feed_id, append_log_message, save_feeds

Layer 2 (Behavioral):
  - test_adds_valid_preset_to_feeds    : Valid preset → appended with correct
                                          keys; save + refresh called
  - test_skips_already_subscribed      : Already present → skipped, no save/refresh
  - test_empty_name_or_url_is_noop     : Empty name or URL → silent return,
                                          nothing appended

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# importlib.util: Finds the filesystem path of the source module for AST-based
#                 import verification in the structural tests.
import importlib.util

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

# pytest: Test framework; provides the @pytest.fixture decorator for the qapp
#         singleton that all PyQt6 widget tests share.
import pytest
# unittest.mock.MagicMock: Creates fake objects that record every method call,
#                          used to spy on window stub interactions.
# unittest.mock.patch:     Temporarily replaces module attributes with mocks so
#                          we can verify calls without running real code.
from unittest.mock import MagicMock, patch

# offscreen platform required for all PyQt6 widget testing
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform


@pytest.fixture(scope="module")
def qapp():
    """Provide one shared QApplication for the whole module.

    WHAT: Creates a single Qt application object so PyQt6 widgets can be
          constructed in headless (offscreen) mode without a real display.

    OPTIONS: scope="module" — one instance shared by every test in this file.

    DEFAULTS: Qt runs in offscreen mode (no visible window).

    OUTPUT/EFFECT: Yields a QApplication; Qt cleans it up after the tests run.

    ERRORS/EDGE CASES: Creating two QApplication objects in one process crashes
                       Qt, so exactly one is shared at module scope.
    """
    app = QApplication([])
    yield app



def _make_window():
    """Build a minimal WindowStub with an empty feeds list.

    WHAT: Returns a WindowStub (from conftest.py) mimicking the parts of the
          real MainWindow that add_preset_feed touches: window.feeds,
          window.table_presets, and other UI stubs.

    OPTIONS: None.

    DEFAULTS: All stub attributes default to MagicMock. The feeds list is set
              to [] so we can verify append behavior.

    OUTPUT/EFFECT: Returns a configured WindowStub ready for add_preset_feed.

    ERRORS/EDGE CASES: None — MagicMock never raises on attribute access.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.feeds = []
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks.

    These tests inspect the source code's structure without running the GUI.
    They fail if add_preset_feed's signature or imports drift from the contract.
    """

    def test_signature(self):
        """Layer 1 — exact signature check.

        WHAT: Confirms add_preset_feed takes exactly two required parameters
              named "window" and "preset" and declares a return type of None.

        WHY SIGNATURE MATTERS:
          Every caller uses: add_preset_feed(window, preset)
          If the parameter count or name changed, all callers break with TypeError.

        OPTIONS:
          - Parameter "window": POSITIONAL_OR_KEYWORD, no default, no type hint
          - Parameter "preset": POSITIONAL_OR_KEYWORD, no default, no type hint
          - Return type: annotated None

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when the signature matches exactly.

        ERRORS/EDGE CASES:
          - Wrong parameter name/kind/default: params mismatch assertion fails
          - Missing return annotation: return_annotation != None fails

        HOW TO TEST: Change the parameter name from "preset" to "feed_data" in
                     the source, then run — it should fail with a params mismatch.
        """
        import inspect
        from gui._32_preset_add_single_from_catalog.add_preset_feed import (
            add_preset_feed,
        )
        sig = inspect.signature(add_preset_feed)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [
            ("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
            ("preset", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Layer 1 — source import check.

        WHAT: Verifies the source file imports all four collaborators needed
              by add_preset_feed:
          - feed_already_present   (dedup check)
          - generate_feed_id       (unique ID generation)
          - append_log_message     (log output)
          - save_feeds             (persist to disk)

        WHY THESE IMPORTS:
          Without any one of these, add_preset_feed cannot complete its job.
          Removing or renaming an import would cause an ImportError at runtime.

        OPTIONS: Expected set is exactly the four modules listed above.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when all four imports exist in the source.

        ERRORS/EDGE CASES:
          - Missing import: "Missing imports: [...]" naming the module

        HOW TO TEST: Rename one import path in the source, then run —
                     it should fail and name the missing module.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._32_preset_add_single_from_catalog.add_preset_feed"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {
                "features.feature_feed_presets_library.implementation.feeds_presets",
                "gui._09_feed_identifier_generate_from_name.generate_feed_id",
                "gui._10_log_append_timestamped_message.append_timestamped_log",
                "gui._15_feed_config_save_to_disk.save_feeds",
            },
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real add_preset_feed function.

    These tests call the REAL add_preset_feed against a fake window while
    verifying that feeds are appended correctly, saves and refreshes are called,
    and edge cases (already subscribed, empty name/URL) are handled properly.
    """

    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.feed_already_present", return_value=False)
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.generate_feed_id", return_value="feed_a")
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.save_feeds")
    @patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_window")
    @patch("gui._31_presets_table_refresh_view.refresh_presets_table.refresh_presets_table")
    def test_adds_valid_preset_to_feeds(self, mock_refresh_presets, mock_refresh_win, mock_save,
                                         mock_gen_id, mock_already, qapp):
        """Layer 2 — valid preset appended with correct defaults; save + refresh called.

        WHAT: When a preset with a valid name and URL is passed, it must be
              appended to window.feeds with the correct structure (id, name, url,
              category, fetch_interval_hours=12, enabled=True), then saved and
              both window and presets table refreshed.

        WHY MOCK feed_already_present=False:
          We want to test the happy path (not already subscribed), so we force
          the dedup check to return False so the preset gets added.

        WHY MOCK generate_feed_id="feed_a":
          We verify the generated ID is "feed_a" to confirm the ID function
          is called and its return value is used correctly.

        OPTIONS:
          - preset: {"name": "TechCrunch", "url": "...", "category": "Technology"}
          - All downstream functions are mocked to record calls only

        DEFAULTS: fetch_interval_hours=12, enabled=True (set by the source).

        OUTPUT/EFFECT:
          - w.feeds has 1 entry with all expected keys
          - save_feeds(w) called once
          - refresh_window(w) called once
          - refresh_presets_table(w) called once

        ERRORS/EDGE CASES:
          - Wrong feed structure: key assertion fails
          - Save not called: mock_save.assert_called_once_with(w) fails
          - Refresh not called: mock_refresh_* assertions fail

        HOW TO TEST: Remove the window.feeds.append call from the source, then
                     run — the len(w.feeds) == 1 assertion should fail.
        """
        from gui._32_preset_add_single_from_catalog.add_preset_feed import (
            add_preset_feed,
        )
        w = _make_window()
        preset = {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"}
        add_preset_feed(w, preset)
        assert len(w.feeds) == 1
        entry = w.feeds[0]
        assert entry["name"] == "TechCrunch"
        assert entry["url"] == "https://techcrunch.com/feed/"
        assert entry["category"] == "Technology"
        assert entry["fetch_interval_hours"] == 12
        assert entry["enabled"] is True
        assert entry["id"] == "feed_a"
        mock_save.assert_called_once_with(w)
        mock_refresh_win.assert_called_once_with(w)
        mock_refresh_presets.assert_called_once_with(w)

    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.feed_already_present", return_value=True)
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.generate_feed_id")
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.save_feeds")
    def test_skips_already_subscribed(self, mock_save, mock_gen_id, mock_already, qapp):
        """Layer 2 — already subscribed preset is skipped silently.

        WHAT: When feed_already_present returns True (the preset is already in
              window.feeds), add_preset_feed must return immediately without
              modifying feeds, generating an ID, or saving.

        WHY SKIP:
          Duplicate subscriptions waste network resources and confuse the user.
          The function logs a message (not tested here) and exits early.

        OPTIONS:
          - mock_already returns True to simulate an existing subscription
          - mock_gen_id and mock_save record whether they were called

        DEFAULTS: N/A.

        OUTPUT/EFFECT:
          - w.feeds remains empty (len == 0)
          - save_feeds NOT called
          - generate_feed_id NOT called

        ERRORS/EDGE CASES:
          - Feed added anyway: len(w.feeds) == 0 assertion fails
          - Save called despite skip: mock_save.assert_not_called() fails

        HOW TO TEST: Remove the early return after the feed_already_present check
                     in the source, then run — the feed should be incorrectly added.
        """
        from gui._32_preset_add_single_from_catalog.add_preset_feed import (
            add_preset_feed,
        )
        w = _make_window()
        preset = {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"}
        add_preset_feed(w, preset)
        assert len(w.feeds) == 0
        mock_save.assert_not_called()
        mock_gen_id.assert_not_called()

    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.feed_already_present")
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.generate_feed_id")
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.save_feeds")
    def test_empty_name_or_url_is_noop(self, mock_save, mock_gen_id, mock_already, qapp):
        """Layer 2 — empty name or empty URL causes silent no-op.

        WHAT: When the preset has an empty name OR an empty URL (after stripping),
              add_preset_feed must return immediately without appending anything,
              generating an ID, or saving.

        WHY VALIDATE:
          A feed with no name or no URL is unusable. Silently skipping invalid
          presets prevents broken entries from polluting the subscriptions list.

        OPTIONS:
          - First call: empty name, valid URL
          - Second call: valid name, empty URL
          - Both should result in zero feeds added

        DEFAULTS: N/A.

        OUTPUT/EFFECT:
          - w.feeds remains empty after both calls (len == 0)
          - save_feeds NOT called
          - generate_feed_id NOT called

        ERRORS/EDGE CASES:
          - Feed added despite empty field: len(w.feeds) == 0 fails
          - Save called on invalid input: mock_save.assert_not_called() fails

        HOW TO TEST: Remove the empty-name/URL guard clause from the source, then
                     run — the invalid presets should be incorrectly added.
        """
        from gui._32_preset_add_single_from_catalog.add_preset_feed import (
            add_preset_feed,
        )
        w = _make_window()
        add_preset_feed(w, {"name": "", "url": "https://example.com", "category": "Tech"})
        assert len(w.feeds) == 0
        mock_save.assert_not_called()
        add_preset_feed(w, {"name": "Test", "url": "", "category": "Tech"})
        assert len(w.feeds) == 0
