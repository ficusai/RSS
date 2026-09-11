"""
Unit and integration tests for Stealth Browser Ingestion Engine and Client Hints Generator.
"""

import pytest
from core.stealth import get_client_hints_headers, is_stealth_available, fetch_with_stealth_browser
from core.fetcher import fetch_feed


def test_client_hints_headers_structure():
    """Verify that get_client_hints_headers produces valid browser headers and Client Hints."""
    headers = get_client_hints_headers()
    assert "User-Agent" in headers
    assert "Accept" in headers
    assert "Sec-Fetch-Dest" in headers
    
    # Check Client Hints if User-Agent is Chromium-based
    if "Chrome" in headers["User-Agent"]:
        assert "Sec-Ch-Ua" in headers
        assert "Sec-Ch-Ua-Mobile" in headers
        assert "Sec-Ch-Ua-Platform" in headers


def test_is_stealth_available():
    """Verify stealth availability detection function."""
    assert is_stealth_available() is True


def test_stealth_fetcher_real_url():
    """Verify stealth browser fetcher against standard feed URL."""
    if not is_stealth_available():
        pytest.skip("Playwright stealth browser not installed")
    
    url = "https://www.federalreserve.gov/feeds/press_all.xml"
    content = fetch_with_stealth_browser(url, timeout=20, force_headless=True)
    assert isinstance(content, bytes)
    assert len(content) > 0
    assert b"xml" in content.lower() or b"rss" in content.lower() or b"channel" in content.lower()


def test_tiered_fetcher_integration():
    """Verify tiered dual-engine fetch_feed parsing."""
    feed_config = {
        "url": "https://www.federalreserve.gov/feeds/press_all.xml",
        "name": "Fed Press Releases",
        "category": "Economics"
    }
    articles = fetch_feed(feed_config, timeout=10)
    assert isinstance(articles, list)
    assert len(articles) > 0
    assert "title" in articles[0]
    assert "url" in articles[0]
