"""Populate the presets category dropdown from the presets library."""
# WHAT: Loads preset categories and fills window.preset_combo_cat.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: Falls back to ["All Categories"] on any import error.
# OUTPUT/EFFECT: Preset category combo box repopulated.
# ERRORS/EDGE CASES: get_preset_categories may not exist in older branches.
# HOW TO TEST: load_preset_categories(window); assert window.preset_combo_cat.count() > 0
def load_preset_categories(window) -> None:
    """Load preset categories into the presets tab category dropdown."""
    try:
        from features.feature_feed_presets_library.implementation.feeds_presets import get_preset_categories
        cats = ["All Categories"] + get_preset_categories()
    except Exception:
        cats = ["All Categories"]

    cur = window.preset_combo_cat.currentText()
    window.preset_combo_cat.blockSignals(True)
    window.preset_combo_cat.clear()
    window.preset_combo_cat.addItems(cats)
    if cur in cats:
        window.preset_combo_cat.setCurrentText(cur)
    window.preset_combo_cat.blockSignals(False)
