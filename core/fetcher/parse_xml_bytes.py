"""Single-function module for parsing XML byte stream into article items."""
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List
from .parse_local_tag import parse_local_tag
from .parse_item_element import parse_item_element


def parse_xml_bytes(raw_data: bytes, feed_config: Dict[str, Any], extract_full_text: bool = False) -> List[Dict[str, Any]]:
    """Sanitizes raw XML bytes and parses article items."""
    xml_str = raw_data.decode("utf-8", errors="ignore")
    xml_str = re.sub(r"[^\x09\x0A\x0D\x20-\xD7FF\xE000-\xFFFD]", "", xml_str)

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
