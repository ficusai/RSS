"""Single-function module for executing HTTP GET requests and decompressing byte streams."""
import gzip
import io
import urllib.error
import urllib.request
from typing import Dict, Optional
from .get_browser_headers import get_browser_headers


def fetch_url_bytes(url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None) -> bytes:
    """Fetches raw byte response from URL with GZIP decompression."""
    req_headers = headers if headers is not None else get_browser_headers()
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw_bytes = resp.read()
        encoding = resp.info().get("Content-Encoding", "").lower()
        if "gzip" in encoding:
            with gzip.GzipFile(fileobj=io.BytesIO(raw_bytes)) as gz:
                return gz.read()
        return raw_bytes
