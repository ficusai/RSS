"""Thin compatibility facade — re-exports MainWindow from the modular assembly."""
# WHAT: This file exists so that existing imports like `from gui.window import MainWindow`
#       continue to work. All logic lives in the _NN_* atomic modules under gui/.
#       It does NOT support standalone execution (python3 gui/window.py is not valid).
#       The real entry point is gui._38_bootstrap_launch_window.bootstrap_launch_window.launch_gui_window().
# OPTIONS: N/A
# DEFAULTS: N/A
# OUTPUT/EFFECT: Exports the MainWindow class.
# ERRORS/EDGE CASES: Import errors propagate from the facade module.
# HOW TO TEST: from gui.window import MainWindow
from gui._37_main_window_facade_assembly.main_window_facade import MainWindow
