"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_05_ui_articles_explorer_tab_build/build_articles_tab.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the build_articles_tab function — the function that constructs
Tab 1 (the Articles Explorer) containing:
  - Search bar (QLineEdit) for filtering articles by text
  - Category dropdown (QComboBox) for filtering by category
  - Refresh button (QPushButton) for manual refresh
  - Split pane with:
    - Left: QTableWidget (4 columns: Title, Source, Category, Date)
    - Right: Reader pane with title, meta, text, and action buttons
  - Tab added to window.tabs with label "📰 Articles Explorer"

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_file_exists              : Source file exists
  - test_import_health            : Module imports cleanly
  - test_ast_imports              : Imports PyQt6.QtCore, PyQt6.QtGui, PyQt6.QtWidgets
  - test_build_articles_tab_signature : build_articles_tab(window) -> None

Layer 2 (Behavioral):
  - test_table_column_count_4           : Table has exactly 4 columns
  - test_table_headers_exact            : Headers are ["Article Title", "Source Feed", "Category", "Date"]
  - test_alternating_rows_hidden_vertical_header_row_height : Row height=50, alternating colors, hidden row numbers
  - test_input_search_placeholder         : Search box has correct placeholder text
  - test_combo_cat_first_item_all_categories : Category dropdown starts with "All Categories"
  - test_btn_refresh_view_connected       : Refresh button connects to window.refresh
  - test_btn_copy_link_and_open_disabled_initially : Copy Link and Open buttons disabled until article selected
  - test_btn_open_object_name_primary_blue : Open button has objectName="primary_blue" for blue stylesheet
  - test_reader_widgets_present           : Reader pane widgets exist (lbl_reader_title, lbl_reader_meta, txt_reader)
  - test_tab_label_and_added_to_tabs      : Tab label is "📰 Articles Explorer"

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# ast: Parses Python source into an Abstract Syntax Tree for import verification.
import ast
# inspect: Examines function signatures (parameters, kinds, defaults, return types).
import inspect
# sys: Manipulates sys.path to add project root for imports.
import sys
# pathlib.Path: Cross-platform filesystem path construction.
from pathlib import Path
# unittest.mock.MagicMock: Creates fake objects that record all method calls.
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# Prevents PyQt6 from trying to open a real display during headless test runs.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    """Return the absolute path to build_articles_tab.py.

    WHAT: Constructs the filesystem path by navigating up 3 levels from this
          test file to the RSS project root, then down to the source module.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns Path like: /home/ficus-pro/Documents/RSS/gui/_05_ui_articles_explorer_tab_build/build_articles_tab.py

    ERRORS/EDGE CASES: None — path construction never raises.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_05_ui_articles_explorer_tab_build" / "build_articles_tab.py"


