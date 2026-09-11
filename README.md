# RSS Feed Scraper & Tracker Pro

A high-performance RSS/Atom feed scraping, full-text extraction, deduplication, and analytics management system equipped with a modern PyQt6 Graphical User Interface (GUI), CLI modes, and an automated systemd background scheduler.

## Key Features

- **Dual-Format Ingestion**: Full support for both RSS 2.0 (`<item>`) and Atom 1.0 (`<entry>`) feeds.
- **Preview & Full Article Extraction**: Captures concise preview summaries alongside complete article body content, automatically extracting main article text from source web pages when feeds only supply short snippets.
- **SHA-256 Deduplication**: Cryptographic hash tracking (`dedup_state.json`) prevents duplicate articles while dynamically updating stored entries when richer content becomes available.
- **JSON Lines Persistence**: Stores articles in append-friendly UTF-8 JSON Lines format (`SCRAPED-RESULTS/scraped_articles.jsonl`) for fast streaming, querying, and search.
- **PyQt6 Dark Theme Dashboard**: Interactive reader interface with instant category filtering, keyword search, reading time estimation, clipboard URL sharing, and live feed pinging.
- **Automated systemd Scheduler**: Background 12-hour systemd user timer (`rss-scraper.timer`) for unattended scraping.
- **Automated Test Suite**: Integrated unit and integration test coverage (`tests/test_rss.py`).

## Project Structure

```
/home/ficus-pro/Documents/RSS/
├── RSS                     # Executable bash launcher script
├── RSS.desktop             # Linux desktop application entrypoint
├── main.py                 # Application orchestrator (GUI, CLI --scrape, --headless)
├── config/
│   └── feeds.json          # Active feed configurations and polling schedules
├── core/
│   ├── cleaner.py          # HTML entity unescaping, tag stripping, and ISO-8601 date parsing
│   ├── fetcher.py          # RSS/Atom XML fetcher and full-text web page scraper
│   ├── storage.py          # SHA-256 deduplication, JSONL engine, and stats loader
│   └── scheduler.py        # Systemd user service and timer installer
├── gui/
│   └── window.py           # PyQt6 dark dashboard and article reader UI
├── tests/
│   └── test_rss.py         # Unit and integration test suite
├── SCRAPED-RESULTS/
│   ├── dedup_state.json    # SHA-256 deduplication index and metrics
│   └── scraped_articles.jsonl # Master JSONL article dataset
└── README.md
```

## Data Schema (`scraped_articles.jsonl`)

Each line in `scraped_articles.jsonl` contains a single JSON object with the following fields:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `article_id` | String | 64-character SHA-256 fingerprint hash |
| `feed_name` | String | Name of source RSS feed |
| `feed_url` | String | Source RSS feed URL |
| `category` | String | Topic category (e.g., Technology, Central Banks, World News) |
| `title` | String | Clean article title |
| `author` | String | Article author name (if available) |
| `url` | String | Direct web URL to original article |
| `published_at_iso` | String | Standardized UTC ISO-8601 publication timestamp |
| `scraped_at_iso` | String | UTC ISO-8601 timestamp recorded when scraped |
| `preview` | String | Clean preview/summary blurb |
| `summary_raw` | String | Raw RSS `<description>` or `<summary>` markup |
| `content_encoded_raw` | String | Raw RSS `<content:encoded>` or Atom `<content>` markup |
| `full_text_clean` | String | Full clean text body |
| `text_clean` | String | Primary clean text body |
| `tags` | Array | Category tag strings |

## How to Run

### GUI Desktop Mode
Launch the application window directly:
```bash
./RSS
# or
python3 main.py
```

### Headless Scraping Mode (CLI)
Run an immediate feed scrape without opening the GUI:
```bash
./RSS --scrape
# or
python3 main.py --headless
```

### Running Tests
Execute the unit and integration test suite:
```bash
python3 -m unittest tests/test_rss.py
```
