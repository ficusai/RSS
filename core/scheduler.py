"""
Systemd timer installation and management for RSS feed scraper.
"""

# WHAT: Operating system environment utilities module.
# OPTIONS/VALUES: os.environ, os.path.
# DEFAULTS: Standard Python library module.
# OUTPUT/EFFECT: Provides OS interaction functions.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "import os; print(os.name)"'.
import os

# WHAT: Subprocess management library for executing Linux systemctl terminal commands from Python code.
# OPTIONS/VALUES: subprocess.run(), check=True, capture_output=True, text=True.
# DEFAULTS: Runs shell systemctl commands synchronously.
# OUTPUT/EFFECT: Controls systemd user daemon, service units, and timer schedules.
# ERRORS/EDGE CASES: Throws CalledProcessError if systemctl command fails.
# HOW TO TEST: Run 'python3 -c "import subprocess; print(subprocess.run([\"systemctl\", \"--user\", \"is-active\", \"rss-scraper.timer\"], capture_output=True, text=True).stdout)"'.
import subprocess

# WHAT: System parameters module providing path to current Python binary (sys.executable).
# OPTIONS/VALUES: sys.executable (e.g. /usr/bin/python3).
# DEFAULTS: Standard library module.
# OUTPUT/EFFECT: Ensures systemd service uses the exact Python interpreter executing the application.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "import sys; print(sys.executable)"'.
import sys

# WHAT: Object-oriented filesystem path handler.
# OPTIONS/VALUES: Path.home(), Path("/home/ficus-pro/Documents/RSS").
# DEFAULTS: Resolves home directories (~/.config/systemd/user).
# OUTPUT/EFFECT: Constructs paths to systemd user configuration directory.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "from pathlib import Path; print(Path.home() / \".config\")"'.
from pathlib import Path

# WHAT: Type hinting classes for dicts and generic types.
# OPTIONS/VALUES: Any, Dict.
# DEFAULTS: Static typing annotations.
# OUTPUT/EFFECT: Enables type checking.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Checked by static code analysis tools.
from typing import Any, Dict

# WHAT: Path to user systemd configuration folder (~/.config/systemd/user).
# OPTIONS/VALUES: Path object pointing to ~/.config/systemd/user.
# DEFAULTS: Standard Linux user systemd location.
# OUTPUT/EFFECT: Directory where service and timer unit files are installed.
# ERRORS/EDGE CASES: Permission error if user home directory is restricted.
# HOW TO TEST: Run 'ls -la ~/.config/systemd/user'.
SYSTEMD_USER_DIR = Path.home() / ".config" / "systemd" / "user"

# WHAT: Path pointing to the generated systemd service file (rss-scraper.service).
# OPTIONS/VALUES: ~/.config/systemd/user/rss-scraper.service.
# DEFAULTS: Target location for service unit definition.
# OUTPUT/EFFECT: Defines systemd background scrape job execution commands.
# ERRORS/EDGE CASES: Overwritten if timer reinstall is triggered.
# HOW TO TEST: Run 'cat ~/.config/systemd/user/rss-scraper.service'.
SERVICE_FILE = SYSTEMD_USER_DIR / "rss-scraper.service"

# WHAT: Path pointing to the generated systemd timer file (rss-scraper.timer).
# OPTIONS/VALUES: ~/.config/systemd/user/rss-scraper.timer.
# DEFAULTS: Target location for 12-hour schedule definition.
# OUTPUT/EFFECT: Defines timer schedule (OnCalendar=*-*-* 00,12:00:00).
# ERRORS/EDGE CASES: Overwritten on reinstall.
# HOW TO TEST: Run 'systemctl --user status rss-scraper.timer'.
TIMER_FILE = SYSTEMD_USER_DIR / "rss-scraper.timer"


# WHAT: Installs and enables the background systemd timer to automatically run the RSS scraper twice a day (every 12 hours).
# OPTIONS/VALUES: Returns True if systemd daemon was reloaded and timer enabled successfully; False on failure.
# DEFAULTS: OnCalendar=*-*-* 00,12:00:00 (runs at midnight 00:00 and noon 12:00 UTC/local).
# OUTPUT/EFFECT: Writes unit files, runs daemon-reload, and enables timer.
# ERRORS/EDGE CASES: Catches missing systemd environment, permission errors, or systemctl failures.
# HOW TO TEST: Call install_systemd_timer() and check 'systemctl --user list-timers'.
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


# WHAT: Inspects whether the systemd user timer unit files exist, are enabled, and actively running.
# OPTIONS/VALUES: Returns dict with boolean keys 'installed', 'active', 'enabled', and string 'detail'.
# DEFAULTS: Returns active=False if timer is inactive.
# OUTPUT/EFFECT: Provides status information to the GUI header stat card.
# ERRORS/EDGE CASES: Returns detail error message if systemctl query fails.
# HOW TO TEST: Run 'python3 -c "from core.scheduler import get_timer_status; print(get_timer_status())"'.
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
