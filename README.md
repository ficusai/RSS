# RSS — Automated Feed Scraper & Article Tracking Engine

> **RSS** is a lightweight RSS 2.0 & Atom 1.0 feed ingestion, scrubbing, and tracking system. Equipped with a PyQt6 dark-themed GUI reader and a headless CLI engine, it features SHA-256 cryptographic deduplication, JSON Lines storage, full-text web fallback scraping, background systemd scheduling, and a one-click **Feed Presets Library** of 247 curated subscriptions across 22 industry categories.

---

## 📖 Table of Contents
- [Overview & Purpose](#-overview--purpose)
- [Key Features](#-key-features)
- [Architecture & Core Concepts](#-architecture--core-concepts)
- [File & Directory Structure](#-file--directory-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide (CLI & GUI)](#-usage-guide-cli--gui)
- [Feed Presets Library](#-feed-presets-library)
- [Testing & Quality Verification](#-testing--quality-verification)
- [Git & Release Branching](#-git--release-branching)
- [License & Attribution](#-license--attribution)

---

## 💡 Overview & Purpose

Consolidating news, research, and technical blogs across disparate websites often results in duplicate content, broken formatting, or rate-limiting issues.

**RSS** provides a unified pipeline:
* **Ingestion**: Fetches RSS 2.0 (`<item>`) and Atom 1.0 (`<entry>`) feeds using multithreaded parallel requests.
* **Cleaning**: Strips raw HTML, unescapes HTML entities, normalizes timestamps into ISO-8601 UTC, and scrubs script tags.
* **Storage**: Deduplicates entries via SHA-256 hashes and appends entries to UTF-8 JSON Lines datasets (`scraped_articles.jsonl`).
* **Reader & Operations**: Browse, search, and manage feed subscriptions inside a PyQt6 desktop application.
* **Presets Library**: Jump-start a subscription catalog with 239 curated feeds spanning markets, macro, tech, AI, geopolitics, and more.

---

## ⚡ Key Features

* **Dual-Format Feed Parsing**: Full support for XML namespace handling across RSS 2.0 and Atom 1.0 standards.
* **SHA-256 Cryptographic Deduplication**: Maintains `dedup_state.json` to prevent storing identical articles across feed refreshes.
* **Append-Friendly JSON Lines Storage**: Uses `.jsonl` streaming format (`SCRAPED-RESULTS/scraped_articles.jsonl`) for fast querying without loading monolithic files into memory.
* **PyQt6 Dark Theme Dashboard**: Interactive reader UI featuring search, category filter dropdowns, reading time estimators, and subscription management tables.
* **Feed Presets Library Tab**: Dedicated GUI tab with a 239-feed curated catalog — category filter, live search, per-feed **Add**, and bulk **Add All Presets** import.
* **Web Scraper Fallback Module**: Automatically crawls full web page HTML when feeds only supply short preview snippets.
* **Systemd Background Scheduler**: Unattended Linux background timer (`rss-scraper.timer`) executing 12-hour background updates.
* **Headless CLI Scraping**: Execute `--headless` or `--scrape` commands for server automation and cron jobs.

---

## 🏗 Architecture & Core Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│                    PyQt6 GUI / Headless CLI                     │
│                    main.py / RSS Script                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ core/fetcher.py              │ │ core/cleaner.py              │
│ Parallel ThreadPoolExecutor  │ │ HTML Tag Stripping           │
│ RSS 2.0 & Atom 1.0 Parser    │ │ ISO-8601 UTC Conversion      │
└──────────────┬───────────────┘ └──────────────┬───────────────┘
               │                               │
               └───────────────┬───────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│ core/storage.py — SHA-256 Deduplication & JSONL Engine            │
│ ├─ dedup_state.json                                             │
│ └─ SCRAPED-RESULTS/scraped_articles.jsonl                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 File & Directory Structure

```
RSS/
├── main.py                 # Application orchestrator (GUI & CLI headless modes)
├── RSS                     # Executable bash launcher script
├── RSS.desktop             # Linux desktop application entrypoint
├── config/
│   └── feeds.json          # Active feed subscription configuration
├── core/
│   ├── fetcher.py          # Multithreaded RSS/Atom XML ingestion engine
│   ├── cleaner.py          # HTML unescaping, entity scrubbing & date parsing
│   └── storage.py          # SHA-256 deduplication & JSON Lines persistence
├── gui/
│   └── window.py           # PyQt6 dark dashboard, article reader & presets UI
├── features/               # Modular feature implementations
│   ├── feature_web_scraper_fallback/
│   ├── feature_systemd_scheduler/
│   ├── feature_feed_presets_library/   # 239 curated feeds, 22 categories
│   └── feature_gui_reader_pro/
├── tests/                  # Core PyTest / unittest suite
│   └── test_rss.py
├── SCRAPED-RESULTS/        # Output datasets
│   ├── dedup_state.json    # SHA-256 deduplication state index
│   └── scraped_articles.jsonl # Master JSONL article dataset
└── assets/                 # App icon resources
```

---

## 🚀 Installation & Setup

### Prerequisites
* Python **3.11** or higher
* PyQt6, BeautifulSoup4, Feedparser, Requests

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/ficusai/RSS.git
cd RSS

# Install Python dependencies
pip install PyQt6 beautifulsoup4 feedparser requests
```

---

## 💻 Usage Guide (CLI & GUI)

### 1. Graphical User Interface (GUI) Mode
Launch the interactive desktop reader dashboard:

```bash
./RSS
# or
python3 main.py
```

### 2. Headless Scraping Mode (CLI)
Run an immediate background batch scrape and exit without opening a window:

```bash
./RSS --scrape
# or
python3 main.py --headless
```

---

## 📚 Feed Presets Library

> Standalone module, disabled in the core release branch.

The **Feed Presets Library** ships as a Git branch (`feature/feed-presets-library`). It bundles **239 curated RSS/Atom feeds across 22 industry categories** extracted from market-intelligence catalogs and offers a dedicated GUI tab:

| Feature | Description |
| :--- | :--- |
| **Curated Catalog** | 239 verified feeds, deduplicated by URL, sourced from finance, macro, technology, AI research, geopolitics, commodities, health, and more. |
| **Category Filter** | Browse by industry (`Technology`, `Central Banks`, `Commodities & Energy`, `Crypto & Forex`, `Science & Space`, …). |
| **Live Search** | Filter presets instantly by feed name, URL, or category. |
| **Per-Feed Add** | Subscribe to a single preset feed with one click; already-subscribed feeds are flagged `Subscribed`. |
| **Add All Presets** | Bulk-import the entire catalog into your subscription list in a single click. |

The module wraps the catalog in a small, dependency-free Python API under
`features/feature_feed_presets_library/implementation/feeds_presets.py`:

```python
from features.feature_feed_presets_library.implementation.feeds_presets import (
    get_preset_feeds,          # -> all 239 feeds
    get_preset_categories,     # -> 22 category names
    get_presets_by_category,   # -> filter by category ("all" for everything)
    search_presets,            # -> text search over name/url/category
    feed_already_present,      # -> duplicate check against active feeds
)
```

### Presets GUI Usage

1. Launch the app (`./RSS` or `python3 main.py`).
2. Open the **Feed Presets Library** tab.
3. Pick a category or type a search term.
4. Click **Add** on any row to subscribe, or **Add All Presets** to import the whole catalog.

---

## 🧪 Testing & Quality Verification

Run the unit and integration test suites covering feed ingestion, date cleaning, deduplication, and feature modules:

```bash
# Execute core test suite
python3 -m unittest tests/test_rss.py

# Execute modular feature test suites
python3 -m unittest features/feature_feed_presets_library/tests/test_feed_presets.py

# Verify Python syntax across all modules
python3 -m py_compile main.py core/*.py gui/*.py
```

The presets test suite validates catalog completeness (≥ 200 feeds), URL deduplication, clean category naming, per-category filtering, text search, and duplicate detection against an active subscription list.

---

## 🌿 Git & Release Branching

* **Active Release Branch**: `RSS-0.1v-linux-native`
* **Active Feature Branch**: `feature/feed-presets-library`
* **Remote Origin**: `https://github.com/ficusai/RSS.git`

All commits within this repository maintain strict local directory boundary isolation and follow standardized release branch naming (`<PROJECT>-0.1v-linux-native`).

### Branch Map

| Branch | Purpose |
| :--- | :--- |
| `RSS-0.1v-linux-native` | Core release engine — lightweight RSS reader, scraper, storage, and dashboard. |
| `feature/feed-presets-library` | Bundles the 239-feed preset catalog + dedicated GUI presets tab. |

### Branch-Related File Changes

Each feature branch owns a dedicated module folder under `features/` plus any
integration changes it introduces. The following tables record every file
touched by each branch so future branch sessions stay in sync with this README.

#### `feature/feed-presets-library`

| File | Change |
| :--- | :--- |
| `features/feature_feed_presets_library/implementation/feeds_presets.py` | Added — 247 curated RSS/Atom feeds across 22 categories (including RSSHub endpoints) + lookup/duplicate-check API (`get_preset_feeds`, `get_preset_categories`, `get_presets_by_category`, `search_presets`, `feed_already_present`). |
| `config/feeds.json` | Modified — includes active default subscriptions for RSSHub endpoints (36Kr Newsflashes, Zhihu Daily). |
| `features/feature_feed_presets_library/tests/test_feed_presets.py` | Added — validates catalog size, category cleanliness, URL dedup, filtering, search, and duplicate detection. |
| `gui/window.py` | Modified — adds the **Feed Presets Library** tab (category combo, search box, presets table, per-feed Add, Add All Presets) and shared `get_category_color` helper. |
| `README.md` | Modified — documents the presets module, GUI usage, tests, and this branching map. |

Note: older draft modules under `features/` that are **not** implemented as Git
branches (e.g. `web_scraper_fallback`, `systemd_scheduler`, `gui_reader_pro`)
are intentionally **omitted** from this branch map until their feature branches
are actually created and pushed.

---

## 📄 License & Attribution

Distributed under the **MIT License**. See `LICENSE` for details.  
Maintained by the **FICUS AI Team** (`https://github.com/ficusai`).
