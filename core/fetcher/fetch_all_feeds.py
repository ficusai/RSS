"""Single-function module for parallel thread pool feed scraping execution."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional, Tuple
from .fetch_feed import fetch_feed


def fetch_all_feeds(
    feeds_list: List[Dict[str, Any]],
    progress_callback: Optional[Callable[[str], None]] = None,
    max_workers: int = 20,
    extract_full_text: bool = False,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Fetches multiple RSS/Atom feeds in parallel using a ThreadPoolExecutor."""
    all_articles: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    if not feeds_list:
        return all_articles, errors

    workers = min(max_workers, max(1, len(feeds_list)))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_feed = {
            executor.submit(fetch_feed, feed, extract_full_text): feed
            for feed in feeds_list
        }

        for future in as_completed(future_to_feed):
            feed = future_to_feed[future]
            feed_name = feed.get("name", feed.get("url", "Unknown Feed"))
            try:
                articles = future.result()
                all_articles.extend(articles)
                if progress_callback:
                    progress_callback(f"[OK] {feed_name}: Scraped {len(articles)} item(s)")
            except Exception as e:
                err_info = {"feed_name": feed_name, "feed_url": feed.get("url"), "url": feed.get("url"), "error": str(e)}
                errors.append(err_info)
                if progress_callback:
                    progress_callback(f"[ERROR] {feed_name}: {e}")

    return all_articles, errors
