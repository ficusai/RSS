"""Build the header bar: brand badge, stats, sync button, progress bar placeholder."""
# ==============================================================================
# OVERVIEW
# The header bar is the top section of the main window. It contains:
#   - A brand badge ("RSS ENGINE") and subtitle on the left
#   - Two stat badges (article count, feed count) in the middle-right
#   - A "Sync All Feeds" button on the far right
# The function creates a QFrame container and returns it. The caller
# (build_main_window_ui) adds it to the layout.
#
# WHAT: Constructs the header bar QFrame with brand title, article/feed count
#       badges, and a "Sync All Feeds" button. Stores widget references on
#       the window object for later access (lbl_articles_stat, lbl_feeds_stat, btn_sync).
#
# OPTIONS: window — MainWindow instance. Must have attrs: lbl_articles_stat,
#          lbl_feeds_stat, btn_sync (created by this function).
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: Creates and returns a QFrame containing:
#                 - Brand title badge ("⚡ RSS ENGINE")
#                 - Subtitle label ("Feed Tracker & Scraper Pro")
#                 - Article count badge (initially "0 Articles")
#                 - Feed count badge (initially "0 Feeds")
#                 - Sync button (connects to window.start_scrape)
#               The frame is NOT added to any layout — the caller must do that.
#
# ERRORS/EDGE CASES: None expected. All PyQt6 calls are safe with valid inputs.
#
# HOW TO TEST: build_header_bar(window); assert hasattr(window, 'lbl_articles_stat')
#              Running the app should show the header bar at the top.
# ==============================================================================
# PyQt6.QtGui.QFont: controls text appearance.
#   QFont("", 16, QFont.Weight.Bold) creates a font with:
#     - family: "" (empty string = use the system default font)
#     - point size: 16
#     - weight: Bold (makes text stand out)
from PyQt6.QtGui import QFont
# QHBoxLayout: lays out child widgets horizontally (left to right).
# QLabel: displays static text or images.
# QFrame: a container widget that can have borders and background styling.
# QPushButton: a clickable button widget.
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QFrame, QPushButton


