"""Contract-drift tests for gui/_24_preset_quick_import_single_feed/import_preset_feed.py

CONTRACT SNAPSHOT
  module   : gui._24_preset_quick_import_single_feed.import_preset_feed
  function : import_preset(window, name: str, url: str, category: str) -> None
  imports  : (none external — direct attribute assignment + method call)
  effects  : fills in_name, in_url, in_cat; calls window.add_feed
  errors   : None — delegated to add_feed()
"""
# ===========================================================================
# WHAT THIS TEST FILE VERIFIES
# ===========================================================================
# This file protects the recorded CONTRACT of
# gui/_24_preset_quick_import_single_feed/import_preset_feed.py.
# SOURCE BEHAVIOUR (the contract being locked in):
#   Set window.in_name.setText(name), window.in_url.setText(url),
#   window.in_cat.setText(category), then call window.add_feed().
#   No validation is performed here — all validation is delegated to
#   add_feed() which is called afterward.
#
# ===========================================================================
# LAYER BREAKDOWN
# ===========================================================================
# Layer 1 — Structural: shape-of-the-code checks to catch refactor drift.
# Layer 2 — Behavioral Smoke: fake-window smoke tests that verify the form
#                              fields are populated with the exact values
#                              passed in, and that window.add_feed is called
#                              exactly once.
#
# ===========================================================================
# LAYER WHAT EACH TEST CHECKS
# ===========================================================================
# Layer 1 — Structural:
#   test_signature       - exactly four params: "window", "name", "url",
#                          "category" (all positional-or-keyword, no default),
#                          returns None.
#   test_source_imports  - module has NO external imports (empty set).
#   test_callables       - module exposes ONLY the public symbol
#                          "import_preset".
# Layer 2 — Behavioral Smoke:
#   test_fills_form_fields_and_calls_add_feed - all three setText calls hit
#                                                with the right values and
#                                                add_feed is called once.
#   test_add_feed_called_exactly_once         - add_feed call count is 1.
# ===========================================================================
# WHAT: Verifies the import_preset contract survives refactor drift.
# OPTIONS: window with in_name, in_url, in_cat, add_feed; name, url, category strings
# DEFAULTS: N/A
# OUTPUT/EFFECT: Form fields populated; window.add_feed called exactly once
# ERRORS/EDGE CASES: None — all validation delegated to add_feed()
# HOW TO TEST: import_preset(window, "Name", "https://...", "Category")

# sys = runtime controls; plants fake PyQt6 modules and extends import path.
import sys
# inspect = reads a function's declared parameters without running it.
import inspect
# Path = readable file-system paths.
from pathlib import Path
# MagicMock = fake call-recording object; patch = swap a name temporarily.
from unittest.mock import MagicMock, patch

# pytest = the test runner.
import pytest

# Ensure offscreen platform for headless Qt rendering
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
from gui._24_preset_quick_import_single_feed.import_preset_feed import import_preset


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

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
        """WHAT: Verify import_preset accepts exactly four parameters.

        OPTIONS: None — contract is fixed at four parameters: 'window',
                 'name', 'url', and 'category' (all positional-or-keyword,
                 no defaults), returning None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts the signature matches
                       (window, name, url, category) -> None.
        ERRORS/EDGE CASES: If the source gains or loses parameters the test
                           fails, flagging refactor drift.
        HOW TO TEST: assert_signature(import_preset, [("window", 1, inspect.Parameter.empty),
                                                      ("name", 1, inspect.Parameter.empty),
                                                      ("url", 1, inspect.Parameter.empty),
                                                      ("category", 1, inspect.Parameter.empty)], None)
        """
        assert_signature(import_preset, [("window", 1, inspect.Parameter.empty),
                                          ("name", 1, inspect.Parameter.empty),
                                          ("url", 1, inspect.Parameter.empty),
                                          ("category", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """WHAT: Verify the source file has no external imports.

        OPTIONS: None — the contract specifies zero external imports.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts AST-parsed source contains no import statements
                       (empty import set).
        ERRORS/EDGE CASES: If the source introduces any import the test fails.
        HOW TO TEST: assert_source_imports(module_path, set())
        """
        module_path = str(Path(__file__).resolve().parents[3]
                          / "gui" / "_24_preset_quick_import_single_feed" / "import_preset_feed.py")
        assert_source_imports(module_path, set())

    def test_callables(self):
        """WHAT: Verify the module exposes exactly one public callable.

        OPTIONS: None.
        DEFAULTS: N/A
        OUTPUT/EFFECT: Asserts dir(mod) contains only "import_preset" among
                       user-defined callables.
        ERRORS/EDGE CASES: Extra or missing callables indicate drift.
        HOW TO TEST: assert_callables(mod, {"import_preset"})
        """
        import gui._24_preset_quick_import_single_feed.import_preset_feed as mod
        assert_callables(mod, {"import_preset"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:
    """Layer 2 — Behavioral smoke tests against a fake window.

    WHAT: Verifies the observable behaviour of import_preset: populating
         the three form text fields with the exact values passed in, and
         calling window.add_feed exactly once.
    OPTIONS: window with in_name, in_url, in_cat (each with setText), and
             add_feed (a callable).
    DEFAULTS: N/A
    OUTPUT/EFFECT: Form fields populated; window.add_feed called exactly once.
    ERRORS/EDGE CASES: None — all validation is delegated to add_feed().
    HOW TO TEST: import_preset(window, "Name", "https://...", "Category");
                 verify setText calls and add_feed call count.
    """

    def test_fills_form_fields_and_calls_add_feed(self):
        """WHAT: Verify all three form fields are set and add_feed fires.

        OPTIONS: name="TechCrunch", url="https://techcrunch.com/feed/",
                 category="Technology".
        DEFAULTS: None — all three values are explicitly provided.
        OUTPUT/EFFECT: window.in_name.setText("TechCrunch"),
                       window.in_url.setText("https://techcrunch.com/feed/"),
                       window.in_cat.setText("Technology"),
                       window.add_feed called once.
        ERRORS/EDGE CASES: If any setText is called with wrong args or
                           add_feed is not called the assertion fails.
        HOW TO TEST: Call import_preset; assert each setText was called once
                     with the correct string; assert add_feed called once.
        """
        window = WindowStub()
        window.add_feed = MagicMock()

        import_preset(window, "TechCrunch", "https://techcrunch.com/feed/", "Technology")

        window.in_name.setText.assert_called_once_with("TechCrunch")
        window.in_url.setText.assert_called_once_with("https://techcrunch.com/feed/")
        window.in_cat.setText.assert_called_once_with("Technology")
        window.add_feed.assert_called_once()

    def test_add_feed_called_exactly_once(self):
        """WHAT: Verify add_feed is called exactly once (no more, no less).

        OPTIONS: name="Name", url="https://n.com/feed", category="Cat".
        DEFAULTS: None — simple values used for clarity.
        OUTPUT/EFFECT: window.add_feed.call_count == 1.
        ERRORS/EDGE CASES: If the source calls add_feed zero times or
                           multiple times the assertion fails.
        HOW TO TEST: Call import_preset; assert window.add_feed.call_count == 1.
        """
        window = WindowStub()
        window.add_feed = MagicMock()
        import_preset(window, "Name", "https://n.com/feed", "Cat")
        assert window.add_feed.call_count == 1
