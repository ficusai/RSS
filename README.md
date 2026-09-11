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
- **Dynamic Path Optimization**: All paths are dynamically calculated using Python `Path` and bash `dirname` for cross-machine Linux compatibility.

## Active Feature Branches Under Development

The project is modularized into dedicated feature branches online and in local `features/` directories:

| Feature Branch Name | Local Implementation Directory | Branch Purpose & Scope |
| :--- | :--- | :--- |
| **`feature/web-scraper-fallback`** | `features/feature_web_scraper_fallback/` | Full web page text crawling fallback when RSS feeds only supply short preview snippets. |
| **`feature/systemd-scheduler`** | `features/feature_systemd_scheduler/` | Unattended 12-hour background Linux systemd service and timer installer (`rss-scraper.timer`). |
| **`feature/feed-presets-library`** | `features/feature_feed_presets_library/` | Pre-configured catalog of 100+ industry feeds across 15 categories with UI preset picker. |
| **`feature/gui-reader-pro`** | `features/feature_gui_reader_pro/` | Advanced UI category color badging and reading time estimation. |

## Project Structure

```
.
├── RSS                     # Executable bash launcher script (dynamic paths)
├── RSS.desktop             # Linux desktop application entrypoint (dynamic paths)
├── main.py                 # Application orchestrator (GUI, CLI --scrape, --headless)
├── config/
│   └── feeds.json          # Active default feed configurations
├── core/
│   ├── cleaner.py          # HTML entity unescaping, tag stripping, and ISO-8601 date parsing
│   ├── fetcher.py          # RSS/Atom XML fetcher engine
│   └── storage.py          # SHA-256 deduplication, JSONL engine, and stats loader
├── features/
│   ├── README.md           # Local features index mapping code & tests to git branches
│   ├── feature_web_scraper_fallback/
│   ├── feature_systemd_scheduler/
│   ├── feature_feed_presets_library/
│   └── feature_gui_reader_pro/
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

#### Core Test Suite
```bash
python3 -m unittest tests/test_rss.py
```

#### Local Feature Test Suites
```bash
python3 -m unittest features/feature_web_scraper_fallback/tests/test_web_scraper_fallback.py
python3 -m unittest features/feature_systemd_scheduler/tests/test_systemd_scheduler.py
python3 -m unittest features/feature_feed_presets_library/tests/test_feed_presets.py
python3 -m unittest features/feature_gui_reader_pro/tests/test_gui_reader_pro.py
```
