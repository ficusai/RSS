"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_30_preset_categories_load_dropdown/load_preset_categories.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the load_preset_categories function — the function that
repopulates the preset category dropdown when the Subscriptions Hub tab
loads or when the user switches to a different context. It reads the
currently selected category text, blocks signals to prevent unwanted events
during the rebuild, clears the existing items, adds "All Categories" as
the first option followed by the sorted list of preset categories from the
feeds_presets library, and then restores the previous selection if it is
still present in the new list. If the presets library is unavailable, it
falls back to showing only "All Categories".

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_signature               : load_preset_categories(window) -> None exact signature
  - test_no_top_level_imports    : Source has no top-level imports (all lazy inside function)

Layer 2 (Behavioral):
  - test_populates_dropdown_with_fallback_and_restores_selection : Dropdown filled; blockSignals called twice
  - test_fallback_on_import_error                              : Import error → only "All Categories"
  - test_restores_selection_when_still_present                 : Selection preserved if still in new list

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# importlib.util: Inspects Python modules and locates their source files on disk.
import importlib.util
# pytest: The test runner that discovers, runs, and reports these tests.
import pytest
# unittest.mock.MagicMock: A fake object that records every call made to it.
# unittest.mock.patch: Temporarily swaps a name for a fake during a test.
from unittest.mock import MagicMock, patch

# os: Reads and writes environment variables.
# The two lines below set QT_QPA_PLATFORM=offscreen BEFORE any PyQt6 widget
# is instantiated, preventing the test process from trying to open a real X11
# or Wayland display during headless CI runs.
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# PyQt6.QtWidgets.QApplication: The Qt application object required before any
# Qt widget can be created. We import it here (after the offscreen env var)
# so the real PyQt6 library loads in offscreen mode.
from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform

# Module-level QApplication instance. Uses QApplication.instance() to reuse
# an existing app created by another test module, preventing the PyQt6 crash
# that occurs when multiple QApplications exist in the same process.
_qapp = QApplication.instance() or QApplication([])



