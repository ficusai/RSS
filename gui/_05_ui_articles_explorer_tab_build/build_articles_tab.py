"""Build the Articles Explorer tab (Tab 1)."""
# ==============================================================================
# OVERVIEW
# Tab 1 is the "Articles Explorer" — the main content view where users read
# downloaded RSS articles. It has a split-pane design:
#   - LEFT SIDE: A search/filter bar + an article table (shows title, source, category, date)
#   - RIGHT SIDE: A reader pane (shows full article text when selected)
# The user clicks a row in the table to see the article in the reader.
#
# WHAT: Creates the articles tab with search bar, category filter, refresh button,
#       split-pane table+reader, and adds it as the first tab to window.tabs.
#
# OPTIONS: window — MainWindow instance. Stores the following widget references:
#            - window.input_search: QLineEdit for text search
#            - window.combo_cat: QComboBox for category filter
#            - window.btn_refresh_view: QPushButton to refresh the view
#            - window.table_articles: QTableWidget showing articles
#            - window.lbl_reader_title: QLabel for article title
#            - window.lbl_reader_meta: QLabel for metadata (feed, author, date, read time)
#            - window.txt_reader: QTextEdit for article body text
#            - window.btn_copy_link: QPushButton to copy article URL
#            - window.btn_open: QPushButton to open URL in browser
#
# DEFAULTS: N/A.
#
# OUTPUT/EFFECT: Creates tab_art widget and adds it to window.tabs as "📰 Articles Explorer".
#
# ERRORS/EDGE CASES: None expected. All widget creation is safe.
#
# HOW TO TEST: build_articles_tab(window); assert window.tabs.count() >= 1
#              Running the app and clicking Tab 1 should show the articles explorer.
# ==============================================================================
# PyQt6.QtCore.Qt: contains orientation constants.
#   Qt.Orientation.Horizontal: used to make the splitter divide left-to-right
#                              (table on left, reader on right).
from PyQt6.QtCore import Qt
# QFont: for text styling (used implicitly by table headers).
from PyQt6.QtGui import QFont
# Various Qt widgets used in this tab:
from PyQt6.QtWidgets import (
    QHBoxLayout,      # horizontal layout (filter bar, button row)
    QLabel,           # labels for titles and metadata
    QLineEdit,        # text input box for search
    QComboBox,        # dropdown menu for category filter
    QPushButton,      # clickable buttons
    QSplitter,        # resizable divider between table and reader
    QTableWidget,     # spreadsheet-like table for articles
    QHeaderView,      # controls table column headers (resize modes)
    QFrame,           # container with border styling (reader pane)
    QTextEdit,        # multi-line text display (article content, read-only)
    QVBoxLayout,      # vertical layout (stacks widgets top-to-bottom)
    QWidget,          # base widget class
    QSizePolicy,      # size policy for expanding widgets
)


