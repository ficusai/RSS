"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_09_feed_identifier_generate_from_name/generate_feed_id.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.
"""
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
import ast
import inspect
import re
import sys
from pathlib import Path

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_09_feed_identifier_generate_from_name" / "generate_feed_id.py"


def _import_module():
    import gui._09_feed_identifier_generate_from_name.generate_feed_id as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence."""
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health."""
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports."""
    expected = {"re"}
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, f"Missing imports: {sorted(missing)}"


def test_source_contains_slug_regex():
    """Layer 1 — Source contains import re + slug regex literal."""
    source = _module_path().read_text()
    assert "import re" in source
    assert re.search(r'r"\[\^a-zA-Z0-9_\]\+"', source) or re.search(r"r'\[\^a-zA-Z0-9_\]\+'", source), \
        "Source should contain the slug regex literal [^a-zA-Z0-9_]+"


def test_generate_feed_id_signature():
    """Layer 1 — generate_feed_id(name: str, fallback_seed: int) -> str."""
    mod = _import_module()
    func = mod.generate_feed_id
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [
        ("name", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
        ("fallback_seed", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty),
    ]
    assert params == expected
    assert sig.return_annotation is str


def test_techcrunch():
    """Layer 2 — 'TechCrunch' -> 'techcrunch'."""
    mod = _import_module()
    assert mod.generate_feed_id("TechCrunch", 0) == "techcrunch"


def test_bbc_news():
    """Layer 2 — 'BBC News' -> 'bbc_news'."""
    mod = _import_module()
    assert mod.generate_feed_id("BBC News", 0) == "bbc_news"


def test_nasa_science():
    """Layer 2 — 'NASA!Science' -> 'nasa_science'."""
    mod = _import_module()
    assert mod.generate_feed_id("NASA!Science", 0) == "nasa_science"


def test_all_special_chars():
    """Layer 2 — '!!!', 5 -> 'f5'."""
    mod = _import_module()
    assert mod.generate_feed_id("!!!", 5) == "f5"


def test_empty_name():
    """Layer 2 — '', 5 -> 'f5'."""
    mod = _import_module()
    assert mod.generate_feed_id("", 5) == "f5"


def test_output_matches_regex():
    """Layer 2 — Output matches ^[a-z0-9_]+$."""
    mod = _import_module()
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
    pattern = re.compile(r"^[a-z0-9_]+$")
    for name, seed in test_cases:
        result = mod.generate_feed_id(name, seed)
        assert pattern.match(result), f"generate_feed_id({name!r}, {seed}) = {result!r} does not match ^[a-z0-9_]+$"
