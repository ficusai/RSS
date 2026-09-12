"""Contract-drift tests for gui/_16_refresh_all_views_pipeline/refresh_all_views.py

CONTRACT SNAPSHOT
  module   : gui._16_refresh_all_views_pipeline.refresh_all_views
  function : refresh_window(window) -> None
  imports  : gui._13_stats_badges_update_live.update_stats_badges
            , gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table
            , gui._18_articles_table_refresh_view.refresh_articles_table
  effects  : calls all three refresh functions in sequence
  errors   : each sub-function handles its own errors
"""
# ==============================================================================
# WHAT THIS TEST FILE VERIFIES
# ==============================================================================
# This file verifies `refresh_window` — the ORCHESTRATOR that keeps every RSS
# view in sync after feeds change. In user terms, each time feeds are added,
# deleted, toggled, or scraped, this function re-renders the whole app:
#   - Rebuilds the subscriptions (feed) table for the current feed list
#   - Reloads and rebuilds the articles table for the current content
#   - Recomputes the header stat badges (article / feed counts)
# It does no real work itself: it only CALLS the three per-view refresh helpers
# in a fixed order, passing the same window through unchanged. Each helper
# handles its own errors, so this pipeline needs no try/except of its own.
#
# ==============================================================================
# LAYER BREAKDOWN
# ==============================================================================
# Layer 1 (Structural):
#   - test_signature                                   : refresh_window(window) -> None
#   - test_source_imports                              : source imports all three refresh helpers
#   - test_callables                                   : module exposes exactly one public callable
#
# Layer 2 (Behavioral):
#   - test_calls_all_three_refresh_functions              : each helper called exactly once with window
#   - test_order_is_subscriptions_then_articles_then_stats : helpers fire in the fixed order (subs, articles, stats)
#
# LAYER WHAT EACH TEST CHECKS
# ==============================================================================
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# import sys: runtime controls; plants fake PyQt6 modules and extends the
#             import path so the source modules resolve during testing.
import sys
# import inspect: reads a function's declared parameters without running it.
import inspect
# import pathlib.Path: readable file-system paths.
from pathlib import Path
# import unittest.mock: MagicMock = fake call-recording object; patch = swap a
# name inside a module for the duration of a test, then restore it.
from unittest.mock import patch, MagicMock

# import pytest: the test runner that collects and runs these tests.
import pytest

# Ensure offscreen platform for headless Qt rendering
# Plant fake PyQt6 packages before any real import so no screen is needed.
sys.modules.setdefault("PyQt6.QtCore", MagicMock())
sys.modules.setdefault("PyQt6.QtGui", MagicMock())
sys.modules.setdefault("PyQt6.QtWidgets", MagicMock())

# PROJECT_ROOT: three folders up from here = the RSS project root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Put the root on Python's import search path (once).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# import tests.GUI.conftest: shared helpers — the structural assertions
# (signature / imports / callables) plus WindowStub, the fake window that
# supplies every GUI attribute as a recording MagicMock.
from tests.GUI.conftest import assert_signature, assert_source_imports, assert_callables, WindowStub

# ---------------------------------------------------------------------------
# Module under test
# ---------------------------------------------------------------------------
# import gui._16_refresh_all_views_pipeline.refresh_all_views: the REAL source
# module whose refresh_window function is the one guarded by this test file.
from gui._16_refresh_all_views_pipeline.refresh_all_views import refresh_window


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================
# Shape-of-the-code checks to catch refactor drift. The separator bars below
# are the file's original formatting and are kept verbatim.

