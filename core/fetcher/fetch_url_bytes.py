"""Single-function module for executing HTTP GET requests and decompressing byte streams."""
import gzip
import io
import urllib.error
import urllib.request
import zlib
from typing import Dict, Optional

from .get_browser_headers import get_browser_headers

try:
    import brotli
    BROTLI_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    brotli = None
    BROTLI_AVAILABLE = False


def _build_accept_encoding() -> str:
    """Advertises only the content encodings this module can actually decode."""
    supported = ["gzip", "deflate"]
    if BROTLI_AVAILABLE:
        supported.append("br")
    return ", ".join(supported)


def _decompress(raw_bytes: bytes, encoding: str) -> bytes:
    """Decompresses a byte stream according to the HTTP Content-Encoding header."""
    enc = (encoding or "").lower()

    if "gzip" in enc:
        with gzip.GzipFile(fileobj=io.BytesIO(raw_bytes)) as gz:
            return gz.read()

    if "deflate" in enc:
        try:
            return zlib.decompress(raw_bytes)
        except zlib.error:  # raw DEFLATE stream without zlib wrapper
            return zlib.decompress(raw_bytes, -zlib.MAX_WBITS)

    if "br" in enc and BROTLI_AVAILABLE:
        try:
            return brotli.decompress(raw_bytes)
        except Exception:  # pragma: no cover - malformed brotli payload
            return raw_bytes

    return raw_bytes


def fetch_url_bytes(url: str, timeout: int = 10, headers: Optional[Dict[str, str]] = None) -> bytes:
    """Fetches raw byte response from URL and decompresses gzip/deflate/brotli."""
    req_headers = headers if headers is not None else get_browser_headers()

    # Advertise only the encodings we can decode; otherwise br-only servers
    # (e.g. TechCrunch) send brotli bytes we would hand to the XML parser.
    req_headers = dict(req_headers)
    req_headers["Accept-Encoding"] = _build_accept_encoding()

    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw_bytes = resp.read()
        encoding = resp.info().get("Content-Encoding", "").lower()
        return _decompress(raw_bytes, encoding)