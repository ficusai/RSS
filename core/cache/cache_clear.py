"""Single-function module for clearing cache store."""
from typing import Any


def cache_clear(cache_instance: Any) -> None:
    """
    Clears all in-memory cached entries and locks.
    """
    with cache_instance._thread_lock:
        cache_instance.memory_store.clear()
        cache_instance.locks.clear()
