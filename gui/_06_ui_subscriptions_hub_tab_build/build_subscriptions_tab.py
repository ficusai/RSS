"""Build the Subscriptions Hub tab (Tab 2)."""
# ==============================================================================
# OVERVIEW
# Tab 2 is the "Subscriptions Hub" — where users manage their RSS feed subscriptions.
# It contains:
#   - A search/filter bar at the top
#   - A collapsible "drawer" for adding new feeds and quick-importing presets
#   - A table showing all subscribed feeds with controls (interval, enabled, ping, delete)
#
# The drawer is hidden by default and toggled by the "New Feed / Presets ▾" button.
#
# WHAT: Creates the subscriptions tab with filter bar, collapsible add-drawer,
#       two-tier preset dropdown (category → feed name), and a feed management table.
#
# OPTIONS: window — MainWindow instance. Stores widget references:
#            - window.in_filter: search box for filtering feeds
#            - window.cb_cat_filter: category dropdown
#            - window.btn_toggle_drawer: button to show/hide the add drawer
#            - window.drawer_box: collapsible panel with add form + preset dropdowns
#            - window.in_name, window.in_url, window.in_cat: form inputs
#            - window.cb_freq: frequency dropdown (1h/3h/6h/12h/24h)
#            - window.btn_add: add feed button
#            - window.table_feeds: feed management table
#            - window.cb_preset_cat: category selector for preset quick-import
#            - window.cb_preset_select: preset feed selector, filtered by category
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: Creates tab_feed widget and adds it as Tab 2 to window.tabs.
#
# ERRORS/EDGE CASES: None expected. The get_preset_feeds() import may fail if
#                    the presets library feature is not installed, but this is
#                    handled gracefully (empty preset list).
#
# HOW TO TEST: build_subscriptions_tab(window); assert window.tabs.count() >= 2
#              Running the app and clicking Tab 2 should show the subscriptions hub.
# ==============================================================================
# Qt.AlignmentFlag: alignment options for widgets in layouts.
from PyQt6.QtCore import Qt
# Various Qt widgets:
from PyQt6.QtWidgets import (
    QHBoxLayout,      # horizontal layout
    QLabel,           # text labels
    QLineEdit,        # text input boxes
    QComboBox,        # dropdown menus
    QPushButton,      # clickable buttons
    QTableWidget,     # spreadsheet-style table
    QHeaderView,      # column header controls
    QFrame,           # bordered container (drawer)
    QVBoxLayout,      # vertical layout
    QWidget,          # base widget
)

# Import the presets library to populate the two-tier quick-import dropdown.
# get_preset_feeds() returns a list of dicts with 'name', 'url', 'category' keys.
# get_preset_categories() returns an ordered list of all category names.
from features.feature_feed_presets_library.implementation.feeds_presets import (
    get_preset_feeds,
    get_preset_categories,
)


def _refresh_preset_dropdown(window, category_index: int) -> None:
    """Repopulate window.cb_preset_select based on the selected category.

    WHAT: Filters window._preset_feeds by the category at index
      category_index of window.cb_preset_cat, then clears and refills
      window.cb_preset_select with matching preset names. Index 0
      corresponds to "All Categories" and shows all presets.
    OPTIONS:
      window — MainWindow instance with cb_preset_cat, cb_preset_select,
               and _preset_feeds attributes already set up.
      category_index — integer index returned by QComboBox::currentIndexChanged.
    DEFAULTS: N/A.
    OUTPUT/EFFECT: cb_preset_select is cleared, re-populated with matching
      names (prefixed with a placeholder "— Select a feed —" at index 0),
      and reset to index 0 so no feed is auto-selected on category change.
    ERRORS/EDGE CASES: If window._preset_feeds is empty or missing, the
      dropdown is left with only the placeholder item.
    """
    # Re-display the placeholder at index 0.
    cat_text = window.cb_preset_cat.itemText(category_index) if 0 <= category_index < window.cb_preset_cat.count() else "All Categories"
    window.cb_preset_select.blockSignals(True)
    window.cb_preset_select.clear()
    window.cb_preset_select.addItem("— Select a feed —")
    presets = window._preset_feeds if hasattr(window, "_preset_feeds") else []
    if cat_text and cat_text != "All Categories":
        filtered = [p for p in presets if (p.get("category") or "").strip() == cat_text]
    else:
        filtered = presets
    for p in filtered:
        window.cb_preset_select.addItem(p.get("name", "Unknown"))
    window.cb_preset_select.setCurrentIndex(0)
    window.cb_preset_select.blockSignals(False)


