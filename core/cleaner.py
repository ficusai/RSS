"""
HTML cleaning and Date parsing utilities for RSS feed processing.
"""

# WHAT: Standard Python module for converting HTML code (like &lt; or &amp;) into normal readable text (like < or &).
# OPTIONS/VALUES: html.unescape() converts encoded HTML character entities.
# DEFAULTS: Built-in Python standard library module.
# OUTPUT/EFFECT: Provides the unescape function used by clean_html().
# ERRORS/EDGE CASES: None.
# HOW TO TEST: Run 'python3 -c "import html; print(html.unescape(&quot;&amp;amp;&quot;))"'.
import html

# WHAT: Regular Expressions module used for searching, matching, and replacing text patterns (like HTML tags or scripts).
# OPTIONS/VALUES: re.sub() for string replacement, re.DOTALL, re.IGNORECASE.
# DEFAULTS: Built-in Python standard library module.
# OUTPUT/EFFECT: Strips tags, scripts, and extra spaces from article descriptions.
# ERRORS/EDGE CASES: Invalid regex patterns throw re.error.
# HOW TO TEST: Run 'python3 -c "import re; print(re.sub(r&quot;&lt;[^&gt;]+&gt;&quot;, &quot;&quot;, &quot;&lt;b&gt;hello&lt;/b&gt;&quot;))"'.
import re

# WHAT: Datetime utilities for reading, formatting, and standardizing dates and timezones (UTC).
# OPTIONS/VALUES: datetime.now(timezone.utc), datetime.fromisoformat(), strftime().
# DEFAULTS: Uses Coordinated Universal Time (timezone.utc).
# OUTPUT/EFFECT: Produces standard ISO 8601 date strings like "2026-09-11T12:00:00Z".
# ERRORS/EDGE CASES: Invalid date formats throw ValueError.
# HOW TO TEST: Run 'python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc))"'.
from datetime import datetime, timezone

# WHAT: Utility function from Python's email library that parses web date strings (RFC-822 / RSS format).
# OPTIONS/VALUES: Takes input date string like "Thu, 10 Sep 2026 20:00:00 GMT".
# DEFAULTS: Returns a Python datetime object or None if format is unparseable.
# OUTPUT/EFFECT: Converts RSS pubDate header into a timezone-aware datetime object.
# ERRORS/EDGE CASES: Returns None for non-standard or malformed date strings.
# HOW TO TEST: Run 'python3 -c "from email.utils import parsedate_to_datetime; print(parsedate_to_datetime(&quot;Thu, 10 Sep 2026 20:00:00 GMT&quot;))"'.
from email.utils import parsedate_to_datetime


