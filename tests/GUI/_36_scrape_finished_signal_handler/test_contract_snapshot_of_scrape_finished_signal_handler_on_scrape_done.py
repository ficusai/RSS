"""
==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the on_scrape_done function — the signal handler that runs
in the main thread when the background ScrapeThread finishes. on_scrape_done:
  - Re-enables the "Sync All Feeds" button and restores its label
  - Hides the progress bar (returning UI to idle state)
  - Appends a completion log message with new/total article counts
  - Appends an error-summary log message if any feed errors occurred
  - Calls update_stats_badges to refresh the header stat badges
  - Calls refresh_articles_table to show any newly fetched articles

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_signature              : on_scrape_done(window, new: int, total: int,
                                   errors: list) -> None with exact type annotations
  - test_source_imports         : Source imports append_log_message,
                                   update_stats_badges, refresh_articles_table

Layer 2 (Behavioral):
  - test_re_enables_button_and_hides_progress : Button re-enabled with
                                                  "🔄 Sync All Feeds";
                                                  progress bar hidden
  - test_logs_completion_and_errors            : Completion log message appended;
                                                   error-summary log if errors
                                                   present
  - test_calls_update_stats_and_refresh_articles : update_stats_badges and
                                                    refresh_articles_table
                                                    called on completion

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# importlib.util: Finds the filesystem path of the source module for AST-based
#                 import verification in the structural tests.
import importlib.util
# pytest: Test framework; provides the @pytest.fixture decorator for the qapp
#         singleton that all PyQt6 widget tests share.
import pytest
# unittest.mock.MagicMock: Creates fake objects that record every method call,
#                          used to spy on window stub interactions.
# unittest.mock.patch:     Temporarily replaces module attributes with mocks so
#                          we can verify calls without running real code.
from unittest.mock import MagicMock, patch

# sys: extends Python's import search path so `import gui.*` works from here.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

# offscreen platform required for all PyQt6 widget testing
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication  # noqa: E402  # offscreen platform


@pytest.fixture(scope="module")
def qapp():
    """Provide one shared QApplication for the whole module.

    WHAT: Creates a single Qt application object so PyQt6 widgets can be
          constructed in headless (offscreen) mode without a real display.

    OPTIONS: scope="module" — one instance shared by every test in this file.

    DEFAULTS: Qt runs in offscreen mode (no visible window).

    OUTPUT/EFFECT: Yields a QApplication; Qt cleans it up after the tests run.

    ERRORS/EDGE CASES: Creating two QApplication objects in one process crashes
                       Qt, so exactly one is shared at module scope.
    """
    app = QApplication([])
    yield app



def _make_window():
    """Build a minimal WindowStub for on_scrape_done.

    WHAT: Returns a WindowStub (from conftest.py) mimicking the parts of the
          real MainWindow that on_scrape_done touches: window.btn_sync,
          window.progress, and window.log_box.

    OPTIONS: None.

    DEFAULTS: All stub attributes default to MagicMock.

    OUTPUT/EFFECT: Returns a configured WindowStub ready for on_scrape_done.

    ERRORS/EDGE CASES: None — MagicMock never raises.
    """
    from tests.GUI.conftest import WindowStub
    w = WindowStub()
    return w


# ===========================================================================
# Layer 1 — Structural assertions
# ===========================================================================

class TestLayer1_Structural:
    """Structural / signature / import contract checks.

    These tests inspect the source code's structure without running the GUI.
    They fail if on_scrape_done's signature or imports drift from the contract.
    """

    def test_signature(self):
        """Layer 1 — exact signature check with type annotations.

        WHAT: Confirms on_scrape_done takes exactly four required parameters
              named "window", "new", "total", and "errors" and declares a
              return type of None. Also verifies type annotations: new=int,
              total=int, errors=list.

        WHY TYPE ANNOTATIONS:
          The signal connection passes (new, total, errors) from the ScrapeThread.
          The GUI expects these types: new and total are article counts (ints),
          errors is a list of error dicts. Wrong types would cause runtime errors
          in string formatting and iteration.

        OPTIONS:
          - Parameter "window": POSITIONAL_OR_KEYWORD, no default, no type annotation
          - Parameter "new": POSITIONAL_OR_KEYWORD, no default, annotated int
          - Parameter "total": POSITIONAL_OR_KEYWORD, no default, annotated int
          - Parameter "errors": POSITIONAL_OR_KEYWORD, no default, annotated list
          - Return type: annotated None

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when the signature and annotations match exactly.

        ERRORS/EDGE CASES:
          - Wrong parameter name/kind/default: params mismatch
          - Missing or wrong type annotation: annotation assertion fails
          - Missing return annotation: return_annotation != None fails

        HOW TO TEST: Change "new" to "count" in the source, then run —
                     it should fail with a params mismatch.
        """
        import inspect
        from gui._36_scrape_finished_signal_handler.on_scrape_done import on_scrape_done
        sig = inspect.signature(on_scrape_done)
        params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
        assert params == [
            ("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
            ("new", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
            ("total", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
            ("errors", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ]
        # Type annotations
        assert sig.parameters["new"].annotation is int
        assert sig.parameters["total"].annotation is int
        assert sig.parameters["errors"].annotation is list
        assert sig.return_annotation is None

    def test_source_imports(self):
        """Layer 1 — source import check.

        WHAT: Verifies the source file imports all three collaborators:
          - gui._10_log_append_timestamped_message.append_timestamped_log
            (for append_log_message — writes completion/error logs)
          - gui._13_stats_badges_update_live.update_stats_badges
            (for update_stats_badges — refreshes header stat badges)
          - gui._18_articles_table_refresh_view.refresh_articles_table
            (for refresh_articles_table — updates the articles table)

        WHY THIS MATTERS:
          on_scrape_done cannot log results without append_log_message, cannot
          update stats without update_stats_badges, and cannot show new articles
          without refresh_articles_table. All three are essential for the
          completion-handling pipeline.

        OPTIONS: Expected set is exactly the three modules listed above.

        DEFAULTS: N/A.

        OUTPUT/EFFECT: Passes when all three imports exist in the source.

        ERRORS/EDGE CASES:
          - Missing import: "Missing imports: [...]" naming the module

        HOW TO TEST: Rename one import path in the source, then run —
                     it should fail and name the missing module.
        """
        from tests.GUI.conftest import assert_source_imports
        module_path = "gui._36_scrape_finished_signal_handler.on_scrape_done"
        assert_source_imports(
            importlib.util.find_spec(module_path).origin,
            {
                "gui._10_log_append_timestamped_message.append_timestamped_log",
                "gui._13_stats_badges_update_live.update_stats_badges",
                "gui._18_articles_table_refresh_view.refresh_articles_table",
            },
        )


# ===========================================================================
# Layer 2 — Behavioral smoke tests
# ===========================================================================

class TestLayer2_Behavioral:
    """Behavioral smoke tests against the real on_scrape_done function.

    These tests call the REAL on_scrape_done against a fake window while
    verifying UI state transitions, log output, and downstream function calls.
    """

    def test_re_enables_button_and_hides_progress(self, qapp):
        """Layer 2 — sync button re-enabled and progress bar hidden on completion.

        WHAT: After a scrape completes, the sync button must be re-enabled so the
              user can trigger another sync, and its text must revert to "🔄 Sync
              All Feeds". The progress bar must be hidden to return the UI to
              its idle visual state.

        WHY THIS MATTERS:
          If the button stays disabled, the user cannot sync again. If the
          progress bar stays visible, the UI looks broken. These are the two
          most visible signs that the scrape finished successfully.

        OPTIONS:
          - new=5, total=100, errors=[] (successful scrape with 5 new articles)
          - All widget interactions are recorded by MagicMock

        DEFAULTS: qapp provides headless Qt context.

        OUTPUT/EFFECT: btn_sync.setEnabled(True), btn_sync.setText("🔄 Sync All Feeds"),
                       progress.setVisible(False) — each called exactly once.

        ERRORS/EDGE CASES:
          - Button not re-enabled: setEnabled assertion fails
          - Wrong button text: setText assertion fails
          - Progress bar not hidden: setVisible assertion fails

        HOW TO TEST: Remove the setEnabled(True) call from the source, then
                     run — the test should fail on the setEnabled assertion.
        """
        from gui._36_scrape_finished_signal_handler.on_scrape_done import on_scrape_done
        w = _make_window()
        on_scrape_done(w, 5, 100, [])
        w.btn_sync.setEnabled.assert_called_once_with(True)
        w.btn_sync.setText.assert_called_once_with("🔄 Sync All Feeds")
        w.progress.setVisible.assert_called_once_with(False)

    def test_logs_completion_and_errors(self, qapp):
        """Layer 2 — completion log appended; error-summary log when errors exist.

        WHAT: The function must append a completion log message with the article
              counts, and if errors occurred, append a second log message
              summarizing the error count.

        WHY LOG MESSAGES:
          The operations log console is the primary audit trail. Users and
          developers check it to verify what happened during a scrape run.
          Without logs, failures are invisible.

        OPTIONS:
          - Test with 1 error: [{"feed_name": "BBC", "error": "404"}]
          - append_log_message is mocked to record calls

        DEFAULTS: qapp provides headless Qt context.

        OUTPUT/EFFECT:
          - Completion message logged: "Scrape job complete: +3 new article(s)..."
          - Error summary logged: "Encountered 1 feed fetching issue(s)."

        ERRORS/EDGE CASES:
          - No log messages at all: assert_any_call fails
          - Missing error summary when errors present: assertion fails

        HOW TO TEST: Remove the errors conditional block from the source, then
                     run with errors=[...] — the error summary message would
                     be missing and the test should fail.
        """
        from gui._36_scrape_finished_signal_handler.on_scrape_done import on_scrape_done
        w = _make_window()
        with patch("gui._36_scrape_finished_signal_handler.on_scrape_done.append_log_message") as mock_log:
            on_scrape_done(w, 3, 50, [{"feed_name": "BBC", "error": "404"}])
            mock_log.assert_any_call(
                w, "Scrape job complete: +3 new article(s) added. Total database count: 50."
            )
            mock_log.assert_any_call(w, "Encountered 1 feed fetching issue(s).")

    def test_calls_update_stats_and_refresh_articles(self, qapp):
        """Layer 2 — stats badges updated and articles table refreshed on completion.

        WHAT: After a scrape completes, the function must call update_stats_badges
              and refresh_articles_table so the UI reflects the new data.

        WHY BOTH CALLS:
          update_stats_badges refreshes the header badges (article count, feed
          count) and refresh_articles_table updates the articles table to show
          any newly fetched articles. Both are essential for the UI to reflect
          the scrape results accurately.

        OPTIONS:
          - new=5, total=100, errors=[] (normal completion)
          - Both downstream functions are mocked to record calls

        DEFAULTS: qapp provides headless Qt context.

        OUTPUT/EFFECT:
          - update_stats_badges(w) called exactly once
          - refresh_articles_table(w) called exactly once

        ERRORS/EDGE CASES:
          - Stats not updated: assert_called_once_with fails
          - Articles table not refreshed: assert_called_once_with fails

        HOW TO TEST: Remove the update_stats_badges call from the source, then
                     run — the test should fail on the assert_called_once_with.
        """
        from gui._36_scrape_finished_signal_handler.on_scrape_done import on_scrape_done
        w = _make_window()
        with patch("gui._36_scrape_finished_signal_handler.on_scrape_done.update_stats_badges") as mock_stats, \
             patch("gui._36_scrape_finished_signal_handler.on_scrape_done.refresh_articles_table") as mock_refresh:
            on_scrape_done(w, 5, 100, [])
            mock_stats.assert_called_once_with(w)
            mock_refresh.assert_called_once_with(w)
