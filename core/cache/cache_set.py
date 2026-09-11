"""Single-function module for cache insertion."""
import json
import time
from typing import Any, Optional


def cache_set(cache_instance: Any, key: str, value: Any, ttl: Optional[int] = None) -> None:
    """
    Stores key-value pair with a TTL expiration in seconds.
    """
    ttl_seconds = ttl if ttl is not None else cache_instance.default_ttl
    if cache_instance.redis_client:
        try:
            cache_instance.redis_client.setex(key, ttl_seconds, json.dumps(value))
            return
        except Exception:
            pass

    with cache_instance._thread_lock:
        cache_instance.memory_store[key] = (value, time.time() + ttl_seconds)
