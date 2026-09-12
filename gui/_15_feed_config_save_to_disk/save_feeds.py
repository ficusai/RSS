"""Write window.feeds to config/feeds.json."""
# WHAT: Serialises window.feeds as {"feeds": [...]} to disk.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: Creates parent directories if needed.
# OUTPUT/EFFECT: config/feeds.json updated.
# ERRORS/EDGE CASES: Permission errors logged to window log.
# HOW TO TEST: window.feeds = [...]; save_feeds(window); re-load and assert equality
import json
from pathlib import Path

from gui._00_paths_config_constant_definitions.paths_config_constants import CONFIG_PATH
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message


def save_feeds(window) -> None:
    """Persist window.feeds to config/feeds.json."""
    config_path = CONFIG_PATH
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({"feeds": window.feeds}, f, indent=2, ensure_ascii=False)
    except Exception as e:
        append_log_message(window, f"Save error: {e}")
