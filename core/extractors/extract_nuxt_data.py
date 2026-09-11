"""Single-function module for extracting Nuxt.js JSON state from HTML."""
import json
import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def extract_nuxt_data(html: str) -> Optional[Dict[str, Any]]:
    """
    Extracts Nuxt.js page state object from <script id="__NUXT__"> or window.__NUXT__.
    """
    if not html:
        return None

    match = re.search(r'<script\b[^>]*id="__NUXT__"[^>]*>(.*?)</script>', html, flags=re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass

    match = re.search(r'window\.__NUXT__\s*=\s*(\{.*?\}\s*);', html, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception as e:
            logger.debug(f"Failed to parse window.__NUXT__: {e}")
    return None
