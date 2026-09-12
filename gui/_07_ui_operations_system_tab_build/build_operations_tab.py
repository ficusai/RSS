"""Build the Operations & System tab (Tab 3)."""
# ==============================================================================
# OVERVIEW
# Tab 3 is the "Operations & System" tab — a monitoring and control panel for
# the app's background scheduling system. It contains two sections:
#   1. Systemd Status Card: shows whether the Linux systemd timer is installed,
#      active, and enabled for auto-start. Includes refresh and install buttons.
#   2. Live Operations Log: a read-only console showing timestamped messages
#      from scrapes, errors, and system events.
#
# WHAT: Creates the operations tab with a systemd status card and a live log
#       console, then adds it as Tab 3 to window.tabs.
#
# OPTIONS: window — MainWindow instance. Stores widget references:
#            - window.btn_refresh_sys: refresh status button
#            - window.btn_install_timer: install systemd timer button
#            - window.lbl_sys_service, window.lbl_sys_timer, window.lbl_sys_enabled: status badges
#            - window.btn_clear: clear log button
#            - window.log_box: read-only console for log messages
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: Creates tab_ops widget and adds it as "⚙️ Operations & System" tab.
#
# ERRORS/EDGE CASES: None expected. All widget creation is safe.
#
# HOW TO TEST: build_operations_tab(window); assert window.tabs.count() >= 3
#              Running the app and clicking Tab 3 should show the operations panel.
# ==============================================================================
from PyQt6.QtWidgets import (
    QHBoxLayout,      # horizontal layout
    QLabel,           # text labels
    QPushButton,      # clickable buttons
    QFrame,           # bordered container
    QTextEdit,        # multi-line text display (log console)
    QVBoxLayout,      # vertical layout
    QWidget,          # base widget
    QSizePolicy,      # size policy for expanding widgets
)


def build_operations_tab(window) -> None:
    """Build and add the Operations & System tab.

    WHAT: Creates Tab 3 — the system monitoring interface. Contains two cards:
          1. Systemd Status Card: service/timer/enabled badges + control buttons
          2. Operations Log Card: live timestamped message console

    OPTIONS:
      window: MainWindow instance. This function creates and stores the following
              widget attributes on window:
                - window.btn_refresh_sys: refresh systemd status button
                - window.btn_install_timer: install timer button
                - window.lbl_sys_service: service status badge
                - window.lbl_sys_timer: timer status badge
                - window.lbl_sys_enabled: auto-start status badge
                - window.btn_clear: clear log button
                - window.log_box: read-only log console (QTextEdit)

    DEFAULTS: None.

    OUTPUT/EFFECT:
      - Creates a QWidget (tab_ops) containing:
        1. Systemd status card with three badges and two buttons
        2. Operations log card with clear button and read-only console

    ERRORS/EDGE CASES: None expected.

    HOW TO TEST:
      1. Call build_operations_tab(window)
      2. Verify window.tabs.count() >= 3
      3. Verify window.log_box exists and is a QTextEdit
    """
    # QWidget(): creates the tab container.
    tab_ops = QWidget()

    # QVBoxLayout: stack the two cards vertically.
    ops_l = QVBoxLayout(tab_ops)
    ops_l.setContentsMargins(10, 10, 10, 10)
    ops_l.setSpacing(12)

    # --- Systemd Status Card ---
    # QFrame(): bordered container for the systemd status section.
    # setObjectName("card"): applies the dark card style from STYLESHEET.
    card_systemd = QFrame()
    card_systemd.setObjectName("card")

    # QVBoxLayout inside the card.
    sys_v = QVBoxLayout(card_systemd)
    sys_v.setContentsMargins(14, 12, 14, 12)
    sys_v.setSpacing(10)

    # --- Card Header Row ---
    sys_header = QHBoxLayout()

    # QLabel: section title.
    sys_title = QLabel("⚙️ Linux Systemd Background Scheduler Daemon")
    sys_title.setStyleSheet("color: #e6edf3; font-size: 16px; font-weight: bold;")
    sys_header.addWidget(sys_title)
    sys_header.addStretch()  # Push buttons to the right

    # QPushButton: refresh the status display.
    window.btn_refresh_sys = QPushButton("🔄 Refresh Status")
    window.btn_refresh_sys.clicked.connect(window.refresh_systemd_status)
    sys_header.addWidget(window.btn_refresh_sys)

    # QPushButton: install/enable the systemd timer (runs scrapes every 12h).
    window.btn_install_timer = QPushButton("⚡ Install / Enable 12-Hour Systemd Timer")
    window.btn_install_timer.setObjectName("accent")  # Green accent style
    window.btn_install_timer.clicked.connect(window.handle_install_systemd)
    sys_header.addWidget(window.btn_install_timer)

    sys_v.addLayout(sys_header)

    # --- Status Badges Row ---
    status_box = QHBoxLayout()
    status_box.setSpacing(12)

    # Three status badges, initialized to "Checking..." until first query.
    # Each badge uses inline styling: dark background, border, rounded corners.
    window.lbl_sys_service = QLabel("Service: Checking...")
    window.lbl_sys_service.setStyleSheet(
        "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 14px; font-weight: 600;"
    )

    window.lbl_sys_timer = QLabel("Timer: Checking...")
    window.lbl_sys_timer.setStyleSheet(
        "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 14px; font-weight: 600;"
    )

    window.lbl_sys_enabled = QLabel("Enabled: Checking...")
    window.lbl_sys_enabled.setStyleSheet(
        "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 14px; font-weight: 600;"
    )

    status_box.addWidget(window.lbl_sys_service)
    status_box.addWidget(window.lbl_sys_timer)
    status_box.addWidget(window.lbl_sys_enabled)
    status_box.addStretch()
    sys_v.addLayout(status_box)

    # Add the systemd card to the main layout.
    ops_l.addWidget(card_systemd)

    # --- Operations Log Card ---
    ops_box = QFrame()
    ops_box.setObjectName("card")
    ops_v = QVBoxLayout(ops_box)
    ops_v.setContentsMargins(14, 12, 14, 12)
    ops_v.setSpacing(8)

    # --- Log Header Row ---
    sched_l = QHBoxLayout()
    sched_l.setSpacing(10)

    ops_title = QLabel("📜 Live Operations Log")
    ops_title.setStyleSheet("color: #8b949e; font-size: 15px; font-weight: bold;")
    sched_l.addWidget(ops_title)
    sched_l.addStretch()  # Push clear button to the right

    # QPushButton: clear all log messages.
    window.btn_clear = QPushButton("🧹 Clear Log")
    window.btn_clear.clicked.connect(window.clear_log)
    sched_l.addWidget(window.btn_clear)
    ops_v.addLayout(sched_l)

    # QTextEdit: read-only console for displaying log messages.
    # setObjectName("log_console"): applies the terminal-style styling from STYLESHEET
    # (dark background #010409, green monospace text #7ee787).
    window.log_box = QTextEdit()
    window.log_box.setObjectName("log_console")
    window.log_box.setReadOnly(True)  # Users can read but not edit
    ops_v.addWidget(window.log_box, 1)  # '1' stretch: log fills remaining space

    ops_l.addWidget(ops_box, 1)  # '1' stretch: card fills remaining height

    # Add this tab to the main tab widget.
    tab_ops.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    window.tabs.addTab(tab_ops, "⚙️ Operations & System")