# WHAT: Cleaning function that converts raw RSS HTML markup into clean, readable plain text.
# OPTIONS/VALUES: Input 'html_str' can be any string containing raw HTML, formatted tags, or encoded text.
# DEFAULTS: Returns empty string "" if input is None, empty, or not a string.
# OUTPUT/EFFECT: Returns clean plain text string scrubbed of HTML tags, script code, and excessive whitespace.
# ERRORS/EDGE CASES: Non-string or empty inputs are caught immediately and return "".
# HOW TO TEST: Run 'python3 -c "from core.cleaner import clean_html; print(clean_html(&quot;<p>Hello &amp; World!</p>&quot;))"'.
def clean_html(html_str: str) -> str:
    """
    Strips HTML tags, unescapes HTML entities, and normalizes spacing.
    """
    # WHAT: Guard check to ensure input is a valid non-empty string.
    # OPTIONS/VALUES: html_str can be None, "", integer, or a string.
    # DEFAULTS: Returns "" if invalid.
    # OUTPUT/EFFECT: Prevents crash when processing missing or non-text article summaries.
    # ERRORS/EDGE CASES: Handles NoneType or non-string inputs safely.
    # HOW TO TEST: Pass None to clean_html(None).
    if not html_str or not isinstance(html_str, str):
        return ""

    # WHAT: Unescapes HTML entities, turning codes like '&amp;' into '&', '&lt;' into '<', and '&quot;' into quotes.
    # OPTIONS/VALUES: Converts all standard HTML 4 and HTML 5 character entity references.
    # DEFAULTS: Modifies text in place.
    # OUTPUT/EFFECT: Converts entity code characters into normal printable symbols.
    # ERRORS/EDGE CASES: None.
    # HOW TO TEST: Pass "Cats &amp; Dogs" to see "Cats & Dogs".
    text = html.unescape(html_str)

    # WHAT: Removes embedded JavaScript <script>...</script> and CSS <style>...</style> tag blocks completely.
    # OPTIONS/VALUES: Flags re.DOTALL allows matching across multiple lines; re.IGNORECASE ignores uppercase/lowercase tag names.
    # DEFAULTS: Replaces matching script/style code blocks with an empty string "".
    # OUTPUT/EFFECT: Removes raw code scripts from article text.
    # ERRORS/EDGE CASES: Handles unclosed script tags gracefully.
    # HOW TO TEST: Pass "<script>var x=10;</script>Article text" to verify script removal.
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # WHAT: Strips all remaining HTML tags (like <p>, <div>, <a>, <img>) from the text string.
    # OPTIONS/VALUES: Regex matching any characters inside angle brackets '<...>'.
    # DEFAULTS: Replaces each tag with a single space to avoid smushing words together.
    # OUTPUT/EFFECT: Leaves only human-readable article text.
    # ERRORS/EDGE CASES: Handles nested or unclosed brackets safely.
    # HOW TO TEST: Pass "<p>Hello</p><p>World</p>" to verify space separation.
    text = re.sub(r"<[^>]+>", " ", text)

    # WHAT: Replaces consecutive spaces, tabs, and newlines with a single space.
    # OPTIONS/VALUES: Regex '\s+' matches any sequence of whitespace characters.
    # DEFAULTS: Replaces with " ".
    # OUTPUT/EFFECT: Cleans up messy spacing resulting from tag removals.
    # ERRORS/EDGE CASES: None.
    # HOW TO TEST: Pass "Hello    World\n\nTest" to receive "Hello World Test".
    text = re.sub(r"\s+", " ", text)

    # WHAT: Strips leading and trailing spaces from the final text string and returns it.
    # OPTIONS/VALUES: Returns cleaned string.
    # DEFAULTS: None.
    # OUTPUT/EFFECT: Produces final polished article plain text.
    # ERRORS/EDGE CASES: Returns empty string if text consisted entirely of HTML tags or spaces.
    # HOW TO TEST: Pass "  Hello  " to receive "Hello".
    return text.strip()


