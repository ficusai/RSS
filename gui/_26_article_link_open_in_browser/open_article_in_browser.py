"""Open the selected article's URL in the system default browser."""
# WHAT: Reads window.btn_open.property("url") and opens it via QDesktopServices.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: No-op if url property is missing.
# OUTPUT/EFFECT: Default browser opens the article URL.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: open_article_in_browser(window) after selecting an article
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices


def open_article_in_browser(window) -> None:
    """Open the selected article URL in the system browser."""
    url = window.btn_open.property("url")
    if url:
        QDesktopServices.openUrl(QUrl(url))
