"""Quick-import a preset feed: fill the drawer form and add it."""
# WHAT: Sets window.in_name, window.in_url, window.in_cat to the preset values,
#       then calls window.add_feed().
# OPTIONS: window — MainWindow instance; name, url, category — preset fields.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: Drawer form populated and feed added.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: import_preset(window, "TechCrunch", "https://...", "Technology")
def import_preset(window, name: str, url: str, category: str) -> None:
    """Fill the add-feed form with preset values and add it."""
    window.in_name.setText(name)
    window.in_url.setText(url)
    window.in_cat.setText(category)
    window.add_feed()
