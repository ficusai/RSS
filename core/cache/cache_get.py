"""Single-function module for cache retrieval."""
import json
import time
from typing import Any, Optional


def cache_get(cache_instance: Any, key: str) -> Optional[Any]:
    """
    Retrieves cached value if key exists and has not expired.
    """
    if cache_instance.redis_client:
        try:
            val = cache_instance.redis_client.get(key)
            return json.loads(val) if val else None
        except Exception:
            pass

    with cache_instance._thread_lock:
        entry = cache_instance.memory_store.get(key)
        if entry:
            val, expire_at = entry
            if time.time() < expire_at:
                return val
            del cache_instance.memory_store[key]
    return None
