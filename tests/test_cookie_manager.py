"""
Unit tests for Cookie Manager module.
"""

import pytest
from core.cookie_manager import parse_cookie_header, format_cookie_header


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
