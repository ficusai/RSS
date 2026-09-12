"""Copy the selected article's URL to the system clipboard."""
# WHAT: Reads window.btn_copy_link.property("url"), copies it to clipboard,
#       logs the action, and shows an information dialog.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: No-op if url property is missing.
# OUTPUT/EFFECT: Clipboard updated; log message appended; dialog shown.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: copy_article_link(window) after selecting an article
from PyQt6.QtWidgets import QApplication, QMessageBox

from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message


def copy_article_link(window) -> None:
    """Copy the selected article URL to the clipboard."""
    url = window.btn_copy_link.property("url")
    if url:
        QApplication.clipboard().setText(url)
        append_log_message(window, f"Copied URL to clipboard: {url}")
        QMessageBox.information(window, "Link Copied", "Article URL copied to clipboard!")
