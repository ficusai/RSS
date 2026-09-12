"""Toggle visibility of the RSS Endpoint URL column in the subscriptions table."""
# WHAT: Shows or hides column 1 (RSS Endpoint URL) of window.table_feeds and
#       updates window.btn_toggle_url text to reflect current state.
# OPTIONS: window — MainWindow instance with table_feeds, btn_toggle_url, and
#          _url_visible attributes.
# DEFAULTS: N/A.
# OUTPUT/EFFECT: table_feeds.showColumn(1) or hideColumn(1); btn_toggle_url
#                text set to "🔗 Hide URL" or "🔗 URL"; _url_visible flipped.
# ERRORS/EDGE CASES: None expected.
# HOW TO TEST: toggle_url_column(window) should flip URL column visibility.

def toggle_url_column(window) -> None:
    """Toggle the RSS Endpoint URL column visibility."""
    visible = not window._url_visible
    window._url_visible = visible
    if visible:
        window.table_feeds.showColumn(1)
        window.btn_toggle_url.setText("🔗 Hide URL")
    else:
        window.table_feeds.hideColumn(1)
        window.btn_toggle_url.setText("🔗 URL")
