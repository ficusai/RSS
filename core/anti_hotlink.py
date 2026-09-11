"""
Anti-Hotlink Media Rewriter Engine for Ficus RSS.
Inspired by RSSHub's lib/middleware/anti-hotlink.ts.
Parses HTML content to inject no-referrer policies or proxy templates for hotlink-protected media.
"""

import re
from typing import Optional

# Known hotlink-restricted domains (e.g. Weibo, Bilibili, Zhihu, Douban)
HOTLINK_DOMAINS = (
    "sinaimg.cn",
    "weibo.cn",
    "hdslb.com",
    "bilibili.com",
    "zhimg.com",
    "doubanio.com",
    "qq.com",
    "qpic.cn",
    "pximg.net",
)


def is_hotlink_protected(url: str) -> bool:
    """Checks if a media URL belongs to a known hotlink-protected platform."""
    if not url:
        return False
    lower_url = url.lower()
    return any(domain in lower_url for domain in HOTLINK_DOMAINS)


def process_anti_hotlink(
    html_content: str,
    template: Optional[str] = None,
    force_no_referrer: bool = True,
) -> str:
    """
    Rewrites media elements (img, video, audio, source) in HTML content to bypass hotlink protections.
    
    Args:
        html_content: Raw HTML content string.
        template: Optional proxy template string containing '${href}' or '${href_ue}'.
        force_no_referrer: If True, automatically appends referrerpolicy="no-referrer" to img/video tags.

    Returns:
        Processed HTML content string.
    """
    if not html_content:
        return ""

    content = html_content

    # Inject referrerpolicy="no-referrer" into <img> tags if missing
    if force_no_referrer:

        def add_no_referrer(match: re.Match) -> str:
            tag = match.group(0)
            if "referrerpolicy" not in tag.lower():
                # Insert before closing > or />
                if tag.endswith("/>"):
                    return tag[:-2] + ' referrerpolicy="no-referrer" />'
                return tag[:-1] + ' referrerpolicy="no-referrer">'
            return tag

        content = re.sub(r"<img\b[^>]*>", add_no_referrer, content, flags=re.IGNORECASE)

    # Template replacement if custom media proxy template provided
    if template:
        import urllib.parse

        def replace_src(match: re.Match) -> str:
            prefix, quote, src, suffix = match.groups()
            if is_hotlink_protected(src) and not src.startswith("data:"):
                encoded_src = urllib.parse.quote(src, safe="")
                new_src = template.replace("${href_ue}", encoded_src).replace("${href}", src)
                return f'{prefix}{quote}{new_src}{quote}{suffix}'
            return match.group(0)

        content = re.sub(r'(\bsrc=)(["\'])(.*?)\2([^>]*>)', replace_src, content, flags=re.IGNORECASE)

    return content
