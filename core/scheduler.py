"""
Systemd timer installation and management for RSS feed scraper.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


SYSTEMD_USER_DIR = Path.home() / ".config" / "systemd" / "user"
SERVICE_FILE = SYSTEMD_USER_DIR / "rss-scraper.service"
TIMER_FILE = SYSTEMD_USER_DIR / "rss-scraper.timer"


def install_systemd_timer() -> bool:
    """
    Creates ~/.config/systemd/user/rss-scraper.service and rss-scraper.timer
    Configured to run every 12 hours (OnCalendar=*-*-* 00,12:00:00, persistent).
    Reloads systemd user daemon and enables/starts timer.
    Returns True if successful, False otherwise.
    """
    try:
        SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)

        python_bin = sys.executable
        project_dir = Path("/home/ficus-pro/Documents/RSS")

        service_content = f"""[Unit]
Description=RSS Feed Scraper Automated Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory={project_dir}
ExecStart={python_bin} -c "from core.fetcher import fetch_all_feeds; from core.storage import save_articles; import json, pathlib; config_path = pathlib.Path('{project_dir}/config/feeds.json'); feeds = json.loads(config_path.read_text())['feeds'] if config_path.exists() else []; articles, _ = fetch_all_feeds(feeds); save_articles(articles)"
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
"""

        timer_content = """[Unit]
Description=RSS Feed Scraper 12-Hour Timer

[Timer]
OnCalendar=*-*-* 00,12:00:00
Persistent=true

[Install]
WantedBy=timers.target
"""

        with open(SERVICE_FILE, "w", encoding="utf-8") as f:
            f.write(service_content)

        with open(TIMER_FILE, "w", encoding="utf-8") as f:
            f.write(timer_content)

        # Reload systemd user daemon
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True, capture_output=True)

        # Enable and start timer
        subprocess.run(
            ["systemctl", "--user", "enable", "--now", "rss-scraper.timer"],
            check=True,
            capture_output=True,
        )

        return True
    except Exception as e:
        print(f"Failed to install systemd timer: {e}")
        return False


def get_timer_status() -> Dict[str, Any]:
    """
    Checks if systemd user timer is active and enabled.
    Returns status dict containing installed, active, enabled, and detail fields.
    """
    installed = SERVICE_FILE.exists() and TIMER_FILE.exists()
    active = False
    enabled = False
    detail = ""

    if installed:
        try:
            res_act = subprocess.run(
                ["systemctl", "--user", "is-active", "rss-scraper.timer"],
                capture_output=True,
                text=True,
            )
            active = res_act.stdout.strip() == "active"

            res_ena = subprocess.run(
                ["systemctl", "--user", "is-enabled", "rss-scraper.timer"],
                capture_output=True,
                text=True,
            )
            enabled = res_ena.stdout.strip() == "enabled"

            res_status = subprocess.run(
                ["systemctl", "--user", "status", "rss-scraper.timer"],
                capture_output=True,
                text=True,
            )
            detail = res_status.stdout.strip() or res_status.stderr.strip()
        except Exception as e:
            detail = f"Error querying systemd: {e}"
    else:
        detail = "Systemd service and timer unit files not installed."

    return {
        "installed": installed,
        "active": active,
        "enabled": enabled,
        "detail": detail,
    }
