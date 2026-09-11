"""Single-function module for extracting custom window state JSON from HTML script tags."""
import json
import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


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
