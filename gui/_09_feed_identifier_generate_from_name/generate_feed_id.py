"""Standalone feed-ID generator using a single regex pattern."""
# WHAT: Derives a slug-like ID from a feed name via re.sub(r"[^a-zA-Z0-9_]+", "_", ...).
#       Used at 4 call sites in the original window.py to avoid duplication.
# OPTIONS: fallback_seed — integer used when the sanitized name is empty.
# DEFAULTS: If the sanitized name is empty, falls back to f"f{fallback_seed}".
# OUTPUT/EFFECT: A lowercase string containing only [a-z0-9_].
# ERRORS/EDGE CASES: None.
# HOW TO TEST: generate_feed_id("TechCrunch", 0) == "techcrunch"; generate_feed_id("", 5) == "f5"
import re


def generate_feed_id(name: str, fallback_seed: int) -> str:
    """Return a slug-like feed ID derived from *name*."""
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_")
    return slug or f"f{fallback_seed}"
