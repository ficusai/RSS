"""Single-function module for ensuring storage directory existence."""
from .paths import get_results_dir


def _ensure_dir() -> None:
    """Ensures that the output storage directory exists."""
    get_results_dir().mkdir(parents=True, exist_ok=True)
