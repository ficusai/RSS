"""Toggle visibility of the 'New Feed / Presets' drawer."""
# WHAT: Shows/hides window.drawer_box and updates the toggle button text.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: drawer_box visibility inverted; btn_toggle_drawer text updated.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: toggle_add_drawer(window) should flip drawer visibility.


def toggle_add_drawer(window) -> None:
    """Toggle the collapsible feed-add drawer visibility."""
    visible = not window.drawer_box.isVisible()
    window.drawer_box.setVisible(visible)
    window.btn_toggle_drawer.setText("➖ Hide Drawer" if visible else "➕ New Feed / Presets ▾")
    # Sync URL column: show it when drawer is open, hide when closed.
    window._url_visible = visible
    if visible:
        window.table_feeds.showColumn(1)
        window.btn_toggle_url.setText("🔗 Hide URL")
    else:
        window.table_feeds.hideColumn(1)
        window.btn_toggle_url.setText("🔗 URL")