def build_header_bar(window) -> None:
    """Build and return the header bar QFrame.

    WHAT: Creates the top header section containing the brand identity,
          live statistics badges, and the sync button. Returns the frame
          for the caller to add to the main layout.

    OPTIONS:
      window: MainWindow instance. This function attaches the following
              widgets as attributes on window for later access:
                - window.lbl_articles_stat: QLabel showing article count
                - window.lbl_feeds_stat: QLabel showing feed count
                - window.btn_sync: QPushButton that triggers scraping

    DEFAULTS: None.

    OUTPUT/EFFECT:
      - Returns a QFrame with objectName="card" (for stylesheet targeting)
      - The frame contains a horizontal layout with:
        1. Brand badge and subtitle (left-aligned)
        2. Stretch spacer (pushes everything right)
        3. Article count badge (blue)
        4. Feed count badge (purple)
        5. Sync button (green accent)

    ERRORS/EDGE CASES: None expected.

    HOW TO TEST:
      1. Call build_header_bar(window)
      2. Verify window.lbl_articles_stat exists
      3. Verify window.lbl_feeds_stat exists
      4. Verify window.btn_sync exists and has text "🔄 Sync All Feeds"
    """
    # QFrame(): creates a container widget. We set objectName="card" so the
    # stylesheet can target it specifically (gives it the dark card background
    # and border defined in STYLESHEET).
    hdr = QFrame()
    hdr.setObjectName("card")

    # QHBoxLayout(hdr): creates a horizontal layout inside the frame.
    # Widgets added to this layout appear left-to-right.
    hdr_layout = QHBoxLayout(hdr)

    # setContentsMargins(16, 10, 16, 10): adds padding inside the frame:
    #   16px left, 10px top, 16px right, 10px bottom
    # This prevents widgets from touching the frame edges.
    hdr_layout.setContentsMargins(16, 10, 16, 10)

    # --- Brand Section (left side) ---
    # QHBoxLayout(): creates a nested horizontal layout for the brand elements.
    brand_box = QHBoxLayout()
    # setSpacing(10): adds 10px between the badge and subtitle.
    brand_box.setSpacing(10)

    # QLabel("⚡ RSS ENGINE"): creates the brand title label.
    # The ⚡ emoji is part of the display text.
    title_badge = QLabel("⚡ RSS ENGINE")

    # setFont(): sets the text appearance.
    # QFont("", 16, QFont.Weight.Bold) means: default font family, 16pt size, bold weight.
    title_badge.setFont(QFont("", 16, QFont.Weight.Bold))

    # setStyleSheet(): applies inline CSS-like styling to this specific widget.
    # - color: #ffffff (white text)
    # - background: #1f6feb (blue background, matches GitHub's primary blue)
    # - padding: 4px vertical, 12px horizontal
    # - border-radius: 6px (rounded corners)
    # - font-weight: bold (redundant with QFont but ensures consistency)
    title_badge.setStyleSheet(
        "color: #ffffff; background: #1f6feb; padding: 4px 12px; border-radius: 6px; font-weight: bold;"
    )

    # QLabel("Feed Tracker & Scraper Pro"): creates the subtitle label.
    subtitle_lbl = QLabel("Feed Tracker & Scraper Pro")
    # Same font styling as the title but white text instead of on a colored background.
    subtitle_lbl.setFont(QFont("", 16, QFont.Weight.Bold))
    subtitle_lbl.setStyleSheet("color: #e6edf3; font-weight: bold;")

    # addWidget(): adds the brand elements to the brand_box layout.
    brand_box.addWidget(title_badge)
    brand_box.addWidget(subtitle_lbl)

    # Add the brand section to the main header layout.
    hdr_layout.addLayout(brand_box)

    # addStretch(): adds a flexible empty space that pushes everything after it
    # to the right. This separates the brand (left) from the stats/buttons (right).
    hdr_layout.addStretch()

    # QLabel("0 Articles"): creates the article count badge, initially showing 0.
    # This is updated by update_stats_badges() when data is loaded.
    window.lbl_articles_stat = QLabel("0 Articles")
    # Inline stylesheet: dark background, blue text (#58a6ff), rounded corners.
    # The blue color visually associates this with "articles" content.
    window.lbl_articles_stat.setStyleSheet(
        "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 4px 14px; color: #58a6ff; font-weight: 600;"
    )

    # QLabel("0 Feeds"): creates the feed count badge, initially showing 0.
    # Updated by update_stats_badges() when feeds are loaded.
    window.lbl_feeds_stat = QLabel("0 Feeds")
    # Purple text (#a371f7) distinguishes this badge from the article count.
    window.lbl_feeds_stat.setStyleSheet(
        "background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 4px 14px; color: #a371f7; font-weight: 600;"
    )

    # Add both stat badges to the header layout.
    hdr_layout.addWidget(window.lbl_articles_stat)
    hdr_layout.addWidget(window.lbl_feeds_stat)

    # addSpacing(10): adds 10px of empty space between the stat badges and the sync button.
    hdr_layout.addSpacing(10)

    # QPushButton("🔄 Sync All Feeds"): creates the main action button.
    # The 🔄 emoji indicates refresh/sync action.
    window.btn_sync = QPushButton("🔄 Sync All Feeds")

    # setObjectName("accent"): tells the stylesheet to apply the green "accent"
    # button style (#1a5a2e background, #3fb950 text). This is the primary
    # action button in the interface.
    window.btn_sync.setObjectName("accent")

    # clicked.connect(): connects the button's click event to the window's
    # start_scrape method. When the user clicks this button, start_scrape() runs.
    # In PyQt6, clicked signal does NOT pass arguments to 0-arg slots.
    window.btn_sync.clicked.connect(window.start_scrape)

    # Add the sync button to the header layout (it appears on the far right
    # because addStretch() pushed it there).
    hdr_layout.addWidget(window.btn_sync)

    # Return the completed header frame. The caller (build_main_window_ui)
    # will add this to the main vertical layout.
    return hdr
