"""Contract-drift tests for gui/_15_feed_config_save_to_disk/save_feeds.py

CONTRACT SNAPSHOT
  module   : gui._15_feed_config_save_to_disk.save_feeds
  function : save_feeds(window) -> None
  imports  : gui._00_paths_config_constant_definitions.paths_config_constants.CONFIG_PATH
            , gui._10_log_append_timestamped_message.append_timestamped_log.append_log_message
  effects  : writes config/feeds.json with {"feeds": [...]} + 2-space indent
  errors   : logs via append_log_message on exception
"""
# WHAT: Verifies the save_feeds contract survives refactor drift.
# OPTIONS: window with feeds list; CONFIG_PATH patched to temp dir
# DEFAULTS: Creates parent directories automatically
# OUTPUT/EFFECT: config/feeds.json written with formatted JSON
# ERRORS/EDGE CASES: Permission error → logged; disk full → logged
# HOW TO TEST: save_feeds(window); reload and assert equality

import json
import sys
import inspect
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import pytest

# Ensure offscreen platform for headless Qt rendering
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
from gui._15_feed_config_save_to_disk.save_feeds import save_feeds


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(save_feeds, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_15_feed_config_save_to_disk" / "save_feeds.py")
        assert_source_imports(module_path, {
            "gui._00_paths_config_constant_definitions.paths_config_constants",
            "gui._10_log_append_timestamped_message.append_timestamped_log",
        })

    def test_callables(self):
        import gui._15_feed_config_save_to_disk.save_feeds as mod
        assert_callables(mod, {"save_feeds"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_writes_config_json_with_two_space_indent(self):
        with TemporaryDirectory() as tmpdir:
            fake_config = Path(tmpdir) / "config" / "feeds.json"
            window = WindowStub()
            window.feeds = [
                {"id": "a", "name": "Feed A", "url": "https://a.com/feed", "enabled": True},
                {"id": "b", "name": "Feed B", "url": "https://b.com/feed", "enabled": False},
            ]
            with patch("gui._15_feed_config_save_to_disk.save_feeds.CONFIG_PATH", fake_config):
                save_feeds(window)

            assert fake_config.exists()
            data = json.loads(fake_config.read_text())
            assert data == {"feeds": window.feeds}

            # Verify 2-space indent
            raw = fake_config.read_text()
            assert '  "feeds"' in raw

    def test_creates_config_parent_directory(self):
        with TemporaryDirectory() as tmpdir:
            fake_config = Path(tmpdir) / "deep" / "nested" / "feeds.json"
            window = WindowStub()
            window.feeds = []
            with patch("gui._15_feed_config_save_to_disk.save_feeds.CONFIG_PATH", fake_config):
                save_feeds(window)
            assert fake_config.parent.exists()

    def test_error_logs_via_append_log_message(self):
        window = WindowStub()
        window.feeds = []
        with patch("gui._15_feed_config_save_to_disk.save_feeds.CONFIG_PATH", Path("/nonexistent/path/feeds.json")):
            with patch("gui._15_feed_config_save_to_disk.save_feeds.append_log_message") as mock_log:
                save_feeds(window)
                mock_log.assert_called_once()
