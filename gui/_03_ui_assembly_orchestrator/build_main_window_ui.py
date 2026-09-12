"""Build the complete MainWindow UI: central widget, header, progress bar, 4 tabs."""
# WHAT: Orchestrates UI assembly — creates central widget, root layout, header bar,
#       progress bar, QTabWidget, and calls the four tab builders.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: All Qt widgets on the window are constructed.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: build_main_window_ui(window); assert window.tabs.count() == 4
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from gui._04_ui_header_bar_top_section_build.build_header_bar import build_header_bar
from gui._05_ui_articles_explorer_tab_build.build_articles_tab import build_articles_tab
from gui._06_ui_subscriptions_hub_tab_build.build_subscriptions_tab import build_subscriptions_tab
from gui._07_ui_operations_system_tab_build.build_operations_tab import build_operations_tab
from gui._08_ui_presets_library_tab_build.build_presets_tab import build_presets_tab


def build_main_window_ui(window) -> None:
    """Assemble the full MainWindow UI layout."""
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    layout.setSpacing(12)
    layout.setContentsMargins(16, 16, 16, 16)

    build_header_bar(window)

    window.progress = QProgressBar()
    window.progress.setTextVisible(False)
    window.progress.setVisible(False)
    layout.addWidget(window.progress, 0, Qt.AlignmentFlag.AlignRight)

    window.tabs = QTabWidget()
    layout.addWidget(window.tabs)

    build_articles_tab(window)
    build_subscriptions_tab(window)
    build_operations_tab(window)
    build_presets_tab(window)
