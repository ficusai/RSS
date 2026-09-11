"""Single-function module for rewriting media tags in HTML to bypass hotlink restrictions."""
import re
import urllib.parse
from typing import Optional
from .is_hotlink_protected import is_hotlink_protected


def process_anti_hotlink(
    html_content: str,
    template: Optional[str] = None,
    force_no_referrer: bool = True,
) -> str:
    """
    Rewrites media elements (img, video, audio, source) in HTML content to bypass hotlink protections.
    """
    if not html_content:
        return ""

    content = html_content

    if force_no_referrer:
        def add_no_referrer(match: re.Match) -> str:
            tag = match.group(0)
            if "referrerpolicy" not in tag.lower():
                if tag.endswith("/>"):
                    return tag[:-2] + ' referrerpolicy="no-referrer" />'
                return tag[:-1] + ' referrerpolicy="no-referrer">'
            return tag

        content = re.sub(r"<img\b[^>]*>", add_no_referrer, content, flags=re.IGNORECASE)

    if template:
        def replace_src(match: re.Match) -> str:
            prefix, quote, src, suffix = match.groups()
            if is_hotlink_protected(src) and not src.startswith("data:"):
                encoded_src = urllib.parse.quote(src, safe="")
                new_src = template.replace("${href_ue}", encoded_src).replace("${href}", src)
                return f'{prefix}{quote}{new_src}{quote}{suffix}'
            return match.group(0)

        content = re.sub(r'(\bsrc=)(["\'])(.*?)\2([^>]*>)', replace_src, content, flags=re.IGNORECASE)

    return content
