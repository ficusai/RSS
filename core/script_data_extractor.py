"""
Embedded JavaScript State & JSON Extractor Engine for Ficus RSS.
Inspired by RSSHub's lib/utils/parse-script-data.ts.
Extracts structured JSON state objects (__NEXT_DATA__, __NUXT__, window.__INITIAL_STATE__) from web pages.
"""

import json
import re
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def extract_next_data(html: str) -> Optional[Dict[str, Any]]:
    """
    Extracts Next.js page state object from <script id="__NEXT_DATA__">.
    """
    if not html:
        return None

    match = re.search(r'<script\b[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, flags=re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception as e:
            logger.debug(f"Failed to parse __NEXT_DATA__ JSON: {e}")
    return None


def extract_nuxt_data(html: str) -> Optional[Dict[str, Any]]:
    """
    Extracts Nuxt.js page state object from <script id="__NUXT__"> or window.__NUXT__.
    """
    if not html:
        return None

    # Check script tag with id __NUXT__
    match = re.search(r'<script\b[^>]*id="__NUXT__"[^>]*>(.*?)</script>', html, flags=re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass

    # Check window.__NUXT__ = {...}
    match = re.search(r'window\.__NUXT__\s*=\s*(\{.*?\}\s*);', html, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception as e:
            logger.debug(f"Failed to parse window.__NUXT__: {e}")
    return None


def extract_window_state(html: str, var_name: str = "__INITIAL_STATE__") -> Optional[Dict[str, Any]]:
    """
    Extracts window.<var_name> JSON object from script tags.
    """
    if not html:
        return None

    pattern = rf'window\.{re.escape(var_name)}\s*=\s*(\{{.*?\}});'
    match = re.search(pattern, html, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception as e:
            logger.debug(f"Failed to parse window.{var_name}: {e}")
    return None
