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
# WHAT: Verifies the refresh_window orchestration contract survives refactor drift.
# OPTIONS: window passed through to each sub-function
# DEFAULTS: N/A
# OUTPUT/EFFECT: All three view-refresh functions called exactly once
# ERRORS/EDGE CASES: None — composition only
# HOW TO TEST: refresh_window(window); verify sub-functions called

import sys
import inspect
from pathlib import Path
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
from gui._16_refresh_all_views_pipeline.refresh_all_views import refresh_window


# ===========================================================================
# Layer 1 — Structural
# ===========================================================================

class TestLayer1Structural:

    def test_signature(self):
        assert_signature(refresh_window, [("window", 1, inspect.Parameter.empty)], None)

    def test_source_imports(self):
        module_path = str(Path(__file__).resolve().parents[3]
                         / "gui" / "_16_refresh_all_views_pipeline" / "refresh_all_views.py")
        assert_source_imports(module_path, {
            "gui._13_stats_badges_update_live.update_stats_badges",
            "gui._17_subscriptions_table_refresh_view.refresh_subscriptions_table",
            "gui._18_articles_table_refresh_view.refresh_articles_table",
        })

    def test_callables(self):
        import gui._16_refresh_all_views_pipeline.refresh_all_views as mod
        assert_callables(mod, {"refresh_window"})


# ===========================================================================
# Layer 2 — Behavioral Smoke
# ===========================================================================

class TestLayer2Behavioral:

    def test_calls_all_three_refresh_functions(self):
        window = WindowStub()
        with patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_subscriptions_table") as m1, \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_articles_table") as m2, \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.update_stats_badges") as m3:
            refresh_window(window)
            m1.assert_called_once_with(window)
            m2.assert_called_once_with(window)
            m3.assert_called_once_with(window)

    def test_order_is_subscriptions_then_articles_then_stats(self):
        window = WindowStub()
        order = []
        def record(fn):
            def inner(*args, **kwargs):
                order.append(fn.__name__)
                return fn(*args, **kwargs)
            return inner
        with patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_subscriptions_table",
                   record(lambda w: None)), \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.refresh_articles_table",
                   record(lambda w: None)), \
             patch("gui._16_refresh_all_views_pipeline.refresh_all_views.update_stats_badges",
                   record(lambda w: None)):
            refresh_window(window)
        assert order == ["refresh_subscriptions_table", "refresh_articles_table", "update_stats_badges"]
