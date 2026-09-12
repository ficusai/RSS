"""Contract snapshot: gui/_32_preset_add_single_from_catalog/add_preset_feed.py v1.0.0

Structural contract:
  - Function name: add_preset_feed
  - Signature: (window, preset) -> None
  - Source imports: features.feature_feed_presets_library.implementation.feeds_presets.feed_already_present,
                   gui._09_feed_identifier_generate_from_name.generate_feed_id.generate_feed_id,
                   gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message,
                   gui._15_feed_config_save_to_disk.save_feeds.save_feeds
  - Side effects: window.feeds.append, save_feeds, refresh_window, refresh_presets_table, append_log_message
"""
# ==============================================================================
# WHAT: Verifies the add_preset_feed GUI contract — single preset added to
#       subscriptions with defaults, or skipped if already present / empty.
#
# OPTIONS:
#   window: MainWindow stub with feeds list, save_feeds, refresh_window, etc.
#   preset: dict with at minimum 'name' and 'url' keys.
#
# DEFAULTS: fetch_interval_hours=12, enabled=True.
#
# OUTPUT/EFFECT: Preset added to window.feeds; config saved; views refreshed.
#
# ERRORS/EDGE CASES: Already subscribed → skip + log. Missing name/url → no-op.
#
# HOW TO TEST: add_preset_feed(window, {"name": "...", "url": "...", "category": "..."})
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
    """Build a minimal WindowStub with feeds list."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.feeds = []
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert add_preset_feed(window, preset) -> None."""
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
        """Source must import feed_already_present, generate_feed_id, append_log_message, save_feeds."""
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
    """Behavioral smoke tests against the real function."""

    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.feed_already_present", return_value=False)
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.generate_feed_id", return_value="feed_a")
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.save_feeds")
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.refresh_window")
    @patch("gui._32_preset_add_single_from_catalog.add_preset_feed.refresh_presets_table")
    def test_adds_valid_preset_to_feeds(self, mock_refresh_presets, mock_refresh_win, mock_save,
                                         mock_gen_id, mock_already, qapp):
        """Valid preset → appended to feeds with correct keys; save + refresh called."""
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
        """Already present → skipped, log appended, no save/refresh."""
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
        """Empty name or URL → returns silently, nothing appended."""
        from gui._32_preset_add_single_from_catalog.add_preset_feed import (
            add_preset_feed,
        )
        w = _make_window()
        add_preset_feed(w, {"name": "", "url": "https://example.com", "category": "Tech"})
        assert len(w.feeds) == 0
        mock_save.assert_not_called()
        add_preset_feed(w, {"name": "Test", "url": "", "category": "Tech"})
        assert len(w.feeds) == 0
