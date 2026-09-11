# RSS — Automated Feed Scraper & Article Tracking Engine

> **RSS** is a lightweight RSS 2.0 & Atom 1.0 feed ingestion, scrubbing, and tracking system. Equipped with a PyQt6 dark-themed GUI reader and a headless CLI engine, it features SHA-256 cryptographic deduplication, JSON Lines storage, full-text web fallback scraping, and background systemd scheduling.

---

## 📖 Table of Contents
- [Overview & Purpose](#-overview--purpose)
- [Key Features](#-key-features)
- [Architecture & Core Concepts](#-architecture--core-concepts)
- [File & Directory Structure](#-file--directory-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide (CLI & GUI)](#-usage-guide-cli--gui)
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

---

## ⚡ Key Features

* **Dual-Format Feed Parsing**: Full support for XML namespace handling across RSS 2.0 and Atom 1.0 standards.
* **SHA-256 Cryptographic Deduplication**: Maintains `dedup_state.json` to prevent storing identical articles across feed refreshes.
* **Append-Friendly JSON Lines Storage**: Uses `.jsonl` streaming format (`SCRAPED-RESULTS/scraped_articles.jsonl`) for fast querying without loading monolithic files into memory.
* **PyQt6 Dark Theme Dashboard**: Interactive reader UI featuring search, category filter dropdowns, reading time estimators, and subscription management tables.
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
│   └── window.py           # PyQt6 dark dashboard and article reader UI
├── features/               # Modular feature implementations
│   ├── feature_web_scraper_fallback/
│   ├── feature_systemd_scheduler/
│   ├── feature_feed_presets_library/
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

## 🧪 Testing & Quality Verification

Run the unit and integration test suites covering feed ingestion, date cleaning, deduplication, and feature modules:

```bash
# Execute core test suite
python3 -m unittest tests/test_rss.py

# Execute modular feature test suites
python3 -m unittest features/feature_web_scraper_fallback/tests/test_web_scraper_fallback.py
python3 -m unittest features/feature_systemd_scheduler/tests/test_systemd_scheduler.py
python3 -m unittest features/feature_feed_presets_library/tests/test_feed_presets.py
python3 -m unittest features/feature_gui_reader_pro/tests/test_gui_reader_pro.py

# Verify Python syntax across all modules
python3 -m py_compile main.py core/*.py gui/*.py
```

---

## 🌿 Git & Release Branching

* **Active Release Branch**: `RSS-0.1v-linux-native`
* **Remote Origin**: `https://github.com/ficusai/RSS.git`

All commits within this repository maintain strict local directory boundary isolation and follow standardized release branch naming (`<PROJECT>-0.1v-linux-native`).

---

## 📄 License & Attribution

Distributed under the **MIT License**. See `LICENSE` for details.  
Maintained by the **FICUS AI Team** (`https://github.com/ficusai`).
