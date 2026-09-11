"""Single-function module for inspecting systemd timer status."""
import subprocess
from pathlib import Path
from typing import Any, Dict

SYSTEMD_USER_DIR = Path.home() / ".config" / "systemd" / "user"
SERVICE_FILE = SYSTEMD_USER_DIR / "rss-scraper.service"
TIMER_FILE = SYSTEMD_USER_DIR / "rss-scraper.timer"


def get_timer_status() -> Dict[str, Any]:
    """Inspects whether systemd user timer is active and enabled."""
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
