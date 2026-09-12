"""Query systemd scheduler status and update the three status badges."""
# WHAT: Calls get_timer_status() and colors the Service/Timer/Enabled labels
#       green (active) or gray/red (inactive) accordingly.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: On exception, logs the error.
# OUTPUT/EFFECT: lbl_sys_service, lbl_sys_timer, lbl_sys_enabled updated.
# ERRORS/EDGE CASES: get_timer_status() may raise if systemd is unavailable.
# HOW TO TEST: refresh_systemd_status(window)
from features.feature_systemd_scheduler.implementation.scheduler import get_timer_status
from gui._10_log_append_timestamped_message.append_timestamped_log import append_log_message


def refresh_systemd_status(window) -> None:
    """Refresh the systemd status badges from get_timer_status()."""
    try:
        st = get_timer_status()
        inst = st.get("installed", False)
        act = st.get("active", False)
        ena = st.get("enabled", False)

        if inst:
            window.lbl_sys_service.setText("Service Unit: Installed")
            window.lbl_sys_service.setStyleSheet(
                "background: #0d1117; border: 1px solid #238636; border-radius: 6px; padding: 8px 14px; color: #3fb950; font-weight: 600;"
            )
        else:
            window.lbl_sys_service.setText("Service Unit: Not Installed")
            window.lbl_sys_service.setStyleSheet(
                "background: #0d1117; border: 1px solid #da3633; border-radius: 6px; padding: 8px 14px; color: #f85149; font-weight: 600;"
            )

        if act:
            window.lbl_sys_timer.setText("Timer Status: Active")
            window.lbl_sys_timer.setStyleSheet(
                "background: #0d1117; border: 1px solid #238636; border-radius: 6px; padding: 8px 14px; color: #3fb950; font-weight: 600;"
            )
        else:
            window.lbl_sys_timer.setText("Timer Status: Inactive")
            window.lbl_sys_timer.setStyleSheet(
                "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 14px; color: #8b949e; font-weight: 600;"
            )

        if ena:
            window.lbl_sys_enabled.setText("Systemd Auto-Start: Enabled")
            window.lbl_sys_enabled.setStyleSheet(
                "background: #0d1117; border: 1px solid #238636; border-radius: 6px; padding: 8px 14px; color: #3fb950; font-weight: 600;"
            )
        else:
            window.lbl_sys_enabled.setText("Systemd Auto-Start: Disabled")
            window.lbl_sys_enabled.setStyleSheet(
                "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 14px; color: #8b949e; font-weight: 600;"
            )
    except Exception as e:
        append_log_message(window, f"Error checking systemd status: {e}")
