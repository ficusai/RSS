"""Read config/feeds.json and populate window.feeds."""
# WHAT: Loads the subscribed feeds list from disk into window.feeds.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: If file missing or corrupt, window.feeds = [].
# OUTPUT/EFFECT: window.feeds populated from JSON.
# ERRORS/EDGE CASES: File may be missing, malformed, or not a list/dict.
# HOW TO TEST: load_feeds(window); assert isinstance(window.feeds, list)
import json
from pathlib import Path

from gui._00_paths_config_constant_definitions.paths_config_constants import CONFIG_PATH


def load_feeds(window) -> None:
    """Load subscribed feeds from config/feeds.json into window.feeds."""
    config_path = CONFIG_PATH
    if not config_path.exists():
        window.feeds = []
        return
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            window.feeds = data.get("feeds", data) if isinstance(data, dict) else data
    except Exception:
        window.feeds = []