def _import_selected_preset(window, preset_index: int) -> None:
    """Import the preset feed selected at the given index in cb_preset_select.

    WHAT: Looks up the preset dict from window._preset_feeds by the name
      stored at preset_index in window.cb_preset_select, then calls
      window.import_preset(name, url, category) to subscribe it.
      If preset_index is 0 (the placeholder), nothing happens.
    OPTIONS:
      window — MainWindow instance with cb_preset_select and _preset_feeds.
      preset_index — integer index from QComboBox::currentIndexChanged.
    DEFAULTS: N/A.
    OUTPUT/EFFECT: Calls window.import_preset if a real preset is selected.
    ERRORS/EDGE CASES: If the preset cannot be found by name, nothing happens.
    """
    if preset_index <= 0:
        return
    name = window.cb_preset_select.itemText(preset_index)
    presets = window._preset_feeds if hasattr(window, "_preset_feeds") else []
    match = next((p for p in presets if p.get("name") == name), None)
    if match is None:
        return
    window.import_preset(
        match.get("name", name),
        match.get("url", ""),
        match.get("category", "General"),
    )


def build_subscriptions_tab(window) -> None:
    """Build and add the Subscriptions Hub tab.

    WHAT: Creates Tab 2 — the feed management interface. Contains a filter bar,
          a collapsible drawer for adding feeds and importing presets, and a
          table listing all subscribed feeds with per-row controls.

    OPTIONS:
      window: MainWindow instance. This function creates and stores the following
              widget attributes on window:
                - window.in_filter: search box
                - window.cb_cat_filter: category filter dropdown
                - window.btn_toggle_drawer: show/hide drawer button
                - window.btn_toggle_url: show/hide URL column button
                - window.drawer_box: collapsible add-form panel (QFrame)
                - window.in_name, window.in_url, window.in_cat: form inputs
                - window.cb_freq: interval dropdown
                - window.btn_add: add feed button
                - window.table_feeds: feed management table
                - window.cb_preset_cat: category selector for preset import
                - window.cb_preset_select: preset feed selector dropdown
                - window._url_visible: bool tracking URL column state (default False)

    DEFAULTS: None.

    OUTPUT/EFFECT:
      - Creates a QWidget (tab_feed) containing:
        1. Header with title, search, category filter, toggle button
        2. Collapsible drawer (hidden by default) with:
           - Add-feed form (name, URL, category, interval, add button)
           - Two-tier preset quick-import: category selector → feed name selector
        3. Feed management table with 6 columns: Name, URL, Category, Interval, Active, Actions

    ERRORS/EDGE CASES: None expected. Preset dropdown handles empty preset lists.

    HOW TO TEST:
      1. Call build_subscriptions_tab(window)
      2. Verify window.tabs.count() >= 2
      3. Verify window.drawer_box exists
      4. Verify window.table_feeds has 6 columns
    """
    # QWidget(): creates the tab's container.
    tab_feed = QWidget()

    # QVBoxLayout: stack widgets vertically (filter bar, drawer, table).
    feed_l = QVBoxLayout(tab_feed)
    feed_l.setContentsMargins(10, 10, 10, 10)
    feed_l.setSpacing(10)

    # --- Header Bar (filter controls) ---
    catalog_header = QHBoxLayout()
    catalog_header.setSpacing(10)

    # QLabel("📡 Subscriptions Catalog"): tab title.
    catalog_title = QLabel("📡 Subscriptions Catalog")
    catalog_title.setStyleSheet("color: #e6edf3; font-size: 16px; font-weight: bold;")

    # QLineEdit: search box to filter feeds by name or URL.
    window.in_filter = QLineEdit()
    window.in_filter.setPlaceholderText("Filter feeds by name or URL...")
    # textChanged: refresh table as user types.
    window.in_filter.textChanged.connect(window.refresh_table)

    # QComboBox: dropdown to filter by category.
    window.cb_cat_filter = QComboBox()
    window.cb_cat_filter.addItem("All Categories")
    window.cb_cat_filter.setMinimumWidth(180)
    # currentIndexChanged: refresh table when category changes.
    window.cb_cat_filter.currentIndexChanged.connect(window.refresh_table)

    # QPushButton: toggle the add-drawer visibility.
    window.btn_toggle_drawer = QPushButton("➕ New Feed / Presets ▾")
    window.btn_toggle_drawer.setObjectName("primary_blue")
    window.btn_toggle_drawer.clicked.connect(window.toggle_add_drawer)

    # QPushButton: toggle RSS Endpoint URL column visibility.
    window.btn_toggle_url = QPushButton("🔗 URL")
    window.btn_toggle_url.setObjectName("secondary")
    window.btn_toggle_url.setMaximumWidth(80)
    window.btn_toggle_url.clicked.connect(window.toggle_url_column)
    window._url_visible = False

    # Add controls to header layout (title left, stretch, then filters/button right).
    catalog_header.addWidget(catalog_title)
    catalog_header.addStretch()
    catalog_header.addWidget(window.in_filter, 1)
    catalog_header.addWidget(window.cb_cat_filter)
    catalog_header.addWidget(window.btn_toggle_drawer)
    catalog_header.addWidget(window.btn_toggle_url)
    feed_l.addLayout(catalog_header)

    # --- Collapsible Add & Presets Drawer ---
    # QFrame(): bordered container for the drawer. Initially hidden.
    window.drawer_box = QFrame()
    window.drawer_box.setObjectName("card")
    window.drawer_box.setVisible(False)  # Hidden by default; toggled by button
    drawer_v = QVBoxLayout(window.drawer_box)
    drawer_v.setContentsMargins(12, 12, 12, 12)
    drawer_v.setSpacing(10)

    # --- Add Feed Form Row ---
    add_top = QHBoxLayout()
    add_top.setSpacing(10)

    # QLineEdit: feed name input.
    window.in_name = QLineEdit()
    window.in_name.setPlaceholderText("Feed Name (e.g. TechCrunch)")

    # QLineEdit: RSS URL input.
    window.in_url = QLineEdit()
    window.in_url.setPlaceholderText("RSS URL (e.g. https://techcrunch.com/feed/)")

    # QLineEdit: category input (defaults to "General").
    window.in_cat = QLineEdit()
    window.in_cat.setText("General")  # Default category
    window.in_cat.setPlaceholderText("Category")
    window.in_cat.setMaximumWidth(180)

    # QComboBox: fetch interval selection.
    # addItems(): adds the five available intervals.
    # setCurrentIndex(3): selects "12h" by default (index 3 of 5 options).
    window.cb_freq = QComboBox()
    window.cb_freq.addItems(["1h", "3h", "6h", "12h", "24h"])
    window.cb_freq.setCurrentIndex(3)
    window.cb_freq.setMaximumWidth(110)

    # QPushButton: submit the new feed.
    window.btn_add = QPushButton("➕ Add Feed")
    window.btn_add.setObjectName("accent")
    window.btn_add.clicked.connect(window.add_feed)

    # Arrange form controls horizontally.
    add_top.addWidget(window.in_name, 1)
    add_top.addWidget(window.in_url, 2)
    add_top.addWidget(window.in_cat)
    add_top.addWidget(window.cb_freq)
    add_top.addWidget(window.btn_add)
    drawer_v.addLayout(add_top)

    # --- Two-Tier Preset Quick-Import Dropdown ---
    # Store all presets on the window for lookup by name during import.
    try:
        all_presets = get_preset_feeds()
    except Exception:
        all_presets = []
    window._preset_feeds = all_presets

    # QLabel: section label for the preset importer.
    lbl_import = QLabel("Quick Import:")
    lbl_import.setStyleSheet("color: #8b949e; font-size: 14px; font-weight: 600;")
    drawer_v.addWidget(lbl_import)

    # QComboBox: category selector — populates window.cb_preset_cat.
    # Starts with "All Categories" then appends each preset category.
    window.cb_preset_cat = QComboBox()
    window.cb_preset_cat.setMinimumWidth(200)
    try:
        cats = ["All Categories"] + get_preset_categories()
    except Exception:
        cats = ["All Categories"]
    window.cb_preset_cat.addItems(cats)
    # currentIndexChanged: filter the preset dropdown when the category changes.
    window.cb_preset_cat.currentIndexChanged.connect(
        lambda i: _refresh_preset_dropdown(window, i)
    )
    drawer_v.addWidget(window.cb_preset_cat)

    # QComboBox: preset feed selector — populates window.cb_preset_select.
    # Populated dynamically based on the selected category from cb_preset_cat.
    window.cb_preset_select = QComboBox()
    window.cb_preset_select.setMinimumWidth(280)
    window.cb_preset_select.addItem("— Select a feed —")
    # Set current index to 0 so the placeholder is shown initially.
    window.cb_preset_select.setCurrentIndex(0)
    # currentIndexChanged: when a preset is picked, look it up and import it.
    window.cb_preset_select.currentIndexChanged.connect(
        lambda i: _import_selected_preset(window, i)
    )
    drawer_v.addWidget(window.cb_preset_select)

    # Add the drawer to the main tab layout.
    feed_l.addWidget(window.drawer_box)

    # --- Subscriptions Table ---
    # QTableWidget(): spreadsheet-style table for managing feeds.
    window.table_feeds = QTableWidget()
    window.table_feeds.setColumnCount(6)
    window.table_feeds.setHorizontalHeaderLabels(["Name", "RSS Endpoint URL", "Category", "Interval", "Active", "Actions"])

    # Configure column resizing: Name stretches to fill available width;
    # every other column auto-sizes to its content (no manual dragging needed).
    header = window.table_feeds.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)     # Name
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # URL (hidden by default)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Category
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Interval
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Active
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Actions

    # Hide row numbers, set row height, enable alternating colors.
    window.table_feeds.verticalHeader().setVisible(False)
    window.table_feeds.verticalHeader().setDefaultSectionSize(48)
    # Resize rows to fit their content (allows cells with widgets to grow taller).
    window.table_feeds.verticalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.ResizeToContents
    )
    window.table_feeds.setAlternatingRowColors(True)

    # Hide the RSS Endpoint URL column by default; revealed via toggle button.
    window.table_feeds.hideColumn(1)

    feed_l.addWidget(window.table_feeds, 1)

    # Add this tab to the main tab widget.
    window.tabs.addTab(tab_feed, "📡 Subscriptions Hub")
