"""
GUI package for RSS Feed Manager & Scraper.
"""
# WHAT: Package initialization file for the 'gui' directory.
# This file marks the 'gui' folder as a Python package, allowing other scripts
# to import desktop interface screens, visual layouts, and user interface widgets.
# OPTIONS/VALUES: Contains PyQt6 GUI modules arranged as 39 atomic per-function
#   modules under gui/_00_... through gui/_38_.... The public entry class is
#   MainWindow, re-exported through the thin facade gui/window.py.
# DEFAULTS: Currently an empty package marker file.
# OUTPUT/EFFECT: Enables importing GUI modules via 'import gui' or 'from gui import ...'.
# ERRORS/EDGE CASES: Deleting this file may prevent Python from recognizing the 'gui' folder as an importable module.
# HOW TO TEST: Run 'python3 -c "import gui"' in terminal.
