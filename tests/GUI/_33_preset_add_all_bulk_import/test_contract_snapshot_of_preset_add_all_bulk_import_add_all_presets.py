"""
==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the add_all_presets function — the GUI handler that bulk-imports
all unsubscribed preset feeds from the Presets Library into the user's active
subscriptions. It:
  - Iterates through every preset feed from the library
  - Skips presets that are already subscribed (dedup by URL or name)
  - Skips presets with empty names or empty URLs
  - Adds valid new presets with default settings (12h interval, enabled)
  - Saves config to disk and refreshes all UI views
  - Shows a QMessageBox dialog with the count of added feeds

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_signature              : add_all_presets(window) -> None with exact
                                   parameter name and return type
  - test_source_imports         : Source imports QMessageBox, get_preset_feeds,
                                   feed_already_present, generate_feed_id,
                                   append_log_message, save_feeds,
                                   refresh_window, refresh_presets_table

Layer 2 (Behavioral):
  - test_bulk_import_skips_duplicates_and_empty : 5 fixtures (1 dup + 1 empty
                                                    name + 1 empty url) → 2 added
  - test_nothing_to_add_shows_zero_dialog       : Empty preset list → dialog
                                                    shows count=0, no save/refresh

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
          real MainWindow that add_all_presets touches: window.feeds and other
          UI stubs.

    OPTIONS: None.

    DEFAULTS: All stub attributes default to MagicMock. The feeds list is set
              to [] so we can verify append behavior during bulk import.

    OUTPUT/EFFECT: Returns a configured WindowStub ready for add_all_presets.

    ERRORS/EDGE CASES: None — MagicMock never raises on attribute access.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.feeds = []
    return w


_FIXTURE_PRESETS = [
    {"name": "Feed A", "url": "https://a.com/feed", "category": "Tech"},
    {"name": "Feed B", "url": "https://b.com/feed", "category": "News"},
    {"name": "Feed A", "url": "https://a.com/feed", "category": "Tech"},  # duplicate (same url)
    {"name": "", "url": "https://empty.com/feed", "category": "Other"},  # empty name
    {"name": "Feed C", "url": "", "category": "Other"},                  # empty url
]


def _mock_feed_already_present(preset, feeds):
    """Simulate the real dedup logic: match by normalized url or lowercase name.

    WHAT: Mirrors the actual feed_already_present function from the presets
          library. It normalizes URLs (strip trailing slash) and names (lowercase)
          before comparing, so minor formatting differences don't cause false
          duplicates.

    OPTIONS:
      - preset: dict with 'name' and 'url' keys
      - feeds: list of already-subscribed feed dicts

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns True if a matching feed exists, False otherwise.

    ERRORS/EDGE CASES: None — always returns a boolean.
    """
    preset_url = (preset.get("url") or "").strip().rstrip("/")
    preset_name = (preset.get("name") or "").strip().lower()
    for feed in feeds:
        feed_url = (feed.get("url") or "").strip().rstrip("/")
        feed_name = (feed.get("name") or "").strip().lower()
        if (preset_url and feed_url == preset_url) or (preset_name and feed_name == preset_name):
            return True
    return False


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks.

    These tests inspect the source code's structure without running the GUI.
    They fail if add_all_presets's signature or imports drift from the contract.
    """

    def test_signature(self):
        """Layer 1 — exact signature check.

        WHAT: Confirms add_all_presets takes exactly one required parameter
              named "window" and declares a return type of None.

        WHY SIGNATURE MATTERS:
          Every caller uses: add_all_presets(window)
          If the parameter count or name changed, all callers break with TypeError.

        OPTIONS:
          - Parameter "window": POSITIONAL_OR_KEYWORD, no default, no type hint
          - Return type: annotated None

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when the signature matches exactly.

        ERRORS/EDGE CASES:
          - Wrong parameter name/kind/default: params mismatch assertion fails
          - Missing return annotation: return_annotation != None fails

        HOW TO TEST: Change the parameter name from "window" to "app" in the
                     source, then run — it should fail with a params mismatch.
        """
        import inspect
        from gui._33_preset_add_all_bulk_import.add_all_presets import (
            add_all_presets,
        )
        sig = inspect.signature(add_all_presets)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Layer 1 — source import check.

        WHAT: Verifies the source file imports all eight collaborators needed
              by add_all_presets: QMessageBox, get_preset_feeds,
              feed_already_present, generate_feed_id, append_log_message,
              save_feeds, refresh_window, and refresh_presets_table.

        WHY THESE IMPORTS:
          Each import serves a distinct role: fetching presets, dedup checking,
          ID generation, logging, persisting, and refreshing the UI.

        OPTIONS: Expected set is exactly the eight modules listed above.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when all eight imports exist in the source.

        ERRORS/EDGE CASES:
          - Missing import: "Missing imports: [...]" naming the module

        HOW TO TEST: Rename one import path in the source, then run —
                     it should fail and name the missing module.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._33_preset_add_all_bulk_import.add_all_presets"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {
                "PyQt6.QtWidgets",
                "features.feature_feed_presets_library.implementation.feeds_presets",
                "gui._09_feed_identifier_generate_from_name.generate_feed_id",
                "gui._10_log_append_timestamped_message.append_timestamped_log",
                "gui._15_feed_config_save_to_disk.save_feeds",
                "gui._16_refresh_all_views_pipeline.refresh_all_views",
                "gui._31_presets_table_refresh_view.refresh_presets_table",
            },
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real add_all_presets function.

    These tests call the REAL add_all_presets against a fake window while
    verifying deduplication, empty-entry filtering, persistence, and UI refresh.
    """

    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.refresh_presets_table")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.refresh_window")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.save_feeds")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.generate_feed_id", side_effect=["a", "b", "c"])
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.feed_already_present", side_effect=_mock_feed_already_present)
    @patch(
        "gui._33_preset_add_all_bulk_import.add_all_presets.get_preset_feeds",
        return_value=_FIXTURE_PRESETS,
    )
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.QMessageBox.information")
    def test_bulk_import_skips_duplicates_and_empty(self, mock_info, mock_feeds, mock_already,
                                                     mock_gen_id, mock_save, mock_refresh_win,
                                                     mock_refresh_presets, qapp):
        """Layer 2 — 5 fixtures: 1 dup + 1 empty name + 1 empty url → 2 added.

        WHAT: With 5 preset fixtures (2 valid unique, 1 duplicate, 1 empty name,
              1 empty URL), exactly 2 feeds should be added to window.feeds.
              The duplicate is caught by feed_already_present; the empty entries
              are caught by the name/URL validation. After adding, config is
              saved, views refreshed, and a dialog shows "Added 2 preset feed(s)".

        WHY _mock_feed_already_present:
          The real dedup logic matches by normalized URL (no trailing slash) or
          lowercase name. We simulate this in the mock so the duplicate Feed A
          is correctly detected on the third iteration.

        WHY side_effect=["a","b","c"] for generate_feed_id:
          Each added feed gets a unique ID. The side_effect provides sequential
          IDs so we can verify each call produces a distinct identifier.

        OPTIONS:
          - _FIXTURE_PRESETS contains 5 items as described above
          - All downstream functions are mocked to record calls only

        DEFAULTS: fetch_interval_hours=12, enabled=True (set by the source).

        OUTPUT/EFFECT:
          - w.feeds has exactly 2 entries
          - Both entries have fetch_interval_hours=12 and enabled=True
          - save_feeds(w), refresh_window(w), refresh_presets_table(w) each called once
          - QMessageBox.information called with count=2

        ERRORS/EDGE CASES:
          - Wrong feed count: assert len(w.feeds) == 2 fails
          - Missing defaults: assertion on fetch_interval_hours/enabled fails
          - Dialog message wrong: mock_info assertion fails

        HOW TO TEST: Remove the feed_already_present dedup check from the source,
                     then run — 3 feeds would be added instead of 2 (duplicate
                     would not be skipped).
        """
        from gui._33_preset_add_all_bulk_import.add_all_presets import (
            add_all_presets,
        )
        w = _make_window()
        add_all_presets(w)
        # Only 2 valid unique entries added
        assert len(w.feeds) == 2
        assert all(f["fetch_interval_hours"] == 12 and f["enabled"] is True for f in w.feeds)
        mock_save.assert_called_once_with(w)
        mock_refresh_win.assert_called_once_with(w)
        mock_refresh_presets.assert_called_once_with(w)
        mock_info.assert_called_once_with(w, "Presets Imported", "Added 2 preset feed(s) to your subscriptions.")

    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.refresh_presets_table")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.refresh_window")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.save_feeds")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.QMessageBox.information")
    def test_nothing_to_add_shows_zero_dialog(self, mock_info, mock_save, mock_refresh_win,
                                               mock_refresh_presets, qapp):
        """Layer 2 — empty preset list shows zero-count dialog, no side effects.

        WHAT: When get_preset_feeds returns an empty list, add_all_presets must
              show a dialog with count=0 and NOT call save_feeds, refresh_window,
              or refresh_presets_table (nothing changed, so no need to refresh).

        WHY NO SAVE/REFRESH:
          If zero feeds were added, there is no data change to persist or display.
          Calling save/refresh would be wasteful and could trigger unnecessary
          UI updates.

        OPTIONS:
          - get_preset_feeds returns [] (empty list)
          - All downstream functions are mocked to record calls only

        DEFAULTS: N/A.

        OUTPUT/EFFECT:
          - w.feeds remains empty (len == 0)
          - save_feeds, refresh_window, refresh_presets_table NOT called
          - QMessageBox.information called with count=0

        ERRORS/EDGE CASES:
          - Save/refresh called unnecessarily: assert_not_called fails
          - Wrong dialog message: mock_info assertion fails

        HOW TO TEST: Remove the "if added:" guard around save/refresh in the
                     source, then run — save and refresh would be called even
                     when zero feeds were added.
        """
        from gui._33_preset_add_all_bulk_import.add_all_presets import (
            add_all_presets,
        )
        w = _make_window()
        with patch(
            "gui._33_preset_add_all_bulk_import.add_all_presets.get_preset_feeds",
            return_value=[],
        ):
            add_all_presets(w)
        assert len(w.feeds) == 0
        mock_save.assert_not_called()
        mock_refresh_win.assert_not_called()
        mock_refresh_presets.assert_not_called()
        mock_info.assert_called_once_with(w, "Presets Imported", "Added 0 preset feed(s) to your subscriptions.")
