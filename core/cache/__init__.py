"""Cache module package re-exporting single-function modules and CacheManager facade."""
from .cache_get import cache_get
from .cache_set import cache_set
from .cache_claim_lock import cache_claim_lock
from .cache_release_lock import cache_release_lock
from .cache_clear import cache_clear
from .cache_manager import CacheManager

__all__ = [
    "cache_get",
    "cache_set",
    "cache_claim_lock",
    "cache_release_lock",
    "cache_clear",
    "CacheManager",
]
