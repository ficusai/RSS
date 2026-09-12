"""Standalone GUI entry point — moved from gui/window.py __main__ block."""
# WHAT: Constructs a QApplication and MainWindow, shows the window, and runs the event loop.
# OPTIONS: sys.argv passed through to QApplication.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: GUI application starts and blocks until the window is closed.
# ERRORS/EDGE CASES: Requires a graphical display (X11/Wayland).
# HOW TO TEST: launch_gui_window() from an interactive Python session with a display
import sys

from PyQt6.QtWidgets import QApplication

from gui._37_main_window_facade_assembly.main_window_facade import MainWindow


def launch_gui_window() -> int:
    """Launch the RSS GUI application and return the exit code."""
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # Propagate tab page sizes so tables fill the window on first render.
    win._propagate_tab_sizes()
    return sys.exit(app.exec())
