"""Single-function module for cache lock releasing."""
from typing import Any


def cache_release_lock(cache_instance: Any, key: str) -> None:
    """
    Releases an exclusive concurrency lock.
    """
    lock_key = f"lock:{key}"
    if cache_instance.redis_client:
        try:
            cache_instance.redis_client.delete(lock_key)
            return
        except Exception:
            pass

    with cache_instance._thread_lock:
        cache_instance.locks.pop(lock_key, None)
