"""Contract-drift tests for gui/_14_feed_config_load_from_disk/load_feeds.py

CONTRACT SNAPSHOT
  module   : gui._14_feed_config_load_from_disk.load_feeds
  function : load_feeds(window) -> None
  imports  : gui._00_paths_config_constant_definitions.paths_config_constants.CONFIG_PATH
  effects  : sets window.feeds from config/feeds.json
  errors   : missing/malformed file → window.feeds == []
"""
# WHAT: Verifies the load_feeds contract survives refactor drift.
# OPTIONS: window with feeds attr; CONFIG_PATH patched to temp files
# DEFAULTS: Missing or corrupt file → empty list
# OUTPUT/EFFECT: window.feeds populated from JSON on disk
# ERRORS/EDGE CASES: No file → []; malformed JSON → []; dict with "feeds" key → extracted; raw list → used
# HOW TO TEST: load_feeds(window); assert isinstance(window.feeds, list)

import json
import sys
import inspect
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import MagicMock, patch

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
from gui._14_feed_config_load_from_disk.load_feeds import load_feeds


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(load_feeds, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_14_feed_config_load_from_disk" / "load_feeds.py")
        assert_source_imports(module_path, {"gui._00_paths_config_constant_definitions.paths_config_constants"})

    def test_callables(self):
        import gui._14_feed_config_load_from_disk.load_feeds as mod
        assert_callables(mod, {"load_feeds"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_missing_file_yields_empty_list(self):
        window = WindowStub()
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH") as fake_path:
            fake_path.exists.return_value = False
            load_feeds(window)
        assert window.feeds == []

    def test_malformed_json_yields_empty_list(self):
        window = WindowStub()
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{not valid json")
            tmp = f.name
        from pathlib import Path as P
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH", P(tmp)):
            load_feeds(window)
        assert window.feeds == []
        Path(tmp).unlink(missing_ok=True)

    def test_dict_with_feeds_key_extracted(self):
        window = WindowStub()
        feeds_data = [{"id": "t", "name": "Tech", "url": "https://t.com/feed", "enabled": True}]
        content = json.dumps({"feeds": feeds_data})
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(content)
            tmp = f.name
        from pathlib import Path as P
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH", P(tmp)):
            load_feeds(window)
        assert window.feeds == feeds_data
        Path(tmp).unlink(missing_ok=True)

    def test_raw_list_used_directly(self):
        window = WindowStub()
        feeds_data = [{"id": "a", "name": "API", "url": "https://a.com/feed", "enabled": False}]
        content = json.dumps(feeds_data)
        with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write(content)
            tmp = f.name
        from pathlib import Path as P
        with patch("gui._14_feed_config_load_from_disk.load_feeds.CONFIG_PATH", P(tmp)):
            load_feeds(window)
        assert window.feeds == feeds_data
        Path(tmp).unlink(missing_ok=True)
