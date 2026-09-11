"""Single-function module for parsing XML byte stream into article items."""
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List
from .parse_local_tag import parse_local_tag
from .parse_item_element import parse_item_element


def parse_xml_bytes(raw_data: bytes, feed_config: Dict[str, Any], extract_full_text: bool = False) -> List[Dict[str, Any]]:
    """Sanitizes raw XML bytes and parses article items."""
    xml_str = raw_data.decode("utf-8", errors="ignore")
    # NOTE: strip ONLY characters that are structurally invalid in XML 1.0
    # (most control chars, surrogates, \uFFFE/\uFFFF). Never use a broad
    # allow-list here: \x escapes only consume 2 hex digits, so ranges such
    # as \x20-\xD7FF get misparsed and silently destroy every non-ASCII
    # character (Λ, –, —, curly quotes, ñ, ...) in titles and body text.
    xml_str = re.sub(
        r"[\u0000-\u0008\u000B\u000C\u000E-\u001F\uD800-\uDFFF\uFFFE\uFFFF]",
        "",
        xml_str,
    )

    root = ET.fromstring(xml_str)
    articles = []
    root_tag = parse_local_tag(root)

    if root_tag == "rss":
        channel = root.find("channel")
        if channel is not None:
            for child in channel:
                if parse_local_tag(child) == "item":
                    articles.append(parse_item_element(child, feed_config, extract_full_text=extract_full_text))
    elif root_tag == "feed":
        for child in root:
            if parse_local_tag(child) == "entry":
                articles.append(parse_item_element(child, feed_config, extract_full_text=extract_full_text))
    else:
        for item in root.iter():
            if parse_local_tag(item) in ("item", "entry"):
                articles.append(parse_item_element(item, feed_config, extract_full_text=extract_full_text))

    return articles
