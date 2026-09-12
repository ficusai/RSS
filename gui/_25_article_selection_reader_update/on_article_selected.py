"""Display the selected article's details in the reader pane."""
# WHAT: Reads window.current_articles[row_idx] and populates lbl_reader_title,
#       lbl_reader_meta, txt_reader, and enables/disables btn_open and btn_copy_link.
# OPTIONS: window — MainWindow instance.
# DEFAULTS: Returns early if no selection or row out of bounds.
# OUTPUT/EFFECT: Reader pane populated with article content.
# ERRORS/EDGE CASES: None.
# HOW TO TEST: on_article_selected(window) after selecting a row in table_articles
from features.feature_gui_reader_pro.implementation.reader_pro_components import calculate_reading_time_minutes


def on_article_selected(window) -> None:
    """Update the reader pane for the currently selected article."""
    rows = window.table_articles.selectedIndexes()
    if not rows:
        return
    row_idx = rows[0].row()
    if row_idx >= len(window.current_articles):
        return
    a = window.current_articles[row_idx]

    window.lbl_reader_title.setText(a.get("title", "Untitled"))
    meta = []
    if a.get("feed_name"):
        meta.append(f"📡 {a['feed_name']}")
    if a.get("author"):
        meta.append(f"👤 {a['author']}")
    if a.get("published_at_iso"):
        meta.append(f"📅 {a['published_at_iso'][:10]}")

    preview_text = a.get("preview") or ""
    full_text = a.get("full_text_clean") or a.get("text_clean") or a.get("summary_raw") or "No article content available."

    if preview_text and preview_text != full_text and len(full_text) > len(preview_text) + 50:
        body = f"📌 PREVIEW SUMMARY:\n{preview_text}\n\n{'=' * 45}\n📖 FULL ARTICLE CONTENT:\n{full_text}"
    else:
        body = full_text

    read_time = calculate_reading_time_minutes(body)
    meta.append(f"⏱️ ~{read_time} min read")

    window.lbl_reader_meta.setText("   •   ".join(meta))
    window.txt_reader.setPlainText(body)

    url = a.get("url")
    window.btn_open.setEnabled(bool(url))
    window.btn_copy_link.setEnabled(bool(url))
    if url:
        window.btn_open.setProperty("url", url)
        window.btn_copy_link.setProperty("url", url)
