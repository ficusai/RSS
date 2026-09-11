"""
Unit tests for CacheManager module.
"""

import time
import unittest
from core.cache import CacheManager


class TestCacheManager(unittest.TestCase):
    """Unit tests for Tiered Memory & Response Cache Manager."""

    def setUp(self):
        self.cache = CacheManager(default_ttl=2)

    def tearDown(self):
        self.cache.clear()

    def test_set_and_get_valid(self):
        self.cache.set("key1", {"title": "Test Title", "data": [1, 2, 3]})
        retrieved = self.cache.get("key1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["title"], "Test Title")
        self.assertEqual(retrieved["data"], [1, 2, 3])

    def test_ttl_expiration(self):
        self.cache.set("expire_key", "value", ttl=1)
        self.assertEqual(self.cache.get("expire_key"), "value")
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("expire_key"))

    def test_concurrency_lock_claiming(self):
        lock_key = "feed:https://example.com/rss.xml"
        
        # First claim should succeed
        self.assertTrue(self.cache.claim_lock(lock_key, timeout=5.0))
        
        # Second claim while locked should fail
        self.assertFalse(self.cache.claim_lock(lock_key, timeout=5.0))
        
        # Release lock
        self.cache.release_lock(lock_key)
        
        # Claim after release should succeed
        self.assertTrue(self.cache.claim_lock(lock_key, timeout=5.0))

    def test_clear_resets_store(self):
        self.cache.set("k1", "v1")
        self.cache.set("k2", "v2")
        self.cache.clear()
        self.assertIsNone(self.cache.get("k1"))
        self.assertIsNone(self.cache.get("k2"))


if __name__ == "__main__":
    unittest.main()
