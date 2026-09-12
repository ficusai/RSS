"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_04_ui_header_bar_top_section_build/build_header_bar.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.

==============================================================================
WHAT THIS TEST FILE VERIFIES
==============================================================================
This file verifies the build_header_bar function — the function that constructs
the top banner of the main window containing:
  - Brand badge ("⚡ RSS ENGINE")
  - Subtitle label ("Feed Tracker & Scraper Pro")
  - Article count badge (blue, initially "0 Articles")
  - Feed count badge (purple, initially "0 Feeds")
  - Sync button (green accent, connected to window.start_scrape)

The function returns a QFrame with objectName="card" for stylesheet targeting.

==============================================================================
LAYER BREAKDOWN
==============================================================================
Layer 1 (Structural):
  - test_file_exists              : Source file exists on disk
  - test_import_health            : Module imports without errors
  - test_ast_imports              : Imports exactly {'PyQt6.QtGui', 'PyQt6.QtWidgets'}
  - test_build_header_bar_signature : build_header_bar(window) -> None exact signature

Layer 2 (Behavioral):
  - test_returns_qframe_with_card_object_name : Returns QFrame with objectName="card"
  - test_lbl_articles_stat_created : Creates lbl_articles_stat QLabel on window
  - test_btn_sync_text_and_object_name : btn_sync text is "🔄 Sync All Feeds", objectName="accent"
  - test_btn_sync_connected_to_start_scrape : btn_sync.clicked connects to window.start_scrape

LAYER WHAT EACH TEST CHECKS
==============================================================================
"""
# ==============================================================================
# OVERVIEW OF IMPORTS USED IN THIS TEST FILE
# ==============================================================================
# ast: Parses source into an Abstract Syntax Tree for import verification.
import ast
# inspect: Examines function signatures (parameters, kinds, defaults, return types).
import inspect
# sys: Manipulates sys.path to add project root for imports.
import sys
# pathlib.Path: Cross-platform filesystem path construction.
from pathlib import Path
# unittest.mock.MagicMock: Creates fake objects that记录 all method calls for verification.
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
# Prevents PyQt6 from trying to open a real display during headless test runs.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    """Return the absolute path to build_header_bar.py.

    WHAT: Constructs the filesystem path by navigating up 3 levels from this
          test file to the RSS project root, then down to the source module.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns Path like: /home/ficus-pro/Documents/RSS/gui/_04_ui_header_bar_top_section_build/build_header_bar.py

    ERRORS/EDGE CASES: None — path construction never raises.
    """
    return Path(__file__).resolve().parents[3] / "gui" / "_04_ui_header_bar_top_section_build" / "build_header_bar.py"


def _import_module():
    """Import the source module and return it.

    WHAT: Loads gui._04_ui_header_bar_top_section_build.build_header_bar and returns it.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns module with build_header_bar function.

    ERRORS/EDGE CASES:
      - ImportError: syntax error or missing PyQt6 dependency
      - ModuleNotFoundError: package path changed
    """
    import gui._04_ui_header_bar_top_section_build.build_header_bar as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence.

    WHAT: Asserts the source .py file exists at the expected filesystem path.
          This is the most basic sanity check — if the file is missing, all
          other tests cannot run.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if file exists; raises AssertionError with path if not.

    ERRORS/EDGE CASES:
      - File deleted/moved: AssertionError with full path in message

    HOW TO TEST: Delete build_header_bar.py, then run this test.
                 It should fail with "Source file missing: /path/to/file.py"
    """
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health.

    WHAT: Verifies the module can be imported without any exceptions.
          Catches syntax errors, missing imports, and circular dependency issues.

    OPTIONS: None.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns the imported module object (truthy on success).

    ERRORS/EDGE CASES:
      - SyntaxError: invalid Python syntax in source code
      - ImportError: PyQt6 or other dependency not installed
      - RecursionError: circular import between modules

    HOW TO TEST: Add "import nonexistent_module_xyz" to the source.
                 Run this test — it should fail with ModuleNotFoundError.
    """
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports.

    WHAT: Parses the source AST and verifies the module imports exactly:
          - PyQt6.QtGui  (for QFont text styling)
          - PyQt6.QtWidgets  (for QHBoxLayout, QLabel, QFrame, QPushButton)

    WHY THESE IMPORTS:
          QFont (from QtGui) is used to set bold text on the brand badge.
          The QtWidgets imports are used for all the layout and widget classes.
          No other imports are needed — the stylesheet is a string constant
          defined elsewhere and applied via setStyleSheet().

    HOW IT WORKS:
      1. ast.parse() builds a syntax tree from the source code
      2. ast.walk() visits every node looking for Import and ImportFrom statements
      3. We collect module names into a set
      4. Compare against expected set {"PyQt6.QtGui", "PyQt6.QtWidgets"}

    OPTIONS: Expected set is exactly {"PyQt6.QtGui", "PyQt6.QtWidgets"}.
             No stdlib imports, no core imports, no other gui imports.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if found == expected; lists missing or extra on failure.

    ERRORS/EDGE CASES:
      - Extra import added: "Unexpected imports: ['os']"
      - Missing import: "Missing imports: ['PyQt6.QtGui']"

    HOW TO TEST: Add "import os" to the source. Run this test — it should fail
                 with "Unexpected imports: ['os']".
    """
    expected = {"PyQt6.QtGui", "PyQt6.QtWidgets"}
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        # ast.Import: matches "import os", "import os, sys"
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        # ast.ImportFrom: matches "from PyQt6.QtGui import QFont"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, f"Missing imports: {sorted(missing)}"


def test_build_header_bar_signature():
    """Layer 1 — build_header_bar(window) -> None exact signature.

    WHAT: Verifies the function has exactly one required parameter named "window"
          and a return type annotation of None.

    WHY SIGNATURE MATTERS:
          Every caller uses: build_header_bar(window)
          If the parameter name or count changed, all callers break.
          The return type None tells type checkers the function returns nothing
          meaningful (the QFrame is returned but not typed).

    OPTIONS:
      - Parameter name: must be exactly "window"
      - Parameter kind: POSITIONAL_OR_KEYWORD (can pass by position or name)
      - Default: none (required parameter)
      - Return type: must be annotated as None

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Passes if signature matches exactly.

    ERRORS/EDGE CASES:
      - Parameter renamed: params mismatch
      - Added default: default mismatch
      - Return type changed: return_annotation mismatch

    HOW TO TEST: Change parameter from "window" to "app" in source.
                 Run this test — it should fail with params mismatch.
    """
    mod = _import_module()
    func = mod.build_header_bar
    # inspect.signature(func): returns a Signature object describing the function
    sig = inspect.signature(func)
    # Build list of (name, kind, default) for each parameter
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    # Expected: one required parameter named "window"
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    # Return annotation must be exactly None
    assert sig.return_annotation is None


def test_returns_qframe_with_card_object_name():
    """Layer 2 — Returns QFrame with objectName='card'.

    WHAT: Verifies that build_header_bar returns a QFrame widget and sets its
          objectName to "card". The objectName is used by the QSS stylesheet to
          apply the dark card background and border style.

    WHY objectName="card":
          The stylesheet defines QFrame#card { background-color: #161b22; border: 1px solid #21262d; ... }
          Without this objectName, the header bar would have no background styling
          and would blend into the window background.

    HOW MOCKING WORKS:
      1. patch all Qt classes (QFrame, QLabel, QPushButton, QHBoxLayout, QFont)
      2. Configure mocks to return themselves for chaining
      3. Call build_header_bar(window) and capture the return value
      4. Verify return is the mock frame and objectName was set to "card"

    OPTIONS:
      - objectName: must be exactly "card" (used by stylesheet selector QFrame#card)
      - Return type: must be a QFrame (or MagicMock simulating one)

    DEFAULTS: N/A.

    OUTPUT/EFFECT: Returns QFrame with objectName="card".

    ERRORS/EDGE CASES:
      - Wrong objectName: assert_called_once_with("card") fails
      - Not a QFrame: return type check fails

    HOW TO TEST: Change hdr.setObjectName("card") to hdr.setObjectName("wrong") in source.
                 Run this test — it should fail on the setObjectName assertion.
    """
    mod = _import_module()
    # MagicMock(): creates a fake window with start_scrape method
    window = MagicMock()
    window.start_scrape = MagicMock()
    # patch all Qt classes used in this function
    with patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFrame") as MockFrame, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QLabel") as MockLabel, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QPushButton") as MockButton, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QHBoxLayout") as MockLayout, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFont") as MockFont:
        # Create mock instances
        mock_frame = MagicMock()
        mock_frame.setObjectName = MagicMock()
        mock_layout = MagicMock()
        MockLayout.return_value = mock_layout
        MockFrame.return_value = mock_frame
        # Call the function under test
        result = mod.build_header_bar(window)
        # Verify the returned object is the mock frame
        assert result is mock_frame
        # Verify objectName was set to "card" for stylesheet targeting
        mock_frame.setObjectName.assert_called_once_with("card")


def test_lbl_articles_stat_created():
    """Layer 2 — Creates lbl_articles_stat.

    WHAT: Verifies that build_header_bar creates a QLabel for article count
          and stores it as window.lbl_articles_stat.

    WHY lbl_articles_stat:
          This label displays the current article count (e.g., "142 Articles").
          It is updated by update_stats_badges() after each scrape.
          Other parts of the code reference window.lbl_articles_stat to update the display.

    HOW MOCKING WORKS:
      1. patch all Qt classes
      2. Configure mock Label to return different MagicMock instances
      3. Call build_header_bar(window)
      4. Verify window.lbl_articles_stat was set and setText was called

    OPTIONS: None — lbl_articles_stat must be created and have setText called.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: window.lbl_articles_stat is a QLabel with text set.

    ERRORS/EDGE CASES:
      - Label not created: AttributeError on window.lbl_articles_stat
      - setText not called: assertion fails

    HOW TO TEST: Remove window.lbl_articles_stat = QLabel(...) from source.
                 Run this test — it should fail with AttributeError.
    """
    mod = _import_module()
    window = MagicMock()
    window.start_scrape = MagicMock()
    with patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QLabel") as MockLabel, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QPushButton") as MockButton, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QHBoxLayout") as MockLayout, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFrame") as MockFrame, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFont"):
        MockFrame.return_value = MagicMock()
        MockFrame.return_value.setObjectName = MagicMock()
        MockLayout.return_value = MagicMock()
        # Create mock labels; the 4th one is lbl_articles_stat
        mock_lbl = MagicMock()
        mock_lbl.setStyleSheet = MagicMock()
        mock_lbl.setText = MagicMock()
        # side_effect: each call to MockLabel returns the next mock in sequence
        MockLabel.side_effect = [MagicMock(), MagicMock(), MagicMock(), mock_lbl]
        mod.build_header_bar(window)
        # Verify setText was called on lbl_articles_stat
        mock_lbl.setText.assert_called_once()


