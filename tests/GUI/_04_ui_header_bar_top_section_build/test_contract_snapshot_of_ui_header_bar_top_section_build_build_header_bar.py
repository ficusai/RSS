"""
CONTRACT SNAPSHOT — do not edit by hand.

Source: gui/_04_ui_header_bar_top_section_build/build_header_bar.py
Generated against branch: feature/gui-contract-tests

If this test fails, the source module has drifted from its contract.
Do NOT patch this test. Instead:
  1. Inspect the source change.
  2. If intentional, regenerate this test file.
  3. If unintentional, revert the source change.
"""
# WHAT: / OPTIONS: / DEFAULTS: / OUTPUT/EFFECT: / ERRORS/EDGE CASES: / HOW TO TEST:
import ast
import inspect
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# NOTE: conftest.py sets QT_QPA_PLATFORM=offscreen before this import.
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


def _module_path():
    return Path(__file__).resolve().parents[3] / "gui" / "_04_ui_header_bar_top_section_build" / "build_header_bar.py"


def _import_module():
    import gui._04_ui_header_bar_top_section_build.build_header_bar as mod
    return mod


def test_file_exists():
    """Layer 1 — file existence."""
    p = _module_path()
    assert p.exists(), f"Source file missing: {p}"


def test_import_health():
    """Layer 1 — import health."""
    mod = _import_module()
    assert mod is not None


def test_ast_imports():
    """Layer 1 — AST-verified imports."""
    expected = {"PyQt6.QtGui", "PyQt6.QtWidgets"}
    tree = ast.parse(_module_path().read_text())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    missing = expected - found
    assert not missing, f"Missing imports: {sorted(missing)}"


def test_build_header_bar_signature():
    """Layer 1 — build_header_bar(window) -> None."""
    mod = _import_module()
    func = mod.build_header_bar
    sig = inspect.signature(func)
    params = [(p.name, p.kind, p.default) for p in sig.parameters.values()]
    expected = [("window", inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.empty)]
    assert params == expected
    assert sig.return_annotation is None


def test_returns_qframe_with_card_object_name():
    """Layer 2 — Returns QFrame with objectName='card'."""
    mod = _import_module()
    window = MagicMock()
    window.start_scrape = MagicMock()
    with patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFrame") as MockFrame, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QLabel") as MockLabel, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QPushButton") as MockButton, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QHBoxLayout") as MockLayout, \
         patch("gui._04_ui_header_bar_top_section_build.build_header_bar.QFont") as MockFont:
        mock_frame = MagicMock()
        mock_frame.setObjectName = MagicMock()
        mock_layout = MagicMock()
        MockLayout.return_value = mock_layout
        MockFrame.return_value = mock_frame
        result = mod.build_header_bar(window)
        assert result is mock_frame
        mock_frame.setObjectName.assert_called_once_with("card")


def test_lbl_articles_stat_created():
    """Layer 2 — Creates lbl_articles_stat."""
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
        # First two QLabel calls are for lbl_articles_stat and lbl_feeds_stat
        mock_lbl = MagicMock()
        mock_lbl.setStyleSheet = MagicMock()
        mock_lbl.setText = MagicMock()
        MockLabel.side_effect = [MagicMock(), MagicMock(), MagicMock(), mock_lbl]
        mod.build_header_bar(window)
        mock_lbl.setText.assert_called_once()


def test_btn_sync_text_and_object_name():
    """Layer 2 — btn_sync.text() == '🔄 Sync All Feeds', objectName='accent'."""
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
        mock_btn = MagicMock()
        mock_btn.text.return_value = "🔄 Sync All Feeds"
        mock_btn.setObjectName = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockLabel.return_value = MagicMock()
        mod.build_header_bar(window)
        mock_btn.setObjectName.assert_called_once_with("accent")
        mock_btn.clicked.connect.assert_called_once_with(window.start_scrape)


def test_btn_sync_connected_to_start_scrape():
    """Layer 2 — btn_sync connected to window.start_scrape."""
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
        mock_btn = MagicMock()
        mock_btn.clicked = MagicMock()
        mock_btn.clicked.connect = MagicMock()
        MockButton.return_value = mock_btn
        MockLabel.return_value = MagicMock()
        mod.build_header_bar(window)
        mock_btn.clicked.connect.assert_called_once_with(window.start_scrape)
