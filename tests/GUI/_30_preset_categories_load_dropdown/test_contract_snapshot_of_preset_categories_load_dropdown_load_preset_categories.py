"""Contract snapshot: gui/_30_preset_categories_load_dropdown/load_preset_categories.py v1.0.0

Structural contract:
  - Function name: load_preset_categories
  - Signature: (window) -> None
  - Source imports: None at top-level (lazy import inside function)
  - Side effects: preset_combo_cat.blockSignals, clear, addItems, setCurrentText
"""
# ==============================================================================
# WHAT: Verifies the load_preset_categories GUI contract — dropdown repopulated
#       with "All Categories" + sorted preset categories, with blockSignals guard.
#
# OPTIONS:
#   window: MainWindow stub with preset_combo_cat (QComboBox-like).
#
# DEFAULTS: Falls back to ["All Categories"] on any import error.
#
# OUTPUT/EFFECT: Preset category dropdown repopulated.
#
# ERRORS/EDGE CASES: get_preset_categories unavailable → fallback to default list.
#
# HOW TO TEST: load_preset_categories(window); assert combo count > 0
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
    """Build a minimal WindowStub with preset_combo_cat."""
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.preset_combo_cat.currentText = MagicMock(return_value="Technology")
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks."""

    def test_signature(self):
        """assert load_preset_categories(window) -> None."""
        import inspect
        from gui._30_preset_categories_load_dropdown.load_preset_categories import (
            load_preset_categories,
        )
        sig = inspect.signature(load_preset_categories)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_no_top_level_imports(self):
        """Source has no top-level imports (all lazy inside function)."""
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._30_preset_categories_load_dropdown.load_preset_categories"
        # This module intentionally has no top-level imports
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            set(),
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real function."""

    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.get_preset_categories",
        return_value=["Finance", "News", "Science"],
    )
    def test_populates_dropdown_with_fallback_and_restores_selection(self, mock_get_cats, qapp):
        """Dropdown populated with 'All Categories' + sorted cats; selection restored."""
        from gui._30_preset_categories_load_dropdown.load_preset_categories import (
            load_preset_categories,
        )
        w = _make_window()
        load_preset_categories(w)
        expected = ["All Categories", "Finance", "News", "Science"]
        w.preset_combo_cat.addItems.assert_called_once_with(expected)
        # blockSignals called twice: once True (before rebuild), once False (after)
        assert w.preset_combo_cat.blockSignals.call_count == 2
        # Previous selection "Technology" not in new list → not restored
        w.preset_combo_cat.setCurrentText.assert_not_called()

    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.get_preset_categories",
        side_effect=ImportError("no feature"),
    )
    def test_fallback_on_import_error(self, mock_get_cats, qapp):
        """Import error → falls back to ['All Categories'] only."""
        from gui._30_preset_categories_load_dropdown.load_preset_categories import (
            load_preset_categories,
        )
        w = _make_window()
        load_preset_categories(w)
        w.preset_combo_cat.addItems.assert_called_once_with(["All Categories"])

    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.get_preset_categories",
        return_value=["Finance", "News"],
    )
    def test_restores_selection_when_still_present(self, mock_get_cats, qapp):
        """Selection already in new list → restored via setCurrentText."""
        from gui._30_preset_categories_load_dropdown.load_preset_categories import (
            load_preset_categories,
        )
        w = _make_window()
        w.preset_combo_cat.currentText = MagicMock(return_value="All Categories")
        load_preset_categories(w)
        w.preset_combo_cat.setCurrentText.assert_called_once_with("All Categories")
