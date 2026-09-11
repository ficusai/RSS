"""
Readability & Full-Text Content Extractor module for RSS processing.
Strips site clutter (navbars, sidebars, ads, popups, footers) to isolate clean article body content.
"""

from typing import Dict, Any
from core.extractors.extract_readability import extract_readability


class ReadabilityExtractor:
    """
    DOM-based article content extractor that purges layout noise and isolates primary text.
    Delegates extraction logic to core/extractors/extract_readability.py.
    """

    @classmethod
    def extract(cls, html_content: str, url: str = "") -> Dict[str, Any]:
        return extract_readability(html_content, url)
