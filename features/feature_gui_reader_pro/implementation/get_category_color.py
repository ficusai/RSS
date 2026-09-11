"""Single-function module for generating category badge hex colors."""

def get_category_color(category_name: str) -> str:
    """Returns hex color code badge for a category."""
    cat = (category_name or "").lower()
    if "tech" in cat:
        return "#58a6ff"
    elif "finan" in cat or "econ" in cat or "bank" in cat:
        return "#3fb950"
    elif "news" in cat or "world" in cat:
        return "#d29922"
    return "#a371f7"
