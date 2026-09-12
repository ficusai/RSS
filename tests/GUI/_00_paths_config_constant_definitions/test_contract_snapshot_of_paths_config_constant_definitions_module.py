"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_00_paths_config_constant_definitions/paths_config_constants.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file is a "contract test" — it ensures that the paths_config_constants.py
module exposes exactly three public constants with exact values, and nothing
else (no functions, no extra constants). These constants are imported by
every other GUI module, so any drift would break the entire application.

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_file_exists            : The source .py file is present on disk
  - test_import_health          : The module can be imported without errors
  - test_ast_imports            : The module imports exactly {'pathlib'}
  - test_project_root_is_path   : PROJECT_ROOT is a pathlib.Path pointing to RSS/
  - test_config_path_constant   : CONFIG_PATH == PROJECT_ROOT / "config" / "feeds.json"
  - test_assets_dir_constant    : ASSETS_DIR == PROJECT_ROOT / "assets"
  - test_no_public_callables    : No public functions are defined (constants-only module)
  - test_constants_values       : All three constants have exact expected values

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# ast: Python's Abstract Syntax Tree module.
#   Used to parse source code into a tree of nodes, then walk that tree to
#   find all import statements. This is more reliable than string/grep matching
#   because it understands Python syntax (multi-line imports, parentheses, etc.).
import ast
# inspect: Python's introspection module.
#   Used to examine live objects (functions, classes, parameters, defaults).
#   Here we use it to check for public functions in the imported module.
import inspect
# sys: Python's system module.
#   sys.path is a list of directories Python searches when importing modules.
#   We insert the project root so `import gui._00_...` works from the test directory.
import sys
# pathlib.Path: cross-platform file path manipulation.
#   Path("/a") / "b" produces PosixPath("a/b") or WindowsPath("a\\b").
from pathlib import Path

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# This tells PyQt6 to render to a virtual screen instead of opening a real window,
# which is required for headless test runners (CI, SSH, etc.).
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    """Return the absolute filesystem path to the source module under test.

    WHAT: Constructs the path to paths_config_constants.py by navigating up
          three directory levels from this test file:
            tests/GUI/_00_... → tests/GUI → tests → RSS (project root)
          Then appends gui/_00_paths_config_constant_definitions/paths_config_constants.py.

    OPTIONS: None — this function takes no parameters.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns a Path object like:
                   /home/ficus-pro/Documents/RSS/gui/_00_paths_config_constant_definitions/paths_config_constants.py

    ERRORS/EDGE CASES: None. Path construction never raises.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_00_paths_config_constant_definitions" / "paths_config_constants.py"


def _import_module():
    """Import the source module and return it.

    WHAT: Uses Python's standard import system to load gui._00_paths_config_constant_definitions.paths_config_constants.
          The sys.path.insert() in the module header ensures Python can find it.

    OPTIONS: None — this function takes no parameters.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns the imported module object. You can then access
                   mod.PROJECT_ROOT, mod.CONFIG_PATH, mod.ASSETS_DIR.

    ERRORS/EDGE CASES:
      - ImportError if the module path is wrong or the package __init__.py is missing
      - ModuleNotFoundError if PyQt6 is not installed (not applicable here since no Qt deps)
    """
    import gui._00_paths_config_constant_definitions.paths_config_constants as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence.

    WHAT: Asserts that the source file actually exists on disk at the expected path.
          This is the most basic sanity check — if the file is missing, no other
          tests can run meaningfully.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if the file exists; raises AssertionError with the file path if not.

    ERRORS/EDGE CASES:
      - FileNotFoundError: the source file was deleted or moved
      - PermissionError: cannot access the file (rare on local dev)

    HOW TO TEST: Delete the source file, then run: pytest test_contract_snapshot_of_paths_config_constant_definitions_module.py::test_file_exists
                 The test should fail with the missing file path in the message.
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health.

    WHAT: Verifies that the source module can be imported without any exceptions.
          A module might exist on disk but have syntax errors, missing dependencies,
          or circular import issues. This test catches all of those.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns the imported module object (assigned to `mod`).
                   If import succeeds, mod is a valid module object (truthy).

    ERRORS/EDGE CASES:
      - SyntaxError in source: import fails with SyntaxError
      - Missing dependency (e.g., pathlib not available): ImportWarning or ImportError
      - Circular import: RecursionError or ImportError

    HOW TO TEST: Introduce a syntax error in paths_config_constants.py (e.g., remove a colon),
                 then run this test. It should fail.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports.

    WHAT: Parses the source file's Abstract Syntax Tree (AST) and checks that
          the module imports exactly the set {'pathlib'} and nothing else.
          This prevents accidental addition of unused imports or removal of required ones.

    HOW IT WORKS:
      1. ast.parse() reads the .py file and builds a tree of Python syntax nodes
      2. ast.walk() traverses every node in that tree
      3. For each Import node (e.g., "import os"), we extract the module name "os"
      4. For each ImportFrom node (e.g., "from pathlib import Path"), we extract "pathlib"
      5. We compare the found set against the expected set {'pathlib'}

    OPTIONS: The expected set is hardcoded as {"pathlib"}. This is the ONLY import
             this module should have. No Qt imports, no core imports, nothing else.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if found == expected; raises AssertionError listing missing/extra imports.

    ERRORS/EDGE CASES:
      - If a new import is added to the source: "Unexpected imports: ['something']"
      - If pathlib is removed: "Missing imports: ['pathlib']"
      - Multi-line imports or parentheses are handled correctly by AST (unlike grep)

    HOW TO TEST: Add "import os" to paths_config_constants.py and re-run.
                 The test should fail with "Unexpected imports: ['os']".
    """
    expected = {"pathlib"}
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        # ast.Import handles: "import os", "import os, sys"
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        # ast.ImportFrom handles: "from pathlib import Path", "from . import foo"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, f"Missing imports: {sorted(missing)}"