def _make_window():
    """Build a minimal WindowStub with preset_combo_cat.

    WHAT: Creates a WindowStub from conftest and configures preset_combo_cat
          to record calls to addItems, blockSignals, clear, and setCurrentText.
          The stub also tracks the current text so we can verify selection
          restoration behavior.

        OPTIONS: None — the stub is constructed with a fixed shape.

    DEFAULTS: currentText returns "Technology" (a category that will NOT be
              in the mocked preset list, testing the fallback path).

    OUTPUT/EFFECT: Returns a WindowStub with preset_combo_cat as a MagicMock
                   that tracks addItems, blockSignals, clear, and
                   setCurrentText calls.

    ERRORS/EDGE CASES:
      - WindowStub missing in conftest: ImportError
      - Missing preset_combo_cat attribute: AttributeError at call time
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    w.preset_combo_cat.currentText = MagicMock(return_value="Technology")
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks.

    WHAT: Verifies the surface-level contract of load_preset_categories —
          its function signature and the fact that it has no top-level
          imports. The function uses lazy imports (importing inside the
          function body) to avoid loading the heavy presets library unless
          the function is actually called. This is an intentional design
          choice to keep startup time fast.
    """

    def test_signature(self):
        """assert load_preset_categories(window) -> None.

        WHAT: Verifies the function has exactly one required parameter named
              "window" and a return type annotation of None.

        WHY SIGNATURE MATTERS:
              Every caller uses: load_preset_categories(window)
              If the parameter count or name changed, all callers break with TypeError.

        OPTIONS:
          - Parameter name: must be exactly "window"
          - Parameter kind: POSITIONAL_OR_KEYWORD
          - Default: none (required)
          - Return type: must be annotated as None

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes if signature matches exactly.

        ERRORS/EDGE CASES:
          - Wrong parameter name: params mismatch
          - Added default: default mismatch
          - Missing return annotation: return_annotation == inspect.Parameter.empty

        HOW TO TEST: Change parameter from "window" to "app" in source.
                     Run this test — it should fail with params mismatch.
        """
        import inspect
        from gui._30_preset_categories_load_dropdown.load_preset_categories import (
            load_preset_categories,
        )
        sig = inspect.signature(load_preset_categories)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
        assert sig.return_annotation is None

    def test_no_top_level_imports(self):
        """Source has no top-level imports (all lazy inside function).

        WHAT: Verifies the source file contains NO import statements at the
              module level. All imports are deferred inside the function body
              (lazy import pattern). This keeps the module dependency-free
              at load time and avoids importing heavy libraries like
              features.feature_feed_presets_library on startup.

        WHY LAZY IMPORTS:
              The presets library is large (475 feeds across 22 categories)
              and slow to import. By deferring the import until the function
              is actually called, the app starts faster and the import cost
              is only paid when the user opens the Subscriptions Hub tab.

        OPTIONS: The expected import set is empty — no imports at top level.

        DEFAULTS: Empty set of top-level imports.

        OUTPUT/EFFECT: Passes if ast.parse finds zero Import / ImportFrom nodes
                       at the module level.

        ERRORS/EDGE CASES:
          - Top-level import added: assert_source_imports lists the unexpected module
          - Import moved out of function body: assertion fails

        HOW TO TEST: Add "import os" at the top of the source file.
                     Run this test — it should fail with "Unexpected imports: ['os']".
        """
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
    """Behavioral smoke tests against the real function.

    WHAT: Runs the REAL load_preset_categories function against a WindowStub
          and replaces get_preset_categories with a recording mock. This lets
          us control the returned category list and verify the exact items
          added to the dropdown, the blockSignals pattern, and the selection
          restoration logic.
    """

    @patch(
        "features.feature_feed_presets_library.implementation.feeds_presets.get_preset_categories",
        return_value=["Finance", "News", "Science"],
    )
    def test_populates_dropdown_with_fallback_and_restores_selection(self, mock_get_cats):
        """Dropdown populated with 'All Categories' + sorted cats; selection restored.

        WHAT: Calls load_preset_categories(w) with get_preset_categories
              returning ["Finance", "News", "Science"]. Passes only if:
              1. The dropdown was cleared and repopulated with
                 ["All Categories", "Finance", "News", "Science"] (sorted)
              2. blockSignals was called twice (True before rebuild, False after)
              3. setCurrentText was NOT called because "Technology" (the
                 previous selection) is not in the new list

        WHY BLOCK SIGNALS:
              Qt signals fire whenever a combo box's items change. If we
              rebuilt the list without blocking signals, the currentIndexChanged
              signal would fire for each addItems call, potentially triggering
              unwanted side effects (like fetching articles for the wrong
              category). blockSignals(True) suppresses these events during
              the rebuild, and blockSignals(False) re-enables them afterward.

        WHY SORTED:
              Preset categories are returned alphabetically sorted so users
              can find them easily in the dropdown. The sort order is
              deterministic and does not depend on the order returned by
              the presets library.

        OPTIONS:
          - window: WindowStub with preset_combo_cat; currentText returns "Technology"
          - categories: ["Finance", "News", "Science"]

        DEFAULTS: N/A — explicit category list passed via mock.

        OUTPUT/EFFECT:
          - addItems(["All Categories", "Finance", "News", "Science"])
          - blockSignals called twice (True then False)
          - setCurrentText not called (previous selection not in new list)

        ERRORS/EDGE CASES:
          - Wrong item order: addItems assertion fails
          - blockSignals called wrong number of times: call_count assertion fails
          - setCurrentText called when it shouldn't: assert_not_called fails

        HOW TO TEST: Mock get_preset_categories to return the above list, call
                     the function, and verify addItems, blockSignals, and
                     setCurrentText call history.
        """
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
    def test_fallback_on_import_error(self, mock_get_cats):
        """Import error → falls back to ['All Categories'] only.

        WHAT: Calls load_preset_categories(w) with get_preset_categories
              raising ImportError. Passes only if the dropdown was populated
              with ["All Categories"] only — the function gracefully degrades
              when the presets library is unavailable rather than crashing.

        WHY FALLBACK:
              The presets library is an optional dependency. Users who do not
              have it installed should still be able to use the app; they just
              won't see preset categories. Falling back to "All Categories"
              ensures the dropdown is never empty, which would look broken.

        OPTIONS:
          - window: WindowStub with preset_combo_cat
          - exception: ImportError raised by get_preset_categories

        DEFAULTS: N/A — explicit ImportError raised via mock.

        OUTPUT/EFFECT: addItems(["All Categories"]) called once.

        ERRORS/EDGE CASES:
          - Function crashes instead of falling back: exception raised
          - Dropdown populated with wrong items: addItems assertion fails
          - blockSignals called unnecessarily: call_count assertion fails

        HOW TO TEST: Mock get_preset_categories to raise ImportError, call
                     the function, and verify only "All Categories" is added.
        """
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
    def test_restores_selection_when_still_present(self, mock_get_cats):
        """Selection already in new list → restored via setCurrentText.

        WHAT: Calls load_preset_categories(w) with get_preset_categories
              returning ["Finance", "News"] and the previous selection being
              "All Categories". Passes only if setCurrentText was called with
              "All Categories" — the function preserves the user's previous
              choice when it is still available in the rebuilt list.

        WHY RESTORE SELECTION:
              Users expect their dropdown position to be preserved when the
              list is rebuilt. If they had "All Categories" selected before
              and it is still present after the reload, the UI should show
              "All Categories" as selected rather than jumping to the first
              item. This prevents confusion and maintains context.

        OPTIONS:
          - window: WindowStub with currentText returning "All Categories"
          - categories: ["Finance", "News"]

        DEFAULTS: N/A — explicit category list and current text via mock.

        OUTPUT/EFFECT:
          - addItems(["All Categories", "Finance", "News"])
          - setCurrentText("All Categories") called once

        ERRORS/EDGE CASES:
          - Selection not restored: assert_called_once_with fails
          - Wrong text passed to setCurrentText: assertion fails
          - addItems called with unsorted list: assertion fails

        HOW TO TEST: Mock currentText to return "All Categories", mock
                     get_preset_categories to return ["Finance", "News"],
                     call the function, and verify setCurrentText was called.
        """
        from gui._30_preset_categories_load_dropdown.load_preset_categories import (
            load_preset_categories,
        )
        w = _make_window()
        w.preset_combo_cat.currentText = MagicMock(return_value="All Categories")
        load_preset_categories(w)
        w.preset_combo_cat.setCurrentText.assert_called_once_with("All Categories")
