# RSS Feed Scraper & Tracker Core

A high-performance, lightweight RSS 2.0 & Atom 1.0 feed scraping, deduplication, and article management system equipped with a modern PyQt6 Graphical User Interface (GUI) and CLI modes.

## Supported Operating Systems

| Operating System | Supported |
| :--- | :---: |
| LINUX | ✅ |
| WINDOWS | ✅ |
| MACOS | ✅ |
| ANDROID | ❌ |
| IOS | ❌ |

## Key Features (`main` Core Branch)

- **Dual-Format Ingestion**: Full support for both RSS 2.0 (`<item>`) and Atom 1.0 (`<entry>`) feeds.
- **SHA-256 Deduplication**: Cryptographic hash tracking (`dedup_state.json`) prevents duplicate articles across feed updates.
- **JSON Lines Persistence**: Stores articles in append-friendly UTF-8 JSON Lines format (`SCRAPED-RESULTS/scraped_articles.jsonl`) for fast streaming, querying, and search.
- **PyQt6 Dark Theme Dashboard**: Interactive reader interface with instant category filtering, keyword search, subscription catalog management, and manual sync.
- **Automated Test Suite**: Integrated unit and integration test coverage (`tests/test_rss.py`).

## Modular Feature Branches

Additional specialized features are maintained in dedicated feature branches:

- **`feature/web-scraper-fallback`**: Full web page text crawling fallback when RSS feeds only supply short preview snippets.
- **`feature/systemd-scheduler`**: Unattended 12-hour background Linux systemd service and timer installer (`rss-scraper.timer`).
- **`feature/feed-presets-library`**: Pre-configured catalog of 100+ industry feeds across 15 categories with UI preset picker.
- **`feature/gui-reader-pro`**: Advanced UI category color badging and reading time estimation.

## Project Structure

```
.
├── RSS                     # Executable bash launcher script
├── RSS.desktop             # Linux desktop application entrypoint
├── main.py                 # Application orchestrator (GUI, CLI --scrape, --headless)
├── config/
│   └── feeds.json          # Active feed configurations and polling schedules
├── core/
│   ├── cleaner.py          # HTML entity unescaping, tag stripping, and ISO-8601 date parsing
│   ├── fetcher.py          # RSS/Atom XML fetcher engine
│   └── storage.py          # SHA-256 deduplication, JSONL engine, and stats loader
├── gui/
│   └── window.py           # PyQt6 dark dashboard and article reader UI
├── tests/
│   └── test_rss.py         # Unit and integration test suite
├── SCRAPED-RESULTS/
│   ├── dedup_state.json    # SHA-256 deduplication index and metrics
│   └── scraped_articles.jsonl # Master JSONL article dataset
└── README.md
```

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
