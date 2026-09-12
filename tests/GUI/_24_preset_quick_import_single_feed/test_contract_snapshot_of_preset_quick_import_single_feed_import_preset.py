"""Contract-drift tests for gui/_24_preset_quick_import_single_feed/import_preset_feed.py

CONTRACT SNAPSHOT
  module   : gui._24_preset_quick_import_single_feed.import_preset_feed
  function : import_preset(window, name: str, url: str, category: str) -> None
  imports  : (none external — direct attribute assignment + method call)
  effects  : fills in_name, in_url, in_cat; calls window.add_feed
  errors   : None — delegated to add_feed()
"""
# WHAT: Verifies the import_preset contract survives refactor drift.
# OPTIONS: window with in_name, in_url, in_cat, add_feed; name, url, category strings
# DEFAULTS: N/A
# OUTPUT/EFFECT: Form fields populated; window.add_feed called exactly once
# ERRORS/EDGE CASES: None — all validation delegated to add_feed()
# HOW TO TEST: import_preset(window, "Name", "https://...", "Category")

import sys
import inspect
from pathlib import Path
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
from gui._24_preset_quick_import_single_feed.import_preset_feed import import_preset


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(import_preset, [("window", 1, inspect.Parameter.empty),
                                          ("name", 1, inspect.Parameter.empty),
                                          ("url", 1, inspect.Parameter.empty),
                                          ("category", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_24_preset_quick_import_single_feed" / "import_preset_feed.py")
        assert_source_imports(module_path, set())

    def test_callables(self):
        import gui._24_preset_quick_import_single_feed.import_preset_feed as mod
        assert_callables(mod, {"import_preset"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_fills_form_fields_and_calls_add_feed(self):
        window = WindowStub()
        window.add_feed = MagicMock()
        with patch("gui._24_preset_quick_import_single_feed.import_preset_feed.import_preset") as mock_self:
            pass  # not needed

        import_preset(window, "TechCrunch", "https://techcrunch.com/feed/", "Technology")

        window.in_name.setText.assert_called_once_with("TechCrunch")
        window.in_url.setText.assert_called_once_with("https://techcrunch.com/feed/")
        window.in_cat.setText.assert_called_once_with("Technology")
        window.add_feed.assert_called_once()

    def test_add_feed_called_exactly_once(self):
        window = WindowStub()
        window.add_feed = MagicMock()
        import_preset(window, "Name", "https://n.com/feed", "Cat")
        assert window.add_feed.call_count == 1
