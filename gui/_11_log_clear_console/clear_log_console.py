"""Clear all messages from the operations log console."""
# WHAT: Clears window.log_box.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Log console becomes empty.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: clear_log_console(window); assert window.log_box.toPlainText() == ""


def clear_log_console(window) -> None:
    """Clear the operations log console."""
    window.log_box.clear()
