"""
Multi-Proxy Pool & Failover Health Manager for Ficus RSS.
Inspired by RSSHub's lib/utils/proxy/multi-proxy.ts.
Tracks proxy availability, rotates proxies round-robin, and handles automatic failure recovery.
"""

import time
import logging
import urllib.request
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ProxyState:
    """Represents the operational health and configuration state of a proxy."""

    def __init__(self, uri: str):
        self.uri = uri
        self.is_active = True
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None

    def mark_failed(self, max_failures: int = 3) -> None:
        """Increments failure count and deactivates if threshold reached."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= max_failures:
            self.is_active = False
            logger.warning(f"Proxy {self.uri} marked as inactive after {max_failures} failures.")
        else:
            logger.warning(f"Proxy {self.uri} failure recorded ({self.failure_count}/{max_failures}).")

    def reset(self) -> None:
        """Resets proxy health to active status."""
        self.is_active = True
        self.failure_count = 0
        self.last_failure_time = None
        logger.info(f"Proxy {self.uri} reset to active.")


class ProxyManager:
    """Manages a pool of HTTP/HTTPS/SOCKS proxies with automatic round-robin rotation and failover."""

    def __init__(self, proxy_uris: Optional[List[str]] = None, health_check_interval: float = 60.0):
        self.proxies: List[ProxyState] = []
        self.current_index = 0
        self.health_check_interval = health_check_interval
        self.max_failures = 3

        if proxy_uris:
            for uri in proxy_uris:
                self.add_proxy(uri)

    def add_proxy(self, uri: str) -> None:
        """Adds a proxy URI (e.g. 'http://proxy:8080' or 'socks5://proxy:1080') to the pool."""
        clean_uri = uri.strip()
        if clean_uri and not any(p.uri == clean_uri for p in self.proxies):
            self.proxies.append(ProxyState(clean_uri))
            logger.info(f"Added proxy to pool: {clean_uri}")

    def _refresh_health(self) -> None:
        """Reactivates failed proxies whose quarantine cooldown period has expired."""
        now = time.time()
        for p in self.proxies:
            if not p.is_active and p.last_failure_time:
                if now - p.last_failure_time > self.health_check_interval:
                    p.reset()

    def get_next_proxy(self) -> Optional[ProxyState]:
        """Returns the next active proxy using round-robin selection."""
        self._refresh_health()
        active_proxies = [p for p in self.proxies if p.is_active]
        if not active_proxies:
            return None

        proxy = active_proxies[self.current_index % len(active_proxies)]
        self.current_index = (self.current_index + 1) % len(active_proxies)
        return proxy

    def mark_proxy_failed(self, uri: str) -> None:
        """Marks a proxy failure by URI."""
        for p in self.proxies:
            if p.uri == uri:
                p.mark_failed(self.max_failures)
                break

    def get_urllib_handler(self, proxy_uri: Optional[str] = None) -> urllib.request.ProxyHandler:
        """Creates a urllib ProxyHandler for Tier 1 requests."""
        if not proxy_uri:
            proxy_state = self.get_next_proxy()
            proxy_uri = proxy_state.uri if proxy_state else ""

        if not proxy_uri:
            return urllib.request.ProxyHandler({})

        return urllib.request.ProxyHandler({
            "http": proxy_uri,
            "https": proxy_uri,
        })


# Global default proxy manager instance
global_proxy_manager = ProxyManager()
