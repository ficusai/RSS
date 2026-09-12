"""Module path and configuration constants for the RSS GUI."""
# ==============================================================================
# OVERVIEW
# This file exists so every GUI module shares the same file paths instead of
# each one calculating its own. Without it, moving the app to a different
# folder would break every module that has its own copy of the path logic.
#
# WHAT: Defines three read-only constants:
#         PROJECT_ROOT — where the RSS project lives on disk
#         CONFIG_PATH  — the JSON file storing user's feed subscriptions
#         ASSETS_DIR   — folder for app icons and images
#
# OPTIONS: None — these are package-level constants, no parameters to choose from.
#
# DEFAULTS: PROJECT_ROOT is resolved automatically from this file's location:
#             __file__ = ".../gui/_00_paths_config_constant_definitions/paths_config_constants.py"
#             parents[2] goes up two directories: gui -> gui root -> RSS project root
#             So PROJECT_ROOT = /home/ficus-pro/Documents/RSS
#
# OUTPUT/EFFECT: After this file is imported anywhere, three global constants
#                are available: PROJECT_ROOT, CONFIG_PATH, ASSETS_DIR.
#
# ERRORS/EDGE CASES: None. Path operations on valid string paths never raise.
#                    Even if the folder doesn't exist yet, pathlib still returns
#                    a Path object — it only errors if you try to read/write it.
#
# HOW TO TEST: from gui._00_paths_config_constant_definitions.paths_config_constants import CONFIG_PATH
#              assert str(CONFIG_PATH).endswith("config/feeds.json")
#              Running this should not raise any errors and the assertion should pass.
# ==============================================================================
from pathlib import Path
# pathlib.Path: a Python class for working with file system paths in an
#   operating-system-independent way. Path("a") / "b" becomes "a/b" (or "a\b" on Windows).

# PROJECT_ROOT — the top-level RSS directory where main.py lives.
# __file__ is an automatic Python variable holding the absolute path to THIS file.
# .resolve() converts it to a canonical absolute path (no ".." or symlinks).
# .parents[2] means "go up two directory levels":
#   parents[0] = _00_paths_config_constant_definitions/
#   parents[1] = gui/
#   parents[2] = RSS/   <-- this is the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# CONFIG_PATH — where feed subscription data is stored as JSON.
# The "feeds.json" file is created automatically if it does not exist.
# Options for the filename: any valid filename string. The app always uses "feeds.json".
CONFIG_PATH = PROJECT_ROOT / "config" / "feeds.json"

# ASSETS_DIR — folder containing app icons, images, and other static files.
# The app looks here for "ficus.png" to use as the window icon.
# Options: any folder name string. The app always uses the "assets" folder.
ASSETS_DIR = PROJECT_ROOT / "assets"
