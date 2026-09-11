"""Shared boilerplate vocabulary for extraction quality control.

Single source of truth consumed by the readability extractor (to prune junk
blocks during extraction) and by the storage layer (to decide whether a freshly
extracted text is clean enough to replace a stored one).
"""

BOILERPLATE_TERMS = (
    "most popular", "recommended for you", "you may also like", "related stories",
    "related posts", "read more", "continue reading", "sign up", "subscribe",
    "subscribe now", "register now", "newsletter", "all rights reserved",
    "cookie policy", "privacy policy", "terms of use", "follow us", "share this",
    "advertisement", "advertising", "sponsored content", "don't miss out",
    "view bio", "download the app", "get the latest", "trending now",
    "load more", "back to top", "watch now", "in case you missed",
    "please enable javascript", "could not load", "skip to content",
    "close ad", "close dialog", "manage consent",
    # site/UI chrome artefacts
    "no results found", "select an option", "learn more about", "clone urls",
    "explore more collections", "sign in to your account",
    # event-promo copy
    "tickets now", "% off", "save up to", "register for the", "reserve your spot",
)