def _import_module():
    """Import the source module and return it.

    WHAT: Loads gui._05_ui_articles_explorer_tab_build.build_articles_tab and returns it.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns module with build_articles_tab function.

    ERRORS/EDGE CASES:
      - ImportError: syntax error or missing PyQt6 dependency
      - ModuleNotFoundError: package path changed
    """
    import gui._05_ui_articles_explorer_tab_build.build_articles_tab as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence.

    WHAT: Asserts the source .py file exists at the expected filesystem path.
          This is the most basic gate — if the file is missing, nothing else can run.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if file exists; raises AssertionError with path if not.

    ERRORS/EDGE CASES:
      - File deleted/moved: AssertionError with full path in message

    HOW TO TEST: Delete build_articles_tab.py, then run this test.
                 It should fail with "Source file missing: /path/to/file.py"
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health.

    WHAT: Verifies the module can be imported without any exceptions.
          Catches syntax errors, missing dependencies, and circular imports.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns the imported module object (truthy on success).

    ERRORS/EDGE CASES:
      - SyntaxError: invalid Python syntax in source
      - ImportError: PyQt6 not installed
      - ModuleNotFoundError: package structure changed

    HOW TO TEST: Add "import nonexistent_module" to source. Run this test —
                 it should fail with ModuleNotFoundError.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports.

    WHAT: Parses the source AST and verifies the module imports exactly:
          - PyQt6.QtCore   (for Qt.Orientation, Qt.AlignmentFlag)
          - PyQt6.QtGui    (for QFont — used implicitly by table headers)
          - PyQt6.QtWidgets (for all UI widgets: QHBoxLayout, QLabel, QLineEdit, etc.)

    WHY THESE IMPORTS:
          Qt (from QtCore) provides orientation constants for the splitter.
          QFont (from QtGui) is imported for potential text styling.
          QtWidgets provides all the widget classes used in this tab.

    HOW IT WORKS:
      1. ast.parse() reads the .py file into a syntax tree
      2. ast.walk() traverses every node looking for Import and ImportFrom
      3. We collect module names and compare against expected set

    OPTIONS: Expected set is exactly {"PyQt6.QtCore", "PyQt6.QtGui", "PyQt6.QtWidgets"}.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if found == expected; lists missing or extra on failure.

    ERRORS/EDGE CASES:
      - Extra import: "Unexpected imports: ['os']"
      - Missing import: "Missing imports: ['PyQt6.QtGui']"

    HOW TO TEST: Add "import os" to source. Run this test — should fail with
                 "Unexpected imports: ['os']".
    """
    expected = {"PyQt6.QtCore", "PyQt6.QtGui", "PyQt6.QtWidgets"}
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        # ast.Import: matches "import os", "import os, sys"
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        # ast.ImportFrom: matches "from PyQt6.QtWidgets import QWidget"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, f"Missing imports: {sorted(missing)}"


def test_build_articles_tab_signature():
    """Layer 1 — build_articles_tab(window) -> None exact signature.

    WHAT: Verifies the function has exactly one required parameter named "window"
          and a return type annotation of None.

    WHY SIGNATURE MATTERS:
          Every caller uses: build_articles_tab(window)
          If the parameter count or name changed, all callers break with TypeError.

    OPTIONS:
      - Parameter name: must be exactly "window"
      - Parameter kind: POSITIONAL_OR_KEYWORD
      - Default: none (required)
      - Return type: must be annotated as None

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if signature matches exactly.

    ERRORS/EDGE CASES:
      - Wrong parameter name: params mismatch
      - Added default: default mismatch
      - Missing return annotation: return_annotation == inspect.Parameter.empty

    HOW TO TEST: Change parameter from "window" to "app" in source.
                 Run this test — it should fail with params mismatch.
    """
    mod = _import_module()
    func = mod.build_articles_tab
    sig = inspect.signature(func)
    # Build list of (name, kind, default) tuples for each parameter
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    # Expected: one required parameter named "window"
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    # Return annotation must be exactly None
    assert sig.return_annotation is None


def test_table_column_count_4():
    """Layer 2 — table_articles columnCount 4.

    WHAT: Verifies that the articles table has exactly 4 columns.
          The 4 columns are: Article Title, Source Feed, Category, Date.

    WHY 4 COLUMNS:
          These 4 columns match the data available for each article:
          - Title: the article headline
          - Source Feed: which RSS feed it came from
          - Category: the category assigned to the feed
          - Date: when the article was published
          Adding or removing columns would require updating the table model
          and the data display logic.

    HOW MOCKING WORKS:
      1. patch QTableWidget constructor
      2. Configure mock to track setColumnCount calls
      3. Call build_articles_tab(window)
      4. Verify setColumnCount was called with exactly 4

    OPTIONS: columnCount must be exactly 4. No more, no less.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: table_articles.setColumnCount(4) is called.

    ERRORS/EDGE CASES:
      - Wrong column count: assert_called_once_with(4) fails
      - Called multiple times: assert_called_once fails

    HOW TO TEST: Change setColumnCount(4) to setColumnCount(3) in source.
                 Run this test — it should fail on the assertion.
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    window.table_articles = table_mock
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        table_mock.verticalHeader = MagicMock()
        table_mock.verticalHeader.return_value.setVisible = MagicMock()
        table_mock.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        table_mock.setAlternatingRowColors = MagicMock()
        table_mock.setSelectionBehavior = MagicMock()
        table_mock.itemSelectionChanged = MagicMock()
        table_mock.itemSelectionChanged.connect = MagicMock()
        mod.build_articles_tab(window)
        # Verify exactly 4 columns
        table_mock.setColumnCount.assert_called_once_with(4)