def build_articles_tab(window) -> None:
    """Build and add the Articles Explorer tab.

    WHAT: Creates Tab 1 — a split-pane view with an article table on the left
          and an article reader on the right. Includes search, category filter,
          and refresh controls at the top.

    OPTIONS:
      window: MainWindow instance. This function creates and stores the following
              widget attributes on window for later use by other methods:
                - window.input_search: search text box
                - window.combo_cat: category dropdown
                - window.btn_refresh_view: refresh button
                - window.table_articles: article table widget
                - window.lbl_reader_title: article title label
                - window.lbl_reader_meta: metadata label (feed, author, date, read time)
                - window.txt_reader: read-only text area for article body
                - window.btn_copy_link: copy URL button (disabled until article selected)
                - window.btn_open: open in browser button (disabled until article selected)

    DEFAULTS: None.

    OUTPUT/EFFECT:
      - Creates a QWidget (tab_art) containing:
        1. A horizontal filter bar with search, category dropdown, refresh button
        2. A QSplitter with two panels:
           - Left: QTableWidget with 4 columns (Title, Source, Category, Date)
           - Right: QFrame reader with title, meta, text, and action buttons
      - Adds tab_art to window.tabs with label "📰 Articles Explorer"

    ERRORS/EDGE CASES: None expected.

    HOW TO TEST:
      1. Call build_articles_tab(window)
      2. Verify window.tabs.count() >= 1
      3. Verify window.input_search exists and has placeholder text
      4. Verify window.table_articles has 4 columns
    """
    # QWidget(): creates the empty container for this tab's content.
    # Every tab in a QTabWidget is just a QWidget that gets added to the tab.
    tab_art = QWidget()

    # QVBoxLayout(tab_art): creates a vertical layout to stack widgets top-to-bottom.
    # setContentsMargins(10, 10, 10, 10): adds 10px padding on all sides.
    # setSpacing(10): adds 10px gap between each widget in the layout.
    art_l = QVBoxLayout(tab_art)
    art_l.setContentsMargins(10, 10, 10, 10)
    art_l.setSpacing(10)

    # --- Filter Bar (search + category + refresh) ---
    # QHBoxLayout(): lays out the filter controls left-to-right.
    art_filter = QHBoxLayout()
    art_filter.setSpacing(10)  # 10px between each control

    # QLineEdit(): creates a single-line text input box.
    # setPlaceholderText(): shows gray hint text that disappears when user types.
    window.input_search = QLineEdit()
    window.input_search.setPlaceholderText("🔍 Search by title, text body, author, or feed name...")

    # textChanged.connect(): every time the user types or deletes a character,
    # this signals refresh_articles() to re-query and re-display matching articles.
    # The signal passes the new text string, but refresh_articles() is a 0-arg slot
    # so PyQt6 drops the argument (no error — see signal wiring notes in blueprint).
    window.input_search.textChanged.connect(window.refresh_articles)

    # QComboBox(): creates a dropdown menu.
    # addItem("All Categories"): adds the first option — shows all articles regardless of category.
    window.combo_cat = QComboBox()
    window.combo_cat.addItem("All Categories")
    # setMinimumWidth(220): ensures the dropdown is wide enough to show category names.
    window.combo_cat.setMinimumWidth(220)
    # currentIndexChanged.connect(): when user picks a category, refresh articles.
    window.combo_cat.currentIndexChanged.connect(window.refresh_articles)

    # QPushButton("🔄 Refresh View"): manually trigger a full refresh.
    window.btn_refresh_view = QPushButton("🔄 Refresh View")
    window.btn_refresh_view.clicked.connect(window.refresh)

    # Add widgets to the filter layout.
    # The '1' stretch factor on input_search makes it grow to fill available space.
    art_filter.addWidget(window.input_search, 1)
    art_filter.addWidget(window.combo_cat)
    art_filter.addWidget(window.btn_refresh_view)
    art_l.addLayout(art_filter)

    # --- Split Pane (table | reader) ---
    # QSplitter(Qt.Orientation.Horizontal): creates a resizable divider.
    # The user can drag the divider left/right to resize the two panels.
    splitter = QSplitter(Qt.Orientation.Horizontal)

    # --- Articles Table ---
    # QTableWidget(): creates a spreadsheet-style table.
    window.table_articles = QTableWidget()

    # setColumnCount(4): the table has exactly 4 columns.
    window.table_articles.setColumnCount(4)

    # setHorizontalHeaderLabels(): sets the column header text.
    # Order matters: index 0 = first column, index 3 = last column.
    window.table_articles.setHorizontalHeaderLabels(["Article Title", "Source Feed", "Category", "Date"])

    # setSectionResizeMode(): controls how each column resizes when the window resizes.
    # QHeaderView.ResizeMode.Stretch: column fills remaining width (used for Title).
    window.table_articles.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    # QHeaderView.ResizeMode.ResizeToContents: column auto-sizes to fit its content.
    window.table_articles.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    window.table_articles.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    window.table_articles.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

    # verticalHeader().setVisible(False): hides the row number column on the left.
    window.table_articles.verticalHeader().setVisible(False)
    # setDefaultSectionSize(50): each row is 50 pixels tall.
    window.table_articles.verticalHeader().setDefaultSectionSize(50)

    # setAlternatingRowColors(True): odd/even rows get different backgrounds
    # (defined in STYLESHEET as #0d1117 and #121720) for readability.
    window.table_articles.setAlternatingRowColors(True)

    # setSelectionBehavior(SelectRows): clicking any cell selects the entire row.
    window.table_articles.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

    # itemSelectionChanged.connect(): when user clicks a row, update the reader pane.
    window.table_articles.itemSelectionChanged.connect(window.on_article_sel)

    # --- Reader Pane (right side of splitter) ---
    # QFrame(): creates a bordered container for the reader.
    # setObjectName("card"): applies the dark card style from STYLESHEET.
    reader_box = QFrame()
    reader_box.setObjectName("card")

    # QVBoxLayout(reader_box): stack reader elements top-to-bottom.
    reader_l = QVBoxLayout(reader_box)
    reader_l.setContentsMargins(14, 14, 14, 14)
    reader_l.setSpacing(10)

    # QLabel("Select an article to view details"): initial placeholder text.
    # setWordWrap(True): long titles wrap to multiple lines instead of overflowing.
    window.lbl_reader_title = QLabel("Select an article to view details")
    window.lbl_reader_title.setWordWrap(True)
    # Blue bold text makes the title stand out.
    window.lbl_reader_title.setStyleSheet("color: #58a6ff; font-size: 18px; font-weight: bold;")

    # QLabel(""): empty metadata label. Filled when an article is selected.
    # Shows: feed name • author • date • estimated read time
    window.lbl_reader_meta = QLabel("")
    window.lbl_reader_meta.setStyleSheet("color: #8b949e; font-size: 15px; font-weight: 500;")

    # QTextEdit(): multi-line text editor for displaying article content.
    # setReadOnly(True): user can select/copy text but cannot edit it.
    window.txt_reader = QTextEdit()
    window.txt_reader.setReadOnly(True)

    # --- Reader Action Buttons ---
    # QHBoxLayout(): lay out buttons left-to-right.
    reader_btn_box = QHBoxLayout()
    reader_btn_box.setSpacing(10)

    # QPushButton("📋 Copy Link"): copy article URL to clipboard.
    # setEnabled(False): disabled until an article is selected.
    window.btn_copy_link = QPushButton("📋 Copy Link")
    window.btn_copy_link.setEnabled(False)
    window.btn_copy_link.clicked.connect(window.copy_article_link)

    # QPushButton("🌐 Open in Browser"): open article URL in system browser.
    # setObjectName("primary_blue"): applies blue accent style from STYLESHEET.
    window.btn_open = QPushButton("🌐 Open in Browser")
    window.btn_open.setObjectName("primary_blue")
    window.btn_open.setEnabled(False)  # disabled until article selected
    window.btn_open.clicked.connect(window.open_browser)

    # Add buttons to the button row.
    # addStretch() pushes the Open button to the far right.
    reader_btn_box.addWidget(window.btn_copy_link)
    reader_btn_box.addStretch()
    reader_btn_box.addWidget(window.btn_open)

    # Stack reader elements vertically.
    reader_l.addWidget(window.lbl_reader_title)
    reader_l.addWidget(window.lbl_reader_meta)
    # The '1' stretch factor makes the text editor grow to fill remaining space.
    reader_l.addWidget(window.txt_reader, 1)
    reader_l.addLayout(reader_btn_box)

    # --- Assemble Splitter ---
    # Add table (left) and reader (right) to the splitter.
    splitter.addWidget(window.table_articles)
    splitter.addWidget(reader_box)
    # setSizes([720, 480]): initial pixel widths — table is wider than reader.
    # User can drag the divider to resize.
    splitter.setSizes([720, 480])

    # Add the splitter to the tab layout. The '1' stretch makes it fill remaining space.
    art_l.addWidget(splitter, 1)

    # Add this tab to the main window's tab widget.
    # "📰 Articles Explorer" is the tab label shown to the user.
    tab_art.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    window.tabs.addTab(tab_art, "📰 Articles Explorer")
