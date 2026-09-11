"""
Unit tests for Anti-Hotlink Media Rewriter and Embedded Script Data Extractor.
"""

import pytest
from core.anti_hotlink import is_hotlink_protected, process_anti_hotlink
from core.script_data_extractor import extract_next_data, extract_nuxt_data, extract_window_state


def test_is_hotlink_protected():
    """Verify detection of hotlink-restricted domains."""
    assert is_hotlink_protected("https://tvax1.sinaimg.cn/crop.0.0.1080.1080.180/img.jpg") is True
    assert is_hotlink_protected("https://i0.hdslb.com/bfs/archive/cover.jpg") is True
    assert is_hotlink_protected("https://example.com/image.png") is False


def test_process_anti_hotlink():
    """Verify injection of referrerpolicy='no-referrer' into HTML media tags."""
    html_raw = '<p>Check this image: <img src="https://tvax1.sinaimg.cn/test.jpg" /></p>'
    processed = process_anti_hotlink(html_raw, force_no_referrer=True)
    assert 'referrerpolicy="no-referrer"' in processed
    assert 'sinaimg.cn' in processed


def test_extract_next_data():
    """Verify extraction of Next.js __NEXT_DATA__ JSON state."""
    html = """
    <html>
      <body>
        <script id="__NEXT_DATA__" type="application/json">
          {"props":{"pageProps":{"title":"Test Page"}},"page":"/test"}
        </script>
      </body>
    </html>
    """
    data = extract_next_data(html)
    assert isinstance(data, dict)
    assert data["page"] == "/test"
    assert data["props"]["pageProps"]["title"] == "Test Page"


def test_extract_nuxt_data():
    """Verify extraction of Nuxt.js __NUXT__ JSON state."""
    html = """
    <html>
      <body>
        <script id="__NUXT__" type="application/json">
          {"data":[{"state":"active"}]}
        </script>
      </body>
    </html>
    """
    data = extract_nuxt_data(html)
    assert isinstance(data, dict)
    assert data["data"][0]["state"] == "active"
