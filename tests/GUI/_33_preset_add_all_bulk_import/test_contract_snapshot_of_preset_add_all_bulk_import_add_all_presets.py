"""Contract snapshot: gui/_33_preset_add_all_bulk_import/add_all_presets.py v1.0.0

Structural contract:
  - Function name: add_all_presets
  - Signature: (window) -> None
  - Source imports: PyQt6.QtWidgets.QMessageBox,
                   features.feature_feed_presets_library.implementation.feeds_presets.get_preset_feeds,
                   features.feature_feed_presets_library.implementation.feeds_presets.feed_already_present,
                   gui._09_feed_identifier_generate_from_name.generate_feed_id.generate_feed_id,
                   gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message,
                   gui._15_feed_config_save_to_disk.save_feeds.save_feeds,
                   gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_window,
                   gui._31_presets_table_refresh_view.refresh_presets_table.refresh_presets_table
  - Side effects: window.feeds.append, save_feeds, refresh_window, refresh_presets_table,
                  append_log_message, QMessageBox.information
"""
# ==============================================================================
# WHAT: Verifies the add_all_presets GUI contract — bulk import of unsubscribed
#       preset feeds, with deduplication of existing and invalid entries.
#
# OPTIONS:
#   window: MainWindow stub with empty feeds list.
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: New presets added; tables refreshed; info dialog shown with count.
#
# ERRORS/EDGE CASES: Duplicate or empty-name/url presets are skipped.
#
# HOW TO TEST: add_all_presets(window)
# ==============================================================================
import importlib.util
import pytest
from unittest.mock import MagicMock, patch

# offscreen platform required for all PyQt6 widget testing
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform


@pytest.fixture(scope="module")
def qapp():
    """Create a single QApplication instance for the module."""
    app = QApplication([])
    yield app



def _make_window():
    """Build a minimal WindowStub with empty feeds."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.feeds = []
    return w


_FIXTURE_PRESETS = [
    {"name": "Feed A", "url": "https://a.com/feed", "category": "Tech"},
    {"name": "Feed B", "url": "https://b.com/feed", "category": "News"},
    {"name": "Feed A", "url": "https://a.com/feed", "category": "Tech"},  # duplicate
    {"name": "", "url": "https://empty.com/feed", "category": "Other"},  # empty name
    {"name": "Feed C", "url": "", "category": "Other"},                  # empty url
]


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert add_all_presets(window) -> None."""
        import inspect
        from gui._33_preset_add_all_bulk_import.add_all_presets import (
            add_all_presets,
        )
        sig = inspect.signature(add_all_presets)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Source must import QMessageBox, get_preset_feeds, feed_already_present, etc."""
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
    """Behavioral smoke tests against the real function."""

    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.refresh_presets_table")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.refresh_window")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.save_feeds")
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.generate_feed_id", side_effect=["a", "b", "c"])
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.feed_already_present", return_value=False)
    @patch(
        "gui._33_preset_add_all_bulk_import.add_all_presets.get_preset_feeds",
        return_value=_FIXTURE_PRESETS,
    )
    @patch("gui._33_preset_add_all_bulk_import.add_all_presets.QMessageBox.information")
    def test_bulk_import_skips_duplicates_and_empty(self, mock_info, mock_feeds, mock_already,
                                                     mock_gen_id, mock_save, mock_refresh_win,
                                                     mock_refresh_presets, qapp):
        """5 fixtures incl. 1 duplicate + 1 empty name + 1 empty url → 2 added."""
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
        """All presets already subscribed → added=0, no save/refresh, dialog shows 0."""
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
