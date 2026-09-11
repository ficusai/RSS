"""
Tiered Memory & Response Cache Manager for RSS feed ingestion.
Prevents cache stampedes and eliminates redundant network requests.
"""

import time
import json
import threading
from typing import Any, Optional, Dict, Tuple


class CacheManager:
    """
    In-memory and Redis-backed TTL caching manager with lock claiming for concurrency control.
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
        """
        Retrieves cached value if key exists and has not expired.
        """
        if self.redis_client:
            try:
                val = self.redis_client.get(key)
                return json.loads(val) if val else None
            except Exception:
                pass

        with self._thread_lock:
            entry = self.memory_store.get(key)
            if entry:
                val, expire_at = entry
                if time.time() < expire_at:
                    return val
                del self.memory_store[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Stores key-value pair with a TTL expiration in seconds.
        """
        ttl_seconds = ttl if ttl is not None else self.default_ttl
        if self.redis_client:
            try:
                self.redis_client.setex(key, ttl_seconds, json.dumps(value))
                return
            except Exception:
                pass

        with self._thread_lock:
            self.memory_store[key] = (value, time.time() + ttl_seconds)

    def claim_lock(self, key: str, timeout: float = 10.0) -> bool:
        """
        Attempts to claim an exclusive concurrency lock for a cache key.
        Prevents thundering herd / cache stampedes when fetching new resources.
        Returns True if lock acquired, False if already locked.
        """
        lock_key = f"lock:{key}"
        now = time.time()

        if self.redis_client:
            try:
                acquired = self.redis_client.set(lock_key, "1", nx=True, px=int(timeout * 1000))
                return bool(acquired)
            except Exception:
                pass

        with self._thread_lock:
            expire_at = self.locks.get(lock_key, 0)
            if now < expire_at:
                return False
            self.locks[lock_key] = now + timeout
            return True

    def release_lock(self, key: str) -> None:
        """
        Releases an exclusive concurrency lock.
        """
        lock_key = f"lock:{key}"
        if self.redis_client:
            try:
                self.redis_client.delete(lock_key)
                return
            except Exception:
                pass

        with self._thread_lock:
            self.locks.pop(lock_key, None)

    def clear(self) -> None:
        """
        Clears all in-memory cached entries and locks.
        """
        with self._thread_lock:
            self.memory_store.clear()
            self.locks.clear()
