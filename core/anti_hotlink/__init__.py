"""Anti-hotlink package re-exporting single-function modules."""
from .is_hotlink_protected import is_hotlink_protected, HOTLINK_DOMAINS
from .process_anti_hotlink import process_anti_hotlink

__all__ = [
    "HOTLINK_DOMAINS",
    "is_hotlink_protected",
    "process_anti_hotlink",
]