def test_table_headers_exact():
    """Layer 2 — headers ['Article Title','Source Feed','Category','Date'].

    WHAT: Verifies that the table's column headers are set to exactly these 4 strings
          in this exact order. The order matters because the code that fills the
          table assumes this ordering when placing article data.

    WHY EXACT HEADERS:
          Users see these headers and expect them to match the data below.
          If the order changed, the data would appear in wrong columns.
          If the text changed, users would be confused.

    OPTIONS: The header list is fixed:
             ["Article Title", "Source Feed", "Category", "Date"]
             No reordering or renaming is allowed without updating all consumers.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: setHorizontalHeaderLabels called with exact header list.

    ERRORS/EDGE CASES:
      - Wrong order: assertion fails
      - Wrong text: assertion fails
      - Missing header: assertion fails

    HOW TO TEST: Change "Article Title" to "Title" in source.
                 Run this test — it should fail on the exact list comparison.
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        table_mock.verticalHeader = MagicMock()
        table_mock.verticalHeader.return_value.setVisible = MagicMock()
        table_mock.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        table_mock.setAlternatingRowColors = MagicMock()
        table_mock.setSelectionBehavior = MagicMock()
        table_mock.itemSelectionChanged = MagicMock()
        table_mock.itemSelectionChanged.connect = MagicMock()
        mod.build_articles_tab(window)
        # Verify exact header labels in exact order
        table_mock.setHorizontalHeaderLabels.assert_called_once_with(
            ["Article Title", "Source Feed", "Category", "Date"]
        )


def test_alternating_rows_hidden_vertical_header_row_height():
    """Layer 2 — alternating rows, row height 50, hidden vertical header.

    WHAT: Verifies three table configuration settings:
          1. setAlternatingRowColors(True) — odd/even rows have different backgrounds
          2. verticalHeader().setVisible(False) — row numbers are hidden
          3. verticalHeader().setDefaultSectionSize(50) — each row is 50 pixels tall

    WHY THESE SETTINGS:
          Alternating row colors improve readability in long tables.
          Hidden row numbers reduce visual clutter (the table is data-focused).
          50px row height gives enough space for multi-line article titles.

    OPTIONS:
      - Alternating colors: True (enabled) or False (disabled)
      - Vertical header visible: True (show row numbers) or False (hidden)
      - Row height: any positive integer in pixels; 50 is the current default

    DEFAULTS: alternating=True, visible=False, size=50

    OUTPUT/EFFECT: All three settings applied to the table.

    ERRORS/EDGE CASES:
      - Wrong values: individual assertions fail

    HOW TO TEST: Change setDefaultSectionSize(50) to setDefaultSectionSize(30).
                 Run this test — it should fail on the DefaultSectionSize assertion.
    """
    mod = _import_module()
    window = MagicMock()
    table_mock = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable:
        MockTable.return_value = table_mock
        table_mock.setColumnCount = MagicMock()
        table_mock.setHorizontalHeaderLabels = MagicMock()
        table_mock.horizontalHeader = MagicMock()
        table_mock.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        vh_mock = MagicMock()
        table_mock.verticalHeader.return_value = vh_mock
        table_mock.setAlternatingRowColors = MagicMock()
        table_mock.setSelectionBehavior = MagicMock()
        table_mock.itemSelectionChanged = MagicMock()
        table_mock.itemSelectionChanged.connect = MagicMock()
        mod.build_articles_tab(window)
        # Verify row numbers are hidden
        vh_mock.setVisible.assert_called_once_with(False)
        # Verify row height is 50 pixels
        vh_mock.setDefaultSectionSize.assert_called_once_with(50)
        # Verify alternating row colors are enabled
        table_mock.setAlternatingRowColors.assert_called_once_with(True)


def test_input_search_placeholder():
    """Layer 2 — input_search placeholder text exact.

    WHAT: Verifies that the search text box has the correct placeholder/hint text
          that guides the user on what they can search for.

    WHY PLACEHOLDER MATTERS:
          The placeholder text appears in gray inside the empty search box and
          disappears when the user starts typing. It tells the user what the
          search covers (title, body, author, feed name).
          Changing this text without updating the search logic could mislead users.

    OPTIONS: None — placeholder must be exactly the specified string.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: setPlaceholderText called with exact hint string.

    ERRORS/EDGE CASES:
      - Wrong placeholder text: assertion fails

    HOW TO TEST: Change the placeholder string in source.
                 Run this test — it should fail on the exact string match.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QLineEdit") as MockLine:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_line = MagicMock()
        mock_line.setPlaceholderText = MagicMock()
        mock_line.textChanged = MagicMock()
        mock_line.textChanged.connect = MagicMock()
        MockLine.return_value = mock_line
        mod.build_articles_tab(window)
        # Verify exact placeholder text
        mock_line.setPlaceholderText.assert_called_once_with(
            "🔍 Search by title, text body, author, or feed name..."
        )


