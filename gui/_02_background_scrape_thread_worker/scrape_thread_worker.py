"""Background QThread worker that downloads feeds in parallel."""
# ==============================================================================
# OVERVIEW
# In PyQt6, the main window runs in the "main thread" and if you do slow work
# (like downloading RSS feeds over the internet) on that same thread, the GUI
# freezes — buttons stop responding, the window looks stuck.
#
# ScrapeThread solves this by doing the download work in a SECONDARY background
# thread, while the main window stays responsive. It emits two signals back to
# the main thread: one for log messages and one for the final results.
#
# WHAT: Defines the ScrapeThread class which inherits from QThread. When started,
#       it downloads all feeds in parallel (via fetch_all_feeds), saves new
#       articles to disk (via save_articles), and emits results back to the GUI.
#
# OPTIONS: feeds — list of feed dictionaries (each dict has keys like 'name',
#             'url', 'enabled'). The thread makes a deep copy so it works on its
#             own snapshot and won't be affected if the user adds/deletes feeds
#             while the download is running.
#          parent — optional QObject parent for PyQt6's memory management (rarely needed).
#
# DEFAULTS: N/A — both parameters are required by design.
#
# OUTPUT/EFFECT: Two signals are emitted back to the main thread:
#                 log_signal(str)           — progress and status messages
#                 finished_signal(int,int,list) — (new_articles, total_articles, errors)
#               Side-effect: articles are saved to disk via core.storage.save_articles.
#
# ERRORS/EDGE CASES:
#   - If fetch_all_feeds or save_articles raises an unexpected exception,
#     the except block catches it and emits finished_signal(0, 0, [error_dict]).
#     The error dict has keys: {"feed_name": "System", "error": "<message>"}.
#   - If no errors occur, the third element of finished_signal is an empty list [].
#
# HOW TO TEST: from gui._02_background_scrape_thread_worker.scrape_thread_worker import ScrapeThread
#              Then create: thread = ScrapeThread(feeds=[], parent=None)
#              Connect to signals and call thread.start()
# ==============================================================================
# copy: Python's standard library module for making deep copies of data structures.
#   We use deepcopy so the background thread gets its own independent copy of the
#   feeds list. Without it, the main thread could modify the list while the
#   background thread is reading it, causing crashes or missed feeds.
import copy

# PyQt6.QtCore: the core module of PyQt6 containing threading, signals, and basic types.
# QThread: a class that lets you run code in a separate OS-level thread.
# pyqtSignal: a decorator that creates a signal — a way for a thread to send
#             messages back to the main thread safely.
from PyQt6.QtCore import QThread, pyqtSignal

# core.fetcher.fetch_all_feeds: downloads all RSS/Atom feeds from the provided list.
#   Returns (articles_list, errors_list) where articles_list contains parsed article data
#   and errors_list contains dicts describing any feeds that failed to download.
from core.fetcher import fetch_all_feeds
# core.storage.save_articles: deduplicates and persists articles to disk storage.
#   Returns (new_count, total_count) where new_count is how many articles were newly saved
#   and total_count is the new total in the database.
from core.storage import save_articles


