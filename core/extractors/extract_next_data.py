"""Single-function module for extracting Next.js JSON state from HTML."""
import json
import logging
import re
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
