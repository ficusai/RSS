"""Single-function module for checking hotlink protection status of media URLs."""
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