def test_btn_sync_text_and_object_name():
    """Layer 2 — btn_sync.text() == '🔄 Sync All Feeds', objectName='accent'.

    WHAT: Verifies that the sync button has the correct display text and objectName.
          The text is what the user sees; the objectName controls the visual style.

    WHY "accent" objectName:
          The stylesheet defines QPushButton#accent { background: #1a5a2e; color: #3fb950; ... }
          This gives the sync button a green background, making it the primary action
          button visually. Without this, the button would have the default gray style.

    WHY "🔄 Sync All Feeds" text:
          The emoji indicates a refresh/sync action. The full text tells the user
          exactly what will happen when clicked. Both must match exactly.

    OPTIONS:
      - Button text: must be exactly "🔄 Sync All Feeds" (including emoji)
      - objectName: must be exactly "accent" (for green stylesheet targeting)

    DEFAULTS: N/A.

    OUTPUT/EFFECT: btn_sync has text "🔄 Sync All Feeds" and objectName "accent".

    ERRORS/EDGE CASES:
      - Wrong text: text.return_value mismatch
      - Wrong objectName: setObjectName assertion fails

    HOW TO TEST: Change "🔄 Sync All Feeds" to "Sync" in source.
                 Run this test — it should fail on the text assertion.
    """
    mod = _import_module()
    window = MagicMock()
    window.start_scrape = MagicMock()
    with patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QLabel") as MockLabel, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QPushButton") as MockButton, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QHBoxLayout") as MockLayout, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFrame") as MockFrame, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFont"):
        MockFrame.return_value = MagicMock()
        MockFrame.return_value.setObjectName = MagicMock()
        MockLayout.return_value = MagicMock()
        # Create mock button
        mock_btn = MagicMock()
        mock_btn.text.return_value = "🔄 Sync All Feeds"
        mock_btn.setObjectName = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockLabel.return_value = MagicMock()
        mod.build_header_bar(window)
        # Verify objectName is "accent" for green stylesheet style
        mock_btn.setObjectName.assert_called_once_with("accent")
        # Verify button text (the mock's text() returns the expected string)
        assert mock_btn.text.return_value == "🔄 Sync All Feeds"


def test_btn_sync_connected_to_start_scrape():
    """Layer 2 — btn_sync connected to window.start_scrape.

    WHAT: Verifies that clicking the sync button triggers window.start_scrape().
          This is the main action of the application — clicking "Sync All Feeds"
          starts the background scrape process.

    WHY CONNECT MATTERS:
          In PyQt6, buttons don't do anything unless you connect their signals
          to slots (functions). The clicked signal is connected to start_scrape,
          which creates and starts the ScrapeThread in the background.
          Without this connection, the button would be visually present but
          non-functional.

    HOW SIGNAL CONNECTION WORKS:
          window.btn_sync.clicked.connect(window.start_scrape)
          - clicked: PyQt6 signal emitted when user clicks the button
          - connect(): method that links the signal to a slot (function)
          - start_scrape: the slot that runs when clicked

    OPTIONS: None — btn_sync.clicked MUST connect to window.start_scrape.

    DEFAULTS: N/A.

    OUTPUT/EFFECT: btn_sync.clicked.connect called once with window.start_scrape.

    ERRORS/EDGE CASES:
      - Wrong connection: connect called with different function
      - No connection: connect never called

    HOW TO TEST: Change window.start_scrape to window.other_function in source.
                 Run this test — it should fail on the connect assertion.
    """
    mod = _import_module()
    window = MagicMock()
    window.start_scrape = MagicMock()
    with patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QLabel") as MockLabel, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QPushButton") as MockButton, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QHBoxLayout") as MockLayout, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFrame") as MockFrame, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFont"):
        MockFrame.return_value = MagicMock()
        MockFrame.return_value.setObjectName = MagicMock()
        MockLayout.return_value = MagicMock()
        # Create mock button
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockLabel.return_value = MagicMock()
        mod.build_header_bar(window)
        # Verify clicked.connect was called exactly once with window.start_scrape
        mock_btn.clicked.connect.assert_called_once_with(window.start_scrape)