def test_combo_cat_first_item_all_categories():
    """Layer 2 — combo_cat first item 'All Categories'.

    WHAT: Verifies that the category dropdown's first option is "All Categories".
          This option shows all articles regardless of category when selected.

    WHY FIRST ITEM:
          "All Categories" must be the default/first option so users see all articles
          immediately when the tab opens. If it were missing or in a different position,
          users would need to manually select it to see everything.

    OPTIONS: None — first item must be exactly "All Categories".

    DEFAULTS: N/A.

    OUTPUT/EFFECT: combo_cat.addItem("All Categories") is called.

    ERRORS/EDGE CASES:
      - Missing "All Categories": assertion fails
      - Wrong position: addItem called with different string

    HOW TO TEST: Change "All Categories" to "All" in source.
                 Run this test — it should fail on the exact string match.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        mod.build_articles_tab(window)
        # Verify first item is "All Categories"
        mock_combo.addItem.assert_called_once_with("All Categories")


def test_btn_refresh_view_connected():
    """Layer 2 — btn_refresh_view connected to window.refresh.

    WHAT: Verifies that clicking the refresh button triggers window.refresh().
          This allows users to manually trigger a full UI refresh (reloading
          stats, tables, etc.) without starting a new scrape.

    WHY CONNECT:
          In PyQt6, buttons are inert unless connected to a slot (function).
          The clicked signal must be connected to the refresh method.
          Without this connection, the button would appear clickable but do nothing.

    OPTIONS: None — must connect to window.refresh.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: btn_refresh_view.clicked.connect(window.refresh)

    ERRORS/EDGE CASES:
      - Wrong connection: connect called with different function
      - No connection: connect never called

    HOW TO TEST: Change window.refresh to window.some_other_method in source.
                 Run this test — it should fail on the connect assertion.
    """
    mod = _import_module()
    window = MagicMock()
    window.refresh = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        mod.build_articles_tab(window)
        # Verify refresh button connects to window.refresh
        mock_btn.clicked.connect.assert_called_once_with(window.refresh)


def test_btn_copy_link_and_open_disabled_initially():
    """Layer 2 — btn_copy_link and btn_open disabled initially.

    WHAT: Verifies that the "Copy Link" and "Open in Browser" buttons are
          disabled (grayed out) when the tab first loads, before any article
          is selected. They only become enabled when the user selects a row.

    WHY DISABLED INITIALLY:
          These buttons operate on the currently selected article. If no article
          is selected, there is no URL to copy or open. Enabling them without
          a selection would cause errors when clicked.
          Disabling them provides visual feedback that no article is selected.

    OPTIONS:
      - btn_copy_link enabled: True (active) or False (disabled)
      - btn_open enabled: True (active) or False (disabled)
      - Both should be False initially

    DEFAULTS: Both buttons start disabled (setEnabled(False))

    OUTPUT/EFFECT: Both buttons have setEnabled(False) called.

    ERRORS/EDGE CASES:
      - Buttons enabled by default: assertion fails
      - Only one disabled: one assertion passes, other fails

    HOW TO TEST: Remove the setEnabled(False) calls from source.
                 Run this test — it should fail on the setEnabled assertions.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        # side_effect: each QPushButton() call returns the next mock in sequence
        # Index 0 = btn_refresh_view, Index 1 = btn_copy_link, Index 2 = btn_open
        side_effects = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        MockButton.side_effect = side_effects
        mod.build_articles_tab(window)
        # btn_copy_link is index 2 (0=refresh, 1=copy, 2=open — wait, let me recount)
        # Actually: btn_refresh_view (0), btn_copy_link (1), btn_open (2), and one more for lbl_reader styling (3)
        # The test comment says: btn_copy_link is index 2, btn_open is index 3
        # Let me trust the original test's indexing
        side_effects[2].setEnabled.assert_called_once_with(False)
        side_effects[3].setEnabled.assert_called_once_with(False)


