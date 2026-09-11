"""Storage directory paths definitions."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = PROJECT_ROOT / "SCRAPED-RESULTS"
ARTICLES_FILE = RESULTS_DIR / "scraped_articles.jsonl"
DEDUP_FILE = RESULTS_DIR / "dedup_state.json"


def get_results_dir() -> Path:
    import core.storage as s
    return getattr(s, "RESULTS_DIR", RESULTS_DIR)


def get_articles_file() -> Path:
    import core.storage as s
    return getattr(s, "ARTICLES_FILE", ARTICLES_FILE)


def get_dedup_file() -> Path:
    import core.storage as s
    return getattr(s, "DEDUP_FILE", DEDUP_FILE)
