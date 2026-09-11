"""Single-function module for installing systemd timer and service user units."""
import os
import subprocess
import sys
from pathlib import Path

SYSTEMD_USER_DIR = Path.home() / ".config" / "systemd" / "user"
SERVICE_FILE = SYSTEMD_USER_DIR / "rss-scraper.service"
TIMER_FILE = SYSTEMD_USER_DIR / "rss-scraper.timer"


def install_systemd_timer() -> bool:
    """
    Creates ~/.config/systemd/user/rss-scraper.service and rss-scraper.timer.
    """
    try:
        SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)

        python_bin = sys.executable
        project_dir = Path(__file__).resolve().parent.parent.parent.parent

        service_content = f"""[Unit]
Description=RSS Feed Scraper Automated Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory={project_dir}
ExecStart={python_bin} {project_dir}/main.py --headless
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

        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True, capture_output=True)
        subprocess.run(
            ["systemctl", "--user", "enable", "--now", "rss-scraper.timer"],
            check=True,
            capture_output=True,
        )

        return True
    except Exception as e:
        print(f"Failed to install systemd timer: {e}")
        return False
