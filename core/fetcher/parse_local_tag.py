"""Single-function module for extracting local XML tag names."""
import xml.etree.ElementTree as ET


def parse_local_tag(elem: ET.Element) -> str:
    """Returns local tag name without XML namespace."""
    if elem.tag.startswith("{"):
        return elem.tag.split("}", 1)[1].lower()
    return elem.tag.lower()
