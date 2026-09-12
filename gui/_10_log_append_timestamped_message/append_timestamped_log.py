"""Append a timestamped message to the operations log console."""
# WHAT: Adds '[HH:MM:SS] msg' to window.log_box and scrolls to bottom.
# OPTIONS: window — MainWindow instance; msg — log message string.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Log console gains one new line.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: append_log_message(window, "test") should add a line starting with [
from datetime import datetime


def append_log_message(window, msg: str) -> None:
    """Append a timestamped message to the live operations log."""
    ts = datetime.now().strftime("%H:%M:%S")
    window.log_box.append(f"[{ts}] {msg}")
    window.log_box.verticalScrollBar().setValue(window.log_box.verticalScrollBar().maximum())
