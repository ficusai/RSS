"""Apply the dark modern QSS stylesheet to a QMainWindow instance."""
# ==============================================================================
# OVERVIEW
# PyQt6 uses Qt Style Sheets (QSS) — a syntax very similar to CSS — to style
# every widget in the application. This file holds the entire stylesheet as a
# single string constant called STYLESHEET, and provides one function that
# applies it to the main window.
#
# WHAT: Defines STYLESHEET (a multi-line string of QSS rules) and
#       apply_window_stylesheet() which calls window.setStyleSheet(STYLESHEET).
#
# OPTIONS: window — must be a QMainWindow instance or a subclass of it.
#          Passing anything else will silently be ignored by Qt (no error,
#          but the style will not be applied to your widget).
#
# DEFAULTS: None — the caller must provide a valid window.
#
# OUTPUT/EFFECT: The entire window and all its child widgets receive the
#                dark GitHub-inspired color scheme defined in STYLESHEET.
#
# ERRORS/EDGE CASES: None. setStyleSheet() accepts any string without validation.
#                    If the string is empty, Qt simply keeps the default style.
#
# HOW TO TEST: from gui._01_window_stylesheet_dark_modern_theme.window_stylesheet_apply import STYLESHEET, apply_window_stylesheet
#              assert len(STYLESHEET) > 0   -- the stylesheet string is not empty
#              Running the app and observing a dark-themed window confirms it works.
# ==============================================================================
# The triple-quoted string below is a Qt Style Sheet (QSS). It uses selectors
# like CSS: "QPushButton" targets all buttons, "QPushButton#accent" targets
# only buttons with objectName="accent", and pseudo-states like ":hover"
# apply when the mouse is over the widget.
STYLESHEET = """
QMainWindow { background-color: #090d16; color: #e6edf3; }
QWidget { font-family: "Segoe UI", system-ui, -apple-system, sans-serif; font-size: 16px; color: #e6edf3; }

/* Tabs */
QTabWidget::pane { border: 1px solid #21262d; border-radius: 8px; background: #0d1117; top: 0; }
QTabBar::tab {
    background: #161b22; color: #8b949e;
    border: 1px solid #21262d; border-bottom: none;
    border-top-left-radius: 8px; border-top-right-radius: 8px;
    padding: 12px 24px; font-size: 16px; font-weight: 600;
    min-height: 44px; margin-right: 4px;
}
QTabBar::tab:selected { background: #0d1117; color: #58a6ff; border-top: 3px solid #58a6ff; }
QTabBar::tab:hover { background: #1c2128; color: #c9d1d9; }

/* Cards & Containers */
QFrame#card {
    background-color: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
}

/* Input Controls */
QLineEdit {
    background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
    padding: 10px 14px; color: #e6edf3; font-size: 16px;
    min-height: 44px;
}
QLineEdit:focus { border-color: #58a6ff; background: #11161d; }
QLineEdit::placeholder { color: #6e7681; }

/* Buttons */
QPushButton {
    background: #21262d; color: #e6edf3; border: 1px solid #363b42;
    border-radius: 6px; padding: 10px 20px; font-size: 16px; font-weight: 600;
    min-height: 44px; min-width: 90px;
}
QPushButton:hover { background: #30363d; border-color: #58a6ff; color: #ffffff; }
QPushButton:pressed { background: #1f6feb; color: #ffffff; }
QPushButton:disabled { background: #161b22; color: #484f58; border-color: #21262d; }

QPushButton#accent {
    background: #1a5a2e; color: #3fb950; border: 1px solid #238636;
    min-height: 44px; font-weight: 600;
}
QPushButton#accent:hover { background: #216e39; color: #56d364; border-color: #3fb950; }

QPushButton#primary_blue {
    background: #1f6feb; color: #ffffff; border: 1px solid #388bfd;
    min-height: 44px; font-weight: 600;
}
QPushButton#primary_blue:hover { background: #388bfd; border-color: #58a6ff; }

QPushButton#danger {
    background: #3d1818; color: #f85149; border: 1px solid #da3633;
    min-height: 44px; font-weight: 600;
}
QPushButton#danger:hover { background: #4e2020; color: #ff7b72; border-color: #f85149; }

QPushButton#chip {
    background: #161b22; color: #58a6ff; border: 1px solid #30363d;
    border-radius: 18px; padding: 6px 14px; font-size: 14px; font-weight: 600;
    min-height: 36px; min-width: 60px;
}
QPushButton#chip:hover { background: #1f6feb; color: #ffffff; border-color: #58a6ff; }

/* Tables */
QTableWidget {
    background: #0d1117; alternate-background-color: #121720;
    border: 1px solid #21262d; border-radius: 8px;
    color: #e6edf3; gridline-color: #21262d; font-size: 16px;
    selection-background-color: #1f6feb44; selection-color: #ffffff;
}
QHeaderView::section {
    background: #161b22; color: #8b949e;
    border-bottom: 2px solid #21262d; padding: 10px 14px;
    font-weight: 700; font-size: 16px; min-height: 46px;
}
QTableWidget::item { padding: 10px 14px; min-height: 46px; }

/* Text Editors */
QTextEdit {
    background: #0d1117; border: 1px solid #21262d; border-radius: 8px;
    color: #e6edf3; font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    font-size: 16px; padding: 14px; line-height: 1.6;
    min-height: 120px;
}

QTextEdit#log_console {
    background: #010409; border: 1px solid #21262d; border-radius: 6px;
    color: #7ee787; font-family: "Cascadia Code", "Fira Code", monospace;
    font-size: 15px; padding: 12px; line-height: 1.4;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #21262d; border-radius: 6px; text-align: center;
    background: #161b22; height: 8px;
}
QProgressBar::chunk { background: #1f6feb; border-radius: 4px; }

/* Dropdowns */
QComboBox {
    background: #0d1117; border: 1px solid #30363d; border-radius: 6px;
    padding: 10px 14px; color: #e6edf3; font-size: 16px;
    min-height: 44px; max-height: 48px;
}
QComboBox::drop-down { border: none; width: 32px; }
QComboBox QAbstractItemView {
    background: #161b22; color: #e6edf3; border: 1px solid #30363d;
    selection-background-color: #1f6feb44; font-size: 16px;
    min-height: 44px; padding: 6px;
}
QComboBox QAbstractItemView::item {
    min-height: 44px; padding: 10px;
}

/* Scrollbars */
QScrollBar:vertical { background: #0d1117; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #30363d; border-radius: 5px; min-height: 28px; }
QScrollBar::handle:vertical:hover { background: #484f58; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }

QScrollBar:horizontal { background: #0d1117; height: 10px; border-radius: 5px; }
QScrollBar::handle:horizontal { background: #30363d; border-radius: 5px; min-width: 28px; }
QScrollBar::handle:horizontal:hover { background: #484f58; }

/* Checkboxes */
QCheckBox { spacing: 10px; color: #e6edf3; font-size: 16px; min-height: 44px; padding: 4px; }
QCheckBox::indicator { width: 22px; height: 22px; border: 2px solid #30363d; border-radius: 5px; background: #0d1117; }
QCheckBox::indicator:checked { background: #1f6feb; border-color: #1f6feb; }
"""


def apply_window_stylesheet(window) -> None:
    """Apply the dark modern QSS stylesheet to *window*.

    WHAT: Calls window.setStyleSheet(STYLESHEET) so the entire window
          and all its children use the dark GitHub-inspired theme.

    OPTIONS: window — a QMainWindow instance (or subclass). Any Qt widget
             that inherits from QWidget will work, but the convention
             is to pass the main window.

    DEFAULTS: None.

    OUTPUT/EFFECT: Every widget in the window renders with the dark colors,
                   16px font, and styled borders defined above.

    ERRORS/EDGE CASES: None. Qt's setStyleSheet() is forgiving — it silently
                       ignores rules it does not understand.

    HOW TO TEST: Call this function on a MainWindow instance, then observe
                 that the window background is dark (#090d16) and buttons
                 have the accent green style when using objectName="accent".
    """
    # setStyleSheet: Qt method that takes a CSS-like string and applies it
    #               to this widget and all its children recursively.
    window.setStyleSheet(STYLESHEET)