def test_project_root_is_path():
    """Layer 1 — PROJECT_ROOT is a Path object equal to the RSS project root.

    WHAT: Verifies two things about PROJECT_ROOT:
          1. It is an instance of pathlib.Path (not a plain string)
          2. It points to the RSS project root directory (3 levels up from this test file)

    WHY THIS MATTERS:
          Every other GUI module imports PROJECT_ROOT to find config paths, assets, etc.
          If this constant were a string instead of a Path, all downstream code using
          "/" path operators would break at runtime.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if PROJECT_ROOT is a Path pointing to the RSS root.

    ERRORS/EDGE CASES:
      - If PROJECT_ROOT is a str: AssertionError from isinstance check
      - If the path is wrong: AssertionError from equality check

    HOW TO TEST: Change PROJECT_ROOT to a string ("abc") in the source.
                 Run this test — it should fail the isinstance check.
    """
    mod = _import_module()
    # isinstance(x, Path): checks that x is a pathlib.Path object, not a str.
    assert isinstance(mod.PROJECT_ROOT, Path)
    # Path(__file__).resolve().parents[3]: goes up 3 levels from this test file:
    #   parents[0] = _00_paths_config_constant_definitions/
    #   parents[1] = GUI/
    #   parents[2] = tests/
    #   parents[3] = RSS/  (project root)
    assert mod.PROJECT_ROOT == Path(__file__).resolve().parents[3]


def test_config_path_constant():
    """Layer 1 — CONFIG_PATH equals PROJECT_ROOT / "config" / "feeds.json".

    WHAT: Verifies that CONFIG_PATH is constructed correctly by joining PROJECT_ROOT
          with the sub-paths "config" and "feeds.json". This is where the app stores
          the user's RSS feed subscriptions as JSON.

    WHY THIS MATTERS:
          If CONFIG_PATH pointed to the wrong location, the app would either:
          - Read from an empty/nonexistent file (no feeds loaded)
          - Write to an unexpected location (data lost between runs)
          The exact path must match what the rest of the codebase expects.

    OPTIONS: The expected path segments are fixed: "config" and "feeds.json".
             Changing these would require updating every module that uses CONFIG_PATH.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if CONFIG_PATH == PROJECT_ROOT / "config" / "feeds.json".

    ERRORS/EDGE CASES:
      - Wrong parent directory: path would point to wrong location
      - Wrong filename: app would look for "feeds.json" but config stored elsewhere

    HOW TO TEST: Change "feeds.json" to "feeds2.json" in the source.
                 Run this test — it should fail the equality assertion.
    """
    mod = _import_module()
    assert mod.CONFIG_PATH == mod.PROJECT_ROOT / "config" / "feeds.json"


def test_assets_dir_constant():
    """Layer 1 — ASSETS_DIR equals PROJECT_ROOT / "assets".

    WHAT: Verifies that ASSETS_DIR points to the assets folder where the app
          stores icons, images, and other static files (like ficus.png for the window icon).

    WHY THIS MATTERS:
          The window icon and other UI assets are loaded from this directory.
          If ASSETS_DIR is wrong, the app starts without icons and may show
          broken image placeholders.

    OPTIONS: The expected sub-path is fixed: "assets". Changing this would
             require moving all asset files or updating all references.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if ASSETS_DIR == PROJECT_ROOT / "assets".

    ERRORS/EDGE CASES:
      - Wrong folder name: asset loading fails silently (Qt shows missing icon)
      - Relative path instead of absolute: breaks when run from different directories

    HOW TO TEST: Change "assets" to "images" in the source.
                 Run this test — it should fail the equality assertion.
    """
    mod = _import_module()
    assert mod.ASSETS_DIR == mod.PROJECT_ROOT / "assets"


def test_no_public_callables():
    """Layer 1 — no public functions or classes are defined in this module.

    WHAT: Uses Python's inspect module to check that this module contains NO
          public (non-underscore-prefixed) functions or classes. This is a
          constants-only module — adding functions would violate its design.

    HOW IT WORKS:
      1. inspect.getmembers(mod, inspect.isfunction) finds all functions in the module
      2. We filter to only functions defined IN this module (obj.__module__ == mod.__name__)
      3. We exclude private/dunder names (starting with "_")
      4. The resulting set must be empty

    OPTIONS: None. This module should NEVER define any public callables.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if no public callables exist; fails listing any extras found.

    ERRORS/EDGE CASES:
      - If a function is accidentally added: AssertionError listing the unexpected name
      - Imported functions from other modules are correctly ignored (__module__ check)

    HOW TO TEST: Add "def dummy(): pass" to paths_config_constants.py.
                 Run this test — it should fail with "Unexpected public callables: ['dummy']".
    """
    mod = _import_module()
    # inspect.getmembers(mod, inspect.isfunction): returns (name, func) pairs for ALL
    # functions defined anywhere in the module (including inherited ones).
    # We filter by __module__ to only get functions actually defined in this module.
    defined = {
        name
        for name, obj in inspect.getmembers(mod, inspect.isfunction)
        if obj.__module__ == mod.__name__ and not name.startswith("_")
    }
    # assert not defined: passes only if the set is empty (no public functions)
    assert not defined, f"Unexpected public callables: {sorted(defined)}"


def test_constants_values():
    """Layer 1 — all three constants have exact expected values.

    WHAT: Final comprehensive check that PROJECT_ROOT, CONFIG_PATH, and ASSETS_DIR
          all have the exact values this test expects. This is a combined sanity
          check that catches any accidental modification of any constant.

    WHY COMBINED: Running as one test instead of three makes it easier to see
                  at a glance which constants are correct/incorrect in test output.

    OPTIONS: The expected values are derived from the project structure:
             - PROJECT_ROOT = Path(__file__).resolve().parents[3] (RSS/ dir)
             - CONFIG_PATH = PROJECT_ROOT / "config" / "feeds.json"
             - ASSETS_DIR = PROJECT_ROOT / "assets"

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if all three constants match; fails on first mismatch.

    ERRORS/EDGE CASES:
      - Any constant being a string instead of Path: AssertionError
      - Any constant pointing to wrong directory: AssertionError

    HOW TO TEST: Modify any constant in the source and re-run. The test will
                 report exactly which constant changed.
    """
    mod = _import_module()
    # Verify PROJECT_ROOT points to the RSS project root (3 levels up from tests/GUI/_XX/)
    assert mod.PROJECT_ROOT == Path(__file__).resolve().parents[3]
    # Verify CONFIG_PATH includes the config/feeds.json path
    assert mod.CONFIG_PATH == mod.PROJECT_ROOT / "config" / "feeds.json"
    # Verify ASSETS_DIR points to the assets folder
    assert mod.ASSETS_DIR == mod.PROJECT_ROOT / "assets"
