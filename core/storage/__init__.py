"""Storage package re-exporting single-function modules and paths."""
import sys
from . import paths
from .ensure_dir import _ensure_dir
from .generate_article_id import generate_article_id
from .load_dedup_state import _load_dedup_state
from .save_dedup_state import _save_dedup_state
from .is_duplicate import is_duplicate
from .save_articles import save_articles
from .get_stats import get_stats
from .load_articles import load_articles

_module = sys.modules[__name__]


def __getattr__(name: str):
    if name in ("RESULTS_DIR", "ARTICLES_FILE", "DEDUP_FILE", "PROJECT_ROOT"):
        return getattr(paths, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __setattr__(name: str, value):
    if name in ("RESULTS_DIR", "ARTICLES_FILE", "DEDUP_FILE", "PROJECT_ROOT"):
        setattr(paths, name, value)
    else:
        super(_module.__class__, _module).__setattr__(name, value)


__all__ = [
    "paths",
    "PROJECT_ROOT",
    "RESULTS_DIR",
    "ARTICLES_FILE",
    "DEDUP_FILE",
    "_ensure_dir",
    "generate_article_id",
    "_load_dedup_state",
    "_save_dedup_state",
    "is_duplicate",
    "save_articles",
    "get_stats",
    "load_articles",
]
