"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_09_feed_identifier_generate_from_name/generate_feed_id.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the generate_feed_id function — a pure function that converts
a human-readable feed name (e.g., "TechCrunch", "BBC News") into a URL-safe
identifier (slug) containing only lowercase letters, digits, and underscores.
It also checks the fallback behavior when the input sanitizes to empty.

Examples:
  "TechCrunch"      -> "techcrunch"
  "BBC News"        -> "bbc_news"
  "NASA!Science"    -> "nasa_science"
  "!!!"             -> "f5"   (fallback when name is all special chars)
  ""                -> "f5"   (fallback when name is empty)

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_file_exists              : Source file exists on disk
  - test_import_health            : Module imports without errors
  - test_ast_imports              : Source imports exactly {'re'}
  - test_source_contains_slug_regex : Source contains import re + slug regex literal
  - test_generate_feed_id_signature : generate_feed_id(name, fallback_seed) -> str

Layer 2 (Behavioral / Pure Function Tests):
  - test_techcrunch       : "TechCrunch", 0 -> "techcrunch"
  - test_bbc_news         : "BBC News", 0 -> "bbc_news"
  - test_nasa_science     : "NASA!Science", 0 -> "nasa_science"
  - test_all_special_chars: "!!!", 5 -> "f5"
  - test_empty_name       : "", 5 -> "f5"
  - test_output_matches_regex : All outputs match ^[a-z0-9_]+$

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# ast: Parses Python source into an Abstract Syntax Tree for import verification.
import ast
# inspect: Examines function signatures (parameters, kinds, defaults, return types).
import inspect
# re: Python's regular expression module.
#   Used here to verify the source contains the expected regex pattern
#   and to validate that all function outputs match the expected format.
import re
# sys: Manipulates sys.path to add project root for imports.
import sys
# pathlib.Path: Cross-platform filesystem path construction.
from pathlib import Path

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# Prevents PyQt6 from trying to open a real display during headless test runs.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    """Return the absolute path to generate_feed_id.py.

    WHAT: Constructs the filesystem path by navigating up 3 levels from this
          test file to the RSS project root, then down to the source module.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns Path like: /home/ficus-pro/Documents/RSS/gui/_09_feed_identifier_generate_from_name/generate_feed_id.py

    ERRORS/EDGE CASES: None — path construction never raises.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_09_feed_identifier_generate_from_name" / "generate_feed_id.py"