class TestLayer1Structural:
    """Layer 1 (Structural): shape-of-the-code checks that snapshot the public
    surface of gui._16_refresh_all_views_pipeline.refresh_all_views. They lock
    in the exact function signature, the three helper imports the orchestrator
    composes, and the single public callable, so a refactor drifts and breaks
    here instead of failing silently at runtime. Example real inputs: the
    refresh_all_views.py module, and inspect.signature(refresh_window).
    """

    def test_signature(self):
        """Layer 1 — refresh_window(window) -> None exact signature.

        WHAT: Asserts refresh_window accepts exactly one required, positional-
              or-keyword parameter named "window" (no default) and returns
              None. Every caller in the app does refresh_window(window),
              so changing the parameter would raise a TypeError in production.
        OPTIONS: "window" — the MainWindow instance to refresh.
        DEFAULTS: N/A — the parameter is required, no default value.
        OUTPUT/EFFECT: Passes when the signature matches exactly; otherwise the
              assert_signature helper raises with a "CONTRACT DRIFT" message.
        ERRORS/EDGE CASES: A renamed, added, or defaulted parameter fails here.
        HOW TO TEST: Rename "window" to "app" in the source and re-run.
        """
        # Contract: exactly one parameter "window" (kind 1 = positional-or-
        # keyword), no default value, returns None.
        assert_signature(refresh_window, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        """Layer 1 — source imports all three refresh helpers.

        WHAT: Parses the REAL source file with the ast module and asserts that
              it imports update_stats_badges, refresh_subscriptions_table, and
              refresh_articles_table from their atomic modules — the three
              parts the orchestrator composes. Losing any one of these means
              that view can never refresh again.
        OPTIONS: module_path points at refresh_all_views.py on disk.
        DEFAULTS: N/A — the three expected module paths are fixed by contract.
        OUTPUT/EFFECT: Passes when every expected module path is found by the
              AST scan; reports the missing names otherwise.
        ERRORS/EDGE CASES: A removed or renamed import fails the missing set.
        HOW TO TEST: Delete one of the three imports in the source and re-run.
        """
        # Point at the real source file on disk.
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_16_refresh_all_views_pipeline" / "refresh_all_views.py")
        # The source MUST import all three refresh helpers (two table refreshes
        # plus the stats-badge refresh), because they are the pipeline's parts.
        assert_source_imports(module_path, {
            "gui._13_stats_badges_update_live.update_stats_badges",
            "gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table",
            "gui._18_articles_table_refresh_view.refresh_articles_table",
        })

    def test_callables(self):
        """Layer 1 — module exposes exactly one public callable.

        WHAT: Asserts the source module defines ONLY refresh_window as a public
              function. This locks in the module's public surface so helpers
              accidentally left public (or added later) are caught early.
        OPTIONS: the module object imported under its real package path.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: Passes while the only public function is refresh_window.
        ERRORS/EDGE CASES: Any extra public callable fails the allowed set.
        HOW TO TEST: Add a public helper function to the source and re-run.
        """
        # The module must define EXACTLY the public function "refresh_window".
        import gui._16_refresh_all_views_pipeline.refresh_all_views as mod
        assert_callables(mod, {"refresh_window"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================
# Level-2 tests run refresh_window with its three helper functions REPLACED by
# fakes, and verify call-count and call-ORDER. Because the helpers are real
# PyQt widgets rebuilders, we must not actually invoke them in tests.

class TestLayer2Behavioral:
    """Layer 2 (Behavioral): run the REAL refresh_window against a fake
    WindowStub (every GUI attribute is a MagicMock that records calls). The
    three helper imports are swapped for recorders, so the real widget-touching
    refresh code never executes, and the tests verify each helper fires exactly
    once — and in the fixed order subscriptions, then articles, then stats.
    Example real input: window = WindowStub() with recording MagicMocks.
    """

    def test_calls_all_three_refresh_functions(self):
        """Layer 2 — all three refresh helpers fire exactly once, with window.

        WHAT: Runs the real refresh_window while swapping each imported helper
              for a recording MagicMock, then asserts each was called exactly
              once and received the SAME window object. That proves the
              orchestrator really hands the window to every view it refreshes.
        OPTIONS: window = WindowStub() supplies every attribute as a mock.
        DEFAULTS: N/A.
        OUTPUT/EFFECT: m1/m2/m3 record one window call each; assertions verify.
        ERRORS/EDGE CASES: A skipped helper fails assert_called_once; a
              different argument fails assert_called_once_with(window).
        HOW TO TEST: Comment out one helper call in the source and re-run.
        """
        # Fake window (WindowStub supplies all the GUI attributes as mocks).
        window = WindowStub()
        # Replace the three helpers INSIDE the source module's namespace with
        # recording fakes. The trailing backslash "\" continues the with-line
        # onto the next lines (Python line continuation).
        with patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_subscriptions_table") as m1, \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_articles_table") as m2, \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.update_stats_badges") as m3:
            refresh_window(window)
            # Each fake must have been called exactly once, and each must have
            # received the SAME window object as its single argument.
            m1.assert_called_once_with(window)
            m2.assert_called_once_with(window)
            m3.assert_called_once_with(window)

    def test_order_is_subscriptions_then_articles_then_stats(self):
        """Layer 2 — helpers fire in the fixed order subs, articles, stats.

        WHAT: Observes the ORDER in which the pipeline invokes its three
              helpers. Each helper is replaced by a spy that appends its
              explicit name to the 'order' list and then calls a do-nothing
              stub. The final list must be exactly ["refresh_subscriptions_table",
              "refresh_articles_table", "update_stats_badges"].

        WHY THE NAME IS PASSED EXPLICITLY: the do-nothing stubs are lambdas,
              and every lambda's __name__ is "<lambda>" — so the spy cannot
              rely on fn.__name__ (that would record "<lambda>" three times).
              The spy therefore takes the name as its first argument.
        OPTIONS: window = WindowStub(); order collects the call sequence.
        DEFAULTS: N/A — the order itself is the contract being locked in.
        OUTPUT/EFFECT: the order list mirrors the invocation order.
        ERRORS/EDGE CASES: Reordering the calls in the source fails the list
              equality assertion word-for-word.
        HOW TO TEST: Swap two calls in the source and re-run — the list order
              assertion should fail.
        """
        window = WindowStub()
        # 'order' accumulates the names of the helper functions in the exact
        # order the pipeline invokes them.
        order = []

        # record(name, fn) builds a "spy": a wrapper that (1) logs *name* into
        # 'order', then (2) calls the real fn. The name is passed in because
        # the stubs patched in below are lambdas whose __name__ is "<lambda>".
        def record(name, fn):
            def inner(*args, **kwargs):
                order.append(name)
                return fn(*args, **kwargs)
            return inner

        # Patch all three helpers with spies. Each spy wraps a do-nothing
        # stub "lambda w: None" — a function that ignores its window argument
        # and returns None, so the real (widget-touching) helper never runs.
        with patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_subscriptions_table",
                   record("refresh_subscriptions_table", lambda w: None)), \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_articles_table",
                   record("refresh_articles_table", lambda w: None)), \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.update_stats_badges",
                   record("update_stats_badges", lambda w: None)):
            refresh_window(window)
        # The order list records each call as it happened. The source calls
        # subscriptions, then articles, then stats — so the ENTIRE list must
        # equal these three names in position (and not in any other order).
        assert order == ["refresh_subscriptions_table", "refresh_articles_table", "update_stats_badges"]