# WHAT: Standardizes raw date strings into ISO 8601 UTC format (YYYY-MM-DDTHH:MM:SSZ).
# OPTIONS/VALUES: Accepts RSS RFC-822 strings, Atom ISO-8601 strings, or custom date strings.
# DEFAULTS: Returns current UTC time if parsing fails or input is empty.
# OUTPUT/EFFECT: Guarantees consistent date format for AI agent analysis and sorting.
# ERRORS/EDGE CASES: Malformed dates fall back to current UTC timestamp.
# HOW TO TEST: Run 'python3 -c "from core.cleaner import parse_to_iso; print(parse_to_iso(&quot;Thu, 10 Sep 2026 20:00:00 GMT&quot;))"'.
def parse_to_iso(date_str: str) -> str:
    """
    Parses RFC-822 (RSS) or ISO-8601 (Atom) date strings into clean ISO 8601 UTC string (YYYY-MM-DDTHH:MM:SSZ).
    Falls back to current UTC time if parsing fails.
    """
    # WHAT: Generates default fallback timestamp for the current moment in UTC.
    # OPTIONS/VALUES: ISO 8601 format string, e.g. "2026-09-11T12:00:00Z".
    # DEFAULTS: Generated using current system time in UTC.
    # OUTPUT/EFFECT: Provides a valid timestamp even if feed article lacks a pubDate tag.
    # ERRORS/EDGE CASES: None.
    # HOW TO TEST: Pass "" to parse_to_iso() to receive current time.
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # WHAT: Input check for missing or non-string date inputs.
    # OPTIONS/VALUES: Returns now_utc if input is None or not a string.
    # DEFAULTS: Returns now_utc.
    # OUTPUT/EFFECT: Protects date parser from crashing on missing date fields.
    # ERRORS/EDGE CASES: Handles None or integer inputs safely.
    # HOW TO TEST: Pass None to parse_to_iso(None).
    if not date_str or not isinstance(date_str, str):
        return now_utc

    # WHAT: Strips surrounding whitespace from input date string.
    # OPTIONS/VALUES: Cleaned string.
    # DEFAULTS: Modifies date_str.
    # OUTPUT/EFFECT: Prepares string for format parsing.
    # ERRORS/EDGE CASES: Empty string after strip returns now_utc.
    # HOW TO TEST: Pass "  " to verify fallback.
    date_str = date_str.strip()
    if not date_str:
        return now_utc

    # 1. Try RFC-822 (RSS format, e.g. Mon, 02 Jan 2006 15:04:05 GMT)
    try:
        # WHAT: Attempts parsing string using standard email/RSS RFC-822 date parser.
        # OPTIONS/VALUES: Parses date string into Python datetime object.
        # DEFAULTS: Returns datetime object or None if unparseable.
        # OUTPUT/EFFECT: Converts date string into datetime object.
        # ERRORS/EDGE CASES: Throws exception on invalid text, caught by try/except block.
        # HOW TO TEST: Pass "Thu, 10 Sep 2026 20:00:00 GMT".
        dt = parsedate_to_datetime(date_str)
        if dt is not None:
            # WHAT: Converts datetime to UTC timezone.
            # OPTIONS/VALUES: Converts timezone offsets to UTC.
            # DEFAULTS: Sets UTC timezone if timezone info is missing.
            # OUTPUT/EFFECT: Normalizes all times to UTC time.
            # ERRORS/EDGE CASES: None.
            # HOW TO TEST: Pass date with EST or +0200 timezone offset.
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc)
            else:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        pass

    # 2. Try ISO-8601 (Atom format, e.g. 2006-01-02T15:04:05Z or 2006-01-02T15:04:05+00:00)
    iso_candidate = date_str
    # WHAT: Replaces trailing 'Z' suffix with explicit '+00:00' UTC offset for Python's ISO parser.
    # OPTIONS/VALUES: Converts "2026-09-11T12:00:00Z" to "2026-09-11T12:00:00+00:00".
    # DEFAULTS: Modifies iso_candidate string.
    # OUTPUT/EFFECT: Ensures compatibility with datetime.fromisoformat().
    # ERRORS/EDGE CASES: None.
    # HOW TO TEST: Pass ISO string ending in 'Z'.
    if iso_candidate.endswith("Z"):
        iso_candidate = iso_candidate[:-1] + "+00:00"

    try:
        # WHAT: Parses ISO-8601 formatted date strings.
        # OPTIONS/VALUES: Parses strings like "2026-09-11T12:00:00+00:00".
        # DEFAULTS: Returns datetime object.
        # OUTPUT/EFFECT: Converts Atom feed dates into datetime object.
        # ERRORS/EDGE CASES: Throws ValueError if format does not match.
        # HOW TO TEST: Pass "2026-09-10T20:00:00Z".
        dt = datetime.fromisoformat(iso_candidate)
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        pass

    # 3. Fallback common date formats
    # WHAT: Loops through standard common date format strings if RFC-822 and ISO-8601 attempts fail.
    # OPTIONS/VALUES: Format options: "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d %b %Y %H:%M:%S".
    # DEFAULTS: Tries formats in order.
    # OUTPUT/EFFECT: Returns formatted ISO date if match is found.
    # ERRORS/EDGE CASES: If no formats match, loop finishes and code falls back to now_utc.
    # HOW TO TEST: Pass "2026-09-10 20:00:00".
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d %b %Y %H:%M:%S"):
        try:
            dt = datetime.strptime(date_str, fmt)
            dt = dt.replace(tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            continue

    # WHAT: Final fallback returning current UTC timestamp if all parsing methods failed.
    # OPTIONS/VALUES: Returns now_utc string.
    # DEFAULTS: Returns current timestamp.
    # OUTPUT/EFFECT: Prevents unhandled date errors.
    # ERRORS/EDGE CASES: Executed only for completely unrecognized date text.
    # HOW TO TEST: Pass unparseable string like "Invalid Date Text".
    return now_utc