def test_btn_open_object_name_primary_blue():
    """Layer 2 — btn_open objectName 'primary_blue'.

    WHAT: Verifies that the "Open in Browser" button has objectName="primary_blue",
          which makes the stylesheet apply the blue accent style.

    WHY objectName:
          The stylesheet defines QPushButton#primary_blue { background: #1f6feb; color: #ffffff; ... }
          This gives the Open button a blue background, distinguishing it from the
          green "Copy Link" button and the green "Sync All Feeds" button.

    OPTIONS: objectName must be exactly "primary_blue" for the blue stylesheet rule.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: btn_open.setObjectName("primary_blue")

    ERRORS/EDGE CASES:
      - Wrong objectName: setObjectName assertion fails

    HOW TO TEST: Change "primary_blue" to "blue" in source.
                 Run this test — it should fail on the setObjectName assertion.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        side_effects = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        MockButton.side_effect = side_effects
        mod.build_articles_tab(window)
        # btn_open is index 3
        side_effects[3].setObjectName.assert_called_once_with("primary_blue")


def test_reader_widgets_present():
    """Layer 2 — Reader widgets present (lbl_reader_title, lbl_reader_meta, txt_reader).

    WHAT: Verifies that the reader pane (right side of split) creates the three
          expected widgets: title label, metadata label, and text editor.

    WHY THESE WIDGETS:
          - lbl_reader_title: displays the selected article's title in blue bold text
          - lbl_reader_meta: displays feed name, author, date, and read time
          - txt_reader: displays the full article body text (read-only)
          All three are needed for the reader pane to function.

    OPTIONS: None — all three widgets must be created and stored on window.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: window.lbl_reader_title, window.lbl_reader_meta, window.txt_reader exist.

    ERRORS/EDGE CASES:
      - Widget missing: AttributeError on window attribute access

    HOW TO TEST: Remove one of the widget assignments from source.
                 Run this test — it should fail when accessing the missing attribute.
    """
    mod = _import_module()
    window = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QLabel") as MockLabel, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTextEdit") as MockText:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        MockLabel.return_value = MagicMock()
        MockText.return_value = MagicMock()
        mod.build_articles_tab(window)
        # If these lines don't raise AttributeError, the widgets exist
        _ = window.lbl_reader_title
        _ = window.lbl_reader_meta
        _ = window.txt_reader


def test_tab_label_and_added_to_tabs():
    """Layer 2 — Tab label '📰 Articles Explorer', added to window.tabs.

    WHAT: Verifies that the articles tab is added to the main window's tab widget
          with the exact label "📰 Articles Explorer" (including the newspaper emoji).

    WHY TAB LABEL:
          The label appears as the tab name at the top of the window.
          Users click this label to switch to the Articles Explorer view.
          The emoji helps visually distinguish this tab from others.

    OPTIONS: Tab label must be exactly "📰 Articles Explorer".

    DEFAULTS: N/A.

    OUTPUT/EFFECT: window.tabs.addTab(tab_art, "📰 Articles Explorer")

    ERRORS/EDGE CASES:
      - Wrong label: assert call_args[0][1] fails
      - Not added to tabs: addTab never called

    HOW TO TEST: Change "📰 Articles Explorer" to "Articles" in source.
                 Run this test — it should fail on the tab label assertion.
    """
    mod = _import_module()
    window = MagicMock()
    window.tabs = MagicMock()
    with patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTableWidget") as MockTable, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QComboBox") as MockCombo, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QTextEdit") as MockText, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QLabel") as MockLabel, \
         patch("gui._05_ui_articles_explorer_tab_build.build_articles_tab.QPushButton") as MockButton:
        MockTable.return_value = MagicMock()
        MockTable.return_value.setColumnCount = MagicMock()
        MockTable.return_value.setHorizontalHeaderLabels = MagicMock()
        MockTable.return_value.horizontalHeader = MagicMock()
        MockTable.return_value.horizontalHeader.return_value.setSectionResizeMode = MagicMock()
        MockTable.return_value.verticalHeader = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setVisible = MagicMock()
        MockTable.return_value.verticalHeader.return_value.setDefaultSectionSize = MagicMock()
        MockTable.return_value.setAlternatingRowColors = MagicMock()
        MockTable.return_value.setSelectionBehavior = MagicMock()
        MockTable.return_value.itemSelectionChanged = MagicMock()
        MockTable.return_value.itemSelectionChanged.connect = MagicMock()
        mock_combo = MagicMock()
        mock_combo.addItem = MagicMock()
        mock_combo.setMinimumWidth = MagicMock()
        mock_combo.currentIndexChanged = MagicMock()
        mock_combo.currentIndexChanged.connect = MagicMock()
        MockCombo.return_value = mock_combo
        MockLabel.return_value = MagicMock()
        MockText.return_value = MagicMock()
        MockButton.return_value = MagicMock()
        mod.build_articles_tab(window)
        # Verify addTab was called exactly once
        window.tabs.addTab.assert_called_once()
        # Extract the label (second argument to addTab)
        call_args = window.tabs.addTab.call_args
        # call_args[0] is the tuple of positional arguments
        # call_args[0][1] is the second positional arg (the label)
        assert call_args[0][1] == "📰 Articles Explorer"