class ScrapeThread(QThread):
    """Background thread that downloads RSS feeds without freezing the GUI.

    WHAT: Inherits from QThread so its run() method executes in a separate OS thread.
          The main window stays responsive while this thread does the slow network work.

    SIGNALS:
      log_signal (pyqtSignal(str)):
        Emits a human-readable message string back to the main thread.
        Used for progress updates like "Downloading TechCrunch..." or error messages.
        Valid test values: any non-empty string. Example: "Starting scrape..."
      finished_signal (pyqtSignal(int, int, list)):
        Emits three values when the scrape completes or fails:
          [0] new — number of NEW articles saved this run (int, >= 0)
          [1] total — total article count in the database after this run (int, >= 0)
          [2] errors — list of error dicts; empty [] if no errors occurred
        Each error dict has keys: {"feed_name": str, "error": str}
    """
    # log_signal: emitted throughout the scrape to report progress to the GUI.
    #   Connect it to a function that appends text to the log console.
    #   Options: any string message. Typical values:
    #     "Initializing parallel feed scrape process..."
    #     "Scrape Error: <error message>"
    log_signal = pyqtSignal(str)

    # finished_signal: emitted exactly once when the scrape completes (success or failure).
    #   Connect it to on_done(new, total, errors) in the main window.
    #   Options for the three parameters:
    #     new: int >= 0 (e.g., 0 if no new articles found, 15 if 15 new articles downloaded)
    #     total: int >= 0 (e.g., 150 total articles in database)
    #     errors: list of dicts; empty [] on success, [{"feed_name": "...", "error": "..."}] on failure
    finished_signal = pyqtSignal(int, int, list)

    def __init__(self, feeds, parent=None):
        """Initialize the background scrape thread.

        WHAT: Called when you create a new ScrapeThread instance. Stores a copy
              of the feeds list so the thread works independently.

        OPTIONS:
          feeds: list of feed dicts. Each dict should have at minimum:
            - 'name' (str): feed display name, e.g. "TechCrunch"
            - 'url' (str): RSS endpoint URL, e.g. "https://techcrunch.com/feed/"
            - 'enabled' (bool): whether to download this feed (default True)
            - 'fetch_interval_hours' (int): how often to check (1, 3, 6, 12, or 24)
          parent: optional Qt parent object for memory management. Usually None.
                  If provided, the thread is automatically cleaned up when parent is destroyed.

        DEFAULTS: parent defaults to None (no automatic cleanup).
        """
        # super().__init__(parent) calls QThread's constructor to initialize
        # the underlying OS thread infrastructure. parent is passed through.
        super().__init__(parent)
        # copy.deepcopy(feeds) creates a completely independent clone of the
        # feeds list and all its nested dicts. This prevents race conditions:
        # if the user adds/deletes feeds in the GUI while this thread is running,
        # the thread continues with its original snapshot instead of crashing.
        # Example: if feeds = [{"name": "CNN", ...}, {"name": "BBC", ...}]
        # then self.feeds becomes an identical but separate list.
        self.feeds = copy.deepcopy(feeds)

    def run(self):
        """Main entry point — called automatically when thread.start() is invoked.

        WHAT: This method runs in the BACKGROUND thread (not the GUI thread).
              It downloads all feeds, saves articles, then signals completion.

        STEPS:
          1. Emit a start message via log_signal.
          2. Call fetch_all_feeds() to download all enabled feeds in parallel.
          3. Call save_articles() to deduplicate and persist new articles to disk.
          4. Emit finished_signal with (new_count, total_count, errors).
          5. If ANY step raises an exception, catch it and emit an error result.

        ERRORS/EDGE CASES:
          - If fetch_all_feeds raises an exception (e.g., network failure),
            we catch it, log the error, and emit finished_signal(0, 0, [error_dict]).
          - If save_articles raises (e.g., disk full), same catch-and-emit behavior.
          - On success, errors list is empty: finished_signal.emit(new, total, [])
        """
        try:
            # Emit a progress message to the GUI log.
            # self.log_signal.emit() sends the string back to the main thread
            # where it will be appended to the operations log console.
            self.log_signal.emit("Initializing parallel feed scrape process...")
            # fetch_all_feeds downloads all feeds in parallel using async/concurrent techniques.
            # progress_callback=self.log_signal.emit means each progress update
            # (e.g., "Downloading TechCrunch...") is sent directly to the GUI log.
            # Returns: (articles, errors)
            #   articles: list of article dicts with keys like 'title', 'url', 'content', 'feed_name'
            #   errors: list of error dicts for feeds that failed to download
            articles, errors = fetch_all_feeds(self.feeds, progress_callback=self.log_signal.emit)
            # save_articles deduplicates articles (by URL) and writes new ones to disk.
            # Returns: (new_count, total_count)
            #   new_count: how many articles were actually saved this run
            #   total_count: total articles in the database after this run
            new, total = save_articles(articles)
            # Emit completion signal back to the main thread's on_done handler.
            # Example values: new=5, total=150, errors=[] (success)
            #                  new=0, total=148, errors=[{"feed_name":"BBC","error":"404"}]
            self.finished_signal.emit(new, total, errors)
        except Exception as e:
            # This catches ANY unexpected error during the entire scrape process.
            # Exception e could be: NetworkError, JSONDecodeError, TypeError, etc.
            # We emit the error message to the log and a failure result signal.
            self.log_signal.emit(f"Scrape Error: {e}")
            # Emit failure result: 0 new, 0 total, one error dict.
            # The error dict uses "System" as feed_name to indicate a global failure
            # (as opposed to a per-feed failure which would have the actual feed name).
            self.finished_signal.emit(0, 0, [{"feed_name": "System", "error": str(e)}])
