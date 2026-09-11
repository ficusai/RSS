"""
Unit tests for Cookie Manager and Multi-Proxy Pool Manager modules.
"""

import pytest
from core.cookie_manager import parse_cookie_header, format_cookie_header
from core.proxy_manager import ProxyManager, ProxyState


def test_parse_cookie_header():
    """Verify parsing raw HTTP Cookie header into Playwright dict array."""
    raw_cookies = "sessionid=xyz123; user_token=abc456; theme=dark"
    cookies = parse_cookie_header(raw_cookies, "example.com")
    assert len(cookies) == 3
    assert cookies[0] == {"name": "sessionid", "value": "xyz123", "domain": "example.com", "path": "/"}
    assert cookies[1] == {"name": "user_token", "value": "abc456", "domain": "example.com", "path": "/"}
    assert cookies[2] == {"name": "theme", "value": "dark", "domain": "example.com", "path": "/"}


def test_format_cookie_header():
    """Verify formatting Playwright dict array into Cookie header string."""
    cookies = [
        {"name": "sessionid", "value": "xyz123", "domain": "example.com", "path": "/"},
        {"name": "user_token", "value": "abc456", "domain": "sub.example.com", "path": "/"},
        {"name": "other", "value": "123", "domain": "otherdomain.com", "path": "/"},
    ]

    header_str = format_cookie_header(cookies, domain_filter="example.com")
    assert "sessionid=xyz123" in header_str
    assert "user_token=abc456" in header_str
    assert "other=123" not in header_str


def test_proxy_manager_rotation_and_failover():
    """Verify round-robin rotation and automatic deactivation upon failures."""
    manager = ProxyManager(["http://proxy1:8080", "http://proxy2:8080"], health_check_interval=1.0)
    
    # Round-robin selection
    p1 = manager.get_next_proxy()
    p2 = manager.get_next_proxy()
    assert p1.uri == "http://proxy1:8080"
    assert p2.uri == "http://proxy2:8080"

    # Mark proxy1 as failed 3 times
    manager.mark_proxy_failed("http://proxy1:8080")
    manager.mark_proxy_failed("http://proxy1:8080")
    manager.mark_proxy_failed("http://proxy1:8080")

    # Only proxy2 should remain active
    next_p = manager.get_next_proxy()
    assert next_p.uri == "http://proxy2:8080"