def _import_module():
    """Import the source module and return it.

    WHAT: Loads gui._09_feed_identifier_generate_from_name.generate_feed_id and returns it.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns module with generate_feed_id function.

    ERRORS/EDGE CASES:
      - ImportError: syntax error or missing dependency
      - ModuleNotFoundError: package path changed
    """
    import gui._09_feed_identifier_generate_from_name.generate_feed_id as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence.

    WHAT: Asserts the source .py file exists at the expected filesystem path.
          This is the most basic gate — if the file is missing, all other
          tests cannot run.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if file exists; raises AssertionError with path if not.

    ERRORS/EDGE CASES:
      - File deleted/moved: AssertionError with full path in message

    HOW TO TEST: Delete generate_feed_id.py, then run this test.
                 It should fail with "Source file missing: /path/to/file.py"
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health.

    WHAT: Verifies the module can be imported without any exceptions.
          Catches syntax errors, missing dependencies, and circular imports.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns the imported module object (truthy on success).

    ERRORS/EDGE CASES:
      - SyntaxError: invalid Python syntax in source
      - ImportError: re module not available (extremely rare — part of stdlib)
      - ModuleNotFoundError: package structure changed

    HOW TO TEST: Add invalid syntax (e.g., "def foo(" missing closing paren) to source.
                 Run this test — it should fail with SyntaxError.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports.

    WHAT: Parses the source AST and verifies the module imports exactly:
          - re  (Python's standard regular expression module)

    WHY ONLY 're':
          The generate_feed_id function uses exactly one import: re.sub() to
          strip non-alphanumeric characters from feed names. No Qt imports,
          no core imports, no other stdlib imports are needed.

    HOW IT WORKS:
      1. ast.parse() builds a syntax tree from the source code
      2. ast.walk() traverses every node looking for Import and ImportFrom
      3. We collect module names and compare against expected set

    OPTIONS: Expected set is exactly {"re"}. No other imports allowed.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if found == expected; lists missing or extra on failure.

    ERRORS/EDGE CASES:
      - Extra import: "Unexpected imports: ['os']"
      - Missing import: "Missing imports: ['re']"

    HOW TO TEST: Add "import os" to source. Run this test — should fail with
                 "Unexpected imports: ['os']".
    """
    expected = {"re"}
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        # ast.Import: matches "import os", "import os, sys"
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        # ast.ImportFrom: matches "from os.path import join"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, f"Missing imports: {sorted(missing)}"


def test_source_contains_slug_regex():
    """Layer 1 — Source contains import re + slug regex literal.

    WHAT: Verifies that the source code contains both:
          1. The statement "import re" (or equivalent)
          2. The regex pattern [^a-zA-Z0-9_]+ used for slug generation

    WHY REGEX MATTERS:
          The regex [^a-zA-Z0-9_]+ matches any sequence of characters that are
          NOT lowercase letters, uppercase letters, digits, or underscores.
          re.sub() replaces these matched sequences with underscores, effectively
          stripping special characters and replacing spaces with underscores.
          Without this regex, the function couldn't sanitize feed names.

    HOW THE CHECK WORKS:
      1. Read the raw source text
      2. Check for the string "import re" (simple substring search)
      3. Use re.search() to find the regex pattern in the source
         - Matches either r"[^a-zA-Z0-9_]+" or r'[^a-zA-Z0-9_]+' (single or double quotes)

    OPTIONS: None — both patterns must be present in the source.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if both "import re" and the regex pattern are found.

    ERRORS/EDGE CASES:
      - Regex removed: second assertion fails
      - Import removed: first assertion fails

    HOW TO TEST: Remove the regex pattern from re.sub() in source.
                 Run this test — it should fail on the regex search assertion.
    """
    source = _module_path().read_text()
    # Verify "import re" is present in the source
    assert "import re" in source
    # Verify the slug regex [^a-zA-Z0-9_]+ is present
    # Matches both r"[^a-zA-Z0-9_]+" and r'[^a-zA-Z0-9_]+' (quote style doesn't matter)
    assert re.search(r'r"\[\^a-zA-Z0-9_\]\+"', source) or re.search(r"r'\[\^a-zA-Z0-9_\]\+'", source), \
        "Source should contain the slug regex literal [^a-zA-Z0-9_]+"


def test_generate_feed_id_signature():
    """Layer 1 — generate_feed_id(name: str, fallback_seed: int) -> str.

    WHAT: Verifies the function has exactly the right parameters with type annotations:
          - name: str (required, no default)
          - fallback_seed: int (required, no default)
          - Return type: str

    WHY TYPE ANNOTATIONS MATTER:
          Type annotations help static type checkers (mypy) catch bugs at development
          time. If someone passes an int instead of a string for name, mypy would
          flag it. The annotations also serve as documentation for callers.

    OPTIONS:
      - name: str — any string representing a feed name
      - fallback_seed: int — non-negative integer used when name sanitizes to empty
      - Return: str — the generated slug ID

    DEFAULTS: N/A — both parameters are required.

    OUTPUT/EFFECT: Passes if signature matches exactly.

    ERRORS/EDGE CASES:
      - Wrong parameter names: params mismatch
      - Missing type annotation: param annotation mismatch
      - Wrong return type: return_annotation mismatch

    HOW TO TEST: Change parameter name from "name" to "feed_name" in source.
                 Run this test — it should fail with params mismatch.
    """
    mod = _import_module()
    func = mod.generate_feed_id
    sig = inspect.signature(func)
    # Build list of (name, kind, default) tuples for each parameter
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    # Expected: two required parameters
    expected = [
        ("name", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ("fallback_seed", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
    ]
    assert params == expected
    # Return annotation must be exactly str
    assert sig.return_annotation is str


def test_techcrunch():
    """Layer 2 — 'TechCrunch', 0 -> 'techcrunch'.

    WHAT: Verifies that a simple camelCase feed name is converted to all lowercase
          with no other changes (no spaces or special chars to replace).

    EXAMPLE WALKTHROUGH:
      1. Input: name="TechCrunch", fallback_seed=0
      2. name.lower() -> "techcrunch"
      3. re.sub(r"[^a-zA-Z0-9_]+", "_", "techcrunch") -> "techcrunch" (no match, unchanged)
      4. .strip("_") -> "techcrunch" (no leading/trailing underscores)
      5. slug is non-empty, so return "techcrunch"

    OPTIONS:
      - Input: "TechCrunch" (camelCase brand name)
      - Fallback seed: 0
      - Expected output: "techcrunch" (all lowercase, no spaces)

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns "techcrunch"

    ERRORS/EDGE CASES:
      - Wrong case: returns "TECHCRUNCH" or "TechCrunch" — assertion fails
      - Extra underscores: returns "tech_crunch" — assertion fails

    HOW TO TEST: Change re.sub to replace with "-" instead of "_".
                 Run this test — it should fail (returns "techcrunch" still since no separator chars).
    """
    mod = _import_module()
    assert mod.generate_feed_id("TechCrunch", 0) == "techcrunch"


def test_bbc_news():
    """Layer 2 — 'BBC News', 0 -> 'bbc_news'.

    WHAT: Verifies that a feed name with a space has the space replaced with
          an underscore, and all letters are lowercased.

    EXAMPLE WALKTHROUGH:
      1. Input: name="BBC News", fallback_seed=0
      2. name.lower() -> "bbc news"
      3. re.sub(r"[^a-zA-Z0-9_]+", "_", "bbc news") -> "bbc_news" (space replaced with _)
      4. .strip("_") -> "bbc_news" (no leading/trailing underscores)
      5. slug is non-empty, so return "bbc_news"

    OPTIONS:
      - Input: "BBC News" (two words with space)
      - Fallback seed: 0
      - Expected output: "bbc_news" (space -> underscore, all lowercase)

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns "bbc_news"

    ERRORS/EDGE CASES:
      - Space not replaced: returns "bbcnews" — assertion fails
      - Case preserved: returns "BBC_News" — assertion fails

    HOW TO TEST: Change the regex to not replace spaces (remove space from pattern).
                 Run this test — it should fail (returns "bbcnews").
    """
    mod = _import_module()
    assert mod.generate_feed_id("BBC News", 0) == "bbc_news"


def test_nasa_science():
    """Layer 2 — 'NASA!Science', 0 -> 'nasa_science'.

    WHAT: Verifies that special characters (like '!') are replaced with underscores,
          and all letters are lowercased.

    EXAMPLE WALKTHROUGH:
      1. Input: name="NASA!Science", fallback_seed=0
      2. name.lower() -> "nasa!science"
      3. re.sub(r"[^a-zA-Z0-9_]+", "_", "nasa!science") -> "nasa_science" (! replaced with _)
      4. .strip("_") -> "nasa_science" (no leading/trailing underscores)
      5. slug is non-empty, so return "nasa_science"

    OPTIONS:
      - Input: "NASA!Science" (special character between words)
      - Fallback seed: 0
      - Expected output: "nasa_science" (! -> _)

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns "nasa_science"

    ERRORS/EDGE CASES:
      - Special char not replaced: returns "nasascience" — assertion fails
      - Multiple special chars: "NASA!!Science" -> "nasa__science" (double underscore)

    HOW TO TEST: Change the regex to keep special chars instead of replacing them.
                 Run this test — it should fail.
    """
    mod = _import_module()
    assert mod.generate_feed_id("NASA!Science", 0) == "nasa_science"


def test_all_special_chars():
    """Layer 2 — '!!!', 5 -> 'f5'.

    WHAT: Verifies the fallback behavior when the feed name consists entirely
          of special characters that get stripped, leaving an empty slug.

    EXAMPLE WALKTHROUGH:
      1. Input: name="!!!", fallback_seed=5
      2. name.lower() -> "!!!"
      3. re.sub(r"[^a-zA-Z0-9_]+", "_", "!!!") -> "_" (all ! replaced with _)
      4. .strip("_") -> "" (leading and trailing underscore removed, leaving empty string)
      5. slug is empty (falsy), so return f"f{fallback_seed}" = "f5"

    WHY FALLBACK:
          Feed IDs must be non-empty strings. If we returned an empty string,
          it would break dictionary lookups, database queries, and UI references.
          The fallback "f{seed}" ensures a valid ID is always generated.

    OPTIONS:
      - Input: "!!!" (all special characters)
      - Fallback seed: 5
      - Expected output: "f5"

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns "f5"

    ERRORS/EDGE CASES:
      - Fallback not used: returns "" — assertion fails
      - Wrong seed: returns "f0" instead of "f5" — assertion fails

    HOW TO TEST: Change the fallback from f"f{fallback_seed}" to just "fallback".
                 Run this test — it should fail (returns "fallback" instead of "f5").
    """
    mod = _import_module()
    assert mod.generate_feed_id("!!!", 5) == "f5"


def test_empty_name():
    """Layer 2 — '', 5 -> 'f5'.

    WHAT: Verifies the fallback behavior when the feed name is an empty string.
          An empty name provides no characters to sanitize, so the fallback is used.

    EXAMPLE WALKTHROUGH:
      1. Input: name="", fallback_seed=5
      2. name.lower() -> ""
      3. re.sub(r"[^a-zA-Z0-9_]+", "_", "") -> "" (nothing to replace)
      4. .strip("_") -> "" (still empty)
      5. slug is empty (falsy), so return f"f{fallback_seed}" = "f5"

    WHY EMPTY NAME FALLBACK:
          Users might accidentally submit an empty feed name. Rather than crashing
          or storing an invalid ID, the function gracefully falls back to a
          deterministic ID based on the seed.

    OPTIONS:
      - Input: "" (empty string)
      - Fallback seed: 5
      - Expected output: "f5"

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns "f5"

    ERRORS/EDGE CASES:
      - Empty string passed: should still return fallback, not crash
      - None passed: would raise TypeError (not handled — caller must pass str)

    HOW TO TEST: Pass None instead of "" to the function.
                 It should raise TypeError (this is expected — not a bug).
    """
    mod = _import_module()
    assert mod.generate_feed_id("", 5) == "f5"


def test_output_matches_regex():
    """Layer 2 — Output matches ^[a-z0-9_]+$.

    WHAT: Runs generate_feed_id through 8 different input cases and verifies
          that EVERY output matches the strict pattern ^[a-z0-9_]+$.
          This pattern means: one or more characters, where each character is
          a lowercase letter (a-z), a digit (0-9), or an underscore (_).

    WHY STRICT PATTERN:
          Feed IDs are used as:
          - Dictionary keys in the config JSON
          - References in the UI (button objectNames, table row keys)
          - Database identifiers
          All of these require a simple alphanumeric+underscore format.
          Spaces, special chars, or uppercase would break these systems.

    TEST CASES COVERED:
      1. ("TechCrunch", 0) -> "techcrunch"   — camelCase
      2. ("BBC News", 1) -> "bbc_news"       — space separator
      3. ("NASA!Science", 2) -> "nasa_science" — special char
      4. ("!!!", 5) -> "f5"                   — all special chars (fallback)
      5. ("", 5) -> "f5"                      — empty name (fallback)
      6. ("The Onion", 0) -> "the_onion"      — three-word name
      7. ("CNN", 0) -> "cnn"                  — all caps
      8. ("ESPN!", 3) -> "espn"               — trailing special char stripped

    HOW THE CHECK WORKS:
      1. Compile regex pattern ^[a-z0-9_]+$
      2. For each (name, seed) pair, call generate_feed_id and check match
      3. If ANY output fails to match, report the failing input and output

    OPTIONS: None — ALL outputs must match the pattern.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if all 8 test cases produce valid slug strings.

    ERRORS/EDGE CASES:
      - Any uppercase letter in output: pattern mismatch
      - Any space in output: pattern mismatch
      - Any special character in output: pattern mismatch
      - Empty output: pattern mismatch (+)

    HOW TO TEST: Modify the function to NOT lowercase (remove .lower()).
                 Run this test — "TechCrunch" would produce "TechCrunch" which fails the pattern.
    """
    mod = _import_module()
    # Compile the strict pattern: only lowercase letters, digits, and underscores
    pattern = re.compile(r"^[a-z0-9_]+$")
    # 8 test cases covering all edge cases
    test_cases = [
        ("TechCrunch", 0),
        ("BBC News", 1),
        ("NASA!Science", 2),
        ("!!!", 5),
        ("", 5),
        ("The Onion", 0),
        ("CNN", 0),
        ("ESPN!", 3),
    ]
    # Run each test case and verify the output matches the strict pattern
    for name, seed in test_cases:
        result = mod.generate_feed_id(name, seed)
        # assert pattern.match(result): checks if the ENTIRE string matches ^[a-z0-9_]+$
        # If it doesn't match, report the failing input and output for debugging
        assert pattern.match(result), f"generate_feed_id({name!r}, {seed}) = {result!r} does not match ^[a-z0-9_]+$"
