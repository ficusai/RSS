"""Single-function module for cache lock claiming."""
import time
from typing import Any


def cache_claim_lock(cache_instance: Any, key: str, timeout: float = 10.0) -> bool:
    """
    Attempts to claim an exclusive concurrency lock for a cache key.
    """
    lock_key = f"lock:{key}"
    now = time.time()

    if cache_instance.redis_client:
        try:
            acquired = cache_instance.redis_client.set(lock_key, "1", nx=True, px=int(timeout * 1000))
            return bool(acquired)
        except Exception:
            pass

    with cache_instance._thread_lock:
        expire_at = cache_instance.locks.get(lock_key, 0)
        if now < expire_at:
            return False
        cache_instance.locks[lock_key] = now + timeout
        return True
