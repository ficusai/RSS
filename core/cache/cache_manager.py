"""
Tiered Memory & Response Cache Manager for RSS feed ingestion.
Prevents cache stampedes and eliminates redundant network requests.
"""

import threading
from typing import Any, Optional, Dict, Tuple

from .cache_get import cache_get
from .cache_set import cache_set
from .cache_claim_lock import cache_claim_lock
from .cache_release_lock import cache_release_lock
from .cache_clear import cache_clear


class CacheManager:
    """
    In-memory and Redis-backed TTL caching manager with lock claiming for concurrency control.
    Delegates operations to dedicated single-function modules under core/cache/.
    """

    def __init__(self, redis_url: Optional[str] = None, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self.memory_store: Dict[str, Tuple[Any, float]] = {}
        self.locks: Dict[str, float] = {}
        self._thread_lock = threading.Lock()
        self.redis_client = None

        if redis_url:
            try:
                import redis
                self.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
            except Exception as e:
                print(f"[CacheManager] Redis unavailable, using In-Memory store: {e}")

    def get(self, key: str) -> Optional[Any]:
        return cache_get(self, key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        cache_set(self, key, value, ttl)

    def claim_lock(self, key: str, timeout: float = 10.0) -> bool:
        return cache_claim_lock(self, key, timeout)

    def release_lock(self, key: str) -> None:
        cache_release_lock(self, key)

    def clear(self) -> None:
        cache_clear(self)
