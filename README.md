# RSS — Automated Feed Scraper & Article Tracking Engine

> **RSS** is a lightweight RSS 2.0 & Atom 1.0 feed ingestion, scrubbing, and tracking system. Equipped with a PyQt6 dark-themed GUI reader and a headless CLI engine, it features SHA-256 cryptographic deduplication, JSON Lines storage, full-text web fallback scraping, background systemd scheduling, and a one-click **Feed Presets Library** of 475 curated subscriptions across 22 industry categories.

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
* **Presets Library**: Jump-start a subscription catalog with 475 curated feeds spanning markets, macro, tech, AI, geopolitics, and more.

---

## ⚡ Key Features

* **Dual-Format Feed Parsing**: Full support for XML namespace handling across RSS 2.0 and Atom 1.0 standards.
* **Tiered Dual-Engine Stealth Scraping**: Combines fast `urllib` HTTP GET with modern Chrome Client Hints (`Sec-Ch-Ua`) and an evasion-hardened Playwright stealth browser engine. Automatically bypasses HTTP 403 / 412 / 503 anti-bot challenges and Cloudflare verification screens with `headless=False` interactive fallback.
* **SHA-256 Cryptographic Deduplication**: Maintains `dedup_state.json` to prevent storing identical articles across feed refreshes.
* **Append-Friendly JSON Lines Storage**: Uses `.jsonl` streaming format (`SCRAPED-RESULTS/scraped_articles.jsonl`) for fast querying without loading monolithic files into memory.
* **PyQt6 Dark Theme Dashboard**: Interactive reader UI featuring search, category filter dropdowns, reading time estimators, and subscription management tables.
* **Feed Presets Library Tab**: Dedicated GUI tab with a 475-feed curated catalog — category filter, live search, per-feed **Add**, and bulk **Add All Presets** import.
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
│   ├── feature_feed_presets_library/   # 475 curated feeds, 22 categories
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
pip install -r requirements.txt

# Install Playwright Chromium driver for anti-bot stealth scraping
python3 -m playwright install chromium
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

The **Feed Presets Library** ships as a Git branch (`feature/feed-presets-library`). It bundles **475 curated RSS/Atom feeds across 22 industry categories** extracted from market-intelligence catalogs, RSSHub endpoints, and global news feeds, offering a dedicated GUI tab:

| Feature | Description |
| :--- | :--- |
| **Curated Catalog** | 475 verified feeds, deduplicated by URL, sourced from finance, macro, technology, AI research, geopolitics, commodities, health, and more. |
| **Category Filter** | Browse by industry (`Technology`, `Central Banks`, `Commodities & Energy`, `Crypto & Forex`, `Science & Space`, …). |
| **Live Search** | Filter presets instantly by feed name, URL, or category. |
| **Per-Feed Add** | Subscribe to a single preset feed with one click; already-subscribed feeds are flagged `Subscribed`. |
| **Add All Presets** | Bulk-import the entire catalog into your subscription list in a single click. |

The module wraps the catalog in a small, dependency-free Python API under
`features/feature_feed_presets_library/implementation/feeds_presets.py`:

```python
from features.feature_feed_presets_library.implementation.feeds_presets import (
    get_preset_feeds,          # -> all 475 feeds
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
find gui -name '*.py' -not -path '*__pycache__*' | xargs python3 -m py_compile main.py
```

The presets test suite validates catalog completeness (≥ 400 feeds), URL deduplication, clean category naming, per-category filtering, text search, and duplicate detection against an active subscription list.

---

## 🌿 Git & Release Branching

* **Active Release Branch**: `RSS-0.1v-linux-native`
* **Active Feature Branch**: `feature/readability-extraction-quality`
* **Remote Origin**: `https://github.com/ficusai/RSS.git`

All commits within this repository maintain strict local directory boundary isolation and follow standardized release branch naming (`<PROJECT>-0.1v-linux-native`).

### Branch Map

| Branch | Purpose |
| :--- | :--- |
| `RSS-0.1v-linux-native` | Core release engine — lightweight RSS reader, scraper, storage, and dashboard. |
| `feature/gui-minimal-3tab` | Streamlined 3-tab GUI architecture (Articles Explorer split reader, Subscriptions Hub with collapsible presets drawer, Systemd Operations & Logs console). |
| `feature/feed-presets-library` | Bundles the 475-feed preset catalog (including RSSHub endpoints & verified global news feeds) + dedicated GUI presets tab. |
| `feature/stealth-browser-fetcher` | Tiered Dual-Engine stealth scraper with Playwright, CDP request replaying, Client Hints, and Cloudflare challenge fallback. |
| `feature/readability-extractor` | DOM-based readability & full-text article body extractor stripping layout clutter, popups, and ads. |
| `feature/tiered-cache-manager` | Tiered memory & response cache manager with lock claiming for concurrency control and thundering herd protection. |
| `feature/core-storage-fetcher-modular` | Single-function modularization of storage, cleaner, XML parser, transport fetcher, and CLI orchestrator. |
| `feature/scraping-quality-improvements` | Full-text extraction improvements: readability-based article extraction, CDATA/HTML entity parsing, and default `extract_full_text=True` for the headless CLI scraper. |
| `feature/feed-parsing-unicode-encoding-fixes` | Fixes XML parsing that silently destroyed non-ASCII characters and adds gzip/deflate/brotli decompression so br-only feeds (TechCrunch) parse. |
| `feature/readability-extraction-quality` | Readability-grade article extraction: block-aware paragraph joining (no broken inline lines), text-density main selection with link-density & boilerplate pruning, smart preview generation (no more "Comments" previews), and an `extractor_version`-gated storage refresh. Requires a full DB rebuild of `SCRAPED-RESULTS`. |
| `feature/gui-atomic-modular-refactor` | Decomposes monolithic `gui/window.py` (1,362 lines) into 39 atomic per-function modules under `gui/_00_*` … `gui/_38_*`, each in its own folder. `gui/window.py` becomes a thin re-export facade. `main.py` GUI bootstrap delegated to `gui._38_bootstrap_launch_window`. |
| `feature/gui-contract-tests` | Contract-drift snapshot test suite for all 39 GUI atomic modules: every `tests/GUI/_NN_*` file locks in each `gui/_NN_*` module's signature, imports, callables, and behaviour to catch refactor drift. |

### Branch-Related File Changes

Each feature branch owns a dedicated module folder under `features/` plus any
integration changes it introduces. The following tables record every file
touched by each branch so future branch sessions stay in sync with this README.

#### `feature/stealth-browser-fetcher`

| File | Change |
| :--- | :--- |
| `core/stealth/get_client_hints_headers.py` | Added — single-function module generating Chrome Client Hints headers (`get_client_hints_headers`). |
| `core/stealth/is_stealth_available.py` | Added — single-function module checking Playwright availability (`is_stealth_available`). |
| `core/stealth/fetch_with_stealth_browser.py` | Added — single-function module executing Playwright browser ingestion (`fetch_with_stealth_browser`). |
| `core/cookies/parse_cookie_header.py` | Added — single-function module parsing HTTP cookie strings (`parse_cookie_header`). |
| `core/cookies/format_cookie_header.py` | Added — single-function module formatting cookie dict arrays (`format_cookie_header`). |
| `core/cookies/set_playwright_cookies.py` | Added — single-function module applying cookies to Playwright context (`set_playwright_cookies`). |
| `core/cookies/get_playwright_cookies.py` | Added — single-function module extracting cookies from Playwright context (`get_playwright_cookies`). |
| `core/anti_hotlink/is_hotlink_protected.py` | Added — single-function module checking hotlink-restricted domains (`is_hotlink_protected`). |
| `core/anti_hotlink/process_anti_hotlink.py` | Added — single-function module rewriting HTML media tags (`process_anti_hotlink`). |
| `core/extractors/extract_next_data.py` | Added — single-function module extracting Next.js state (`extract_next_data`). |
| `core/extractors/extract_nuxt_data.py` | Added — single-function module extracting Nuxt.js state (`extract_nuxt_data`). |
| `core/extractors/extract_window_state.py` | Added — single-function module extracting custom window state (`extract_window_state`). |
| `core/fetcher.py` | Modified — upgraded `fetch_feed` into a Tiered Dual-Engine Fetcher (Tier 1 urllib Client Hints, Tier 2 stealth Playwright fallback). |
| `tests/test_stealth_fetcher.py` | Added — unit and integration tests for Client Hints header generation, stealth availability, and tiered fetch parsing. |
| `tests/test_cookie_manager.py` | Added — unit tests for cookie parsing and domain filtering. |
| `tests/test_anti_hotlink_and_script_data.py` | Added — unit tests for anti-hotlink media rewriting and Next.js / Nuxt.js script JSON state extraction. |
| `requirements.txt` | Added — lists `PyQt6`, `playwright`, and `pytest` dependencies. |
| `README.md` | Modified — updated Key Features, Quick Installation, Branch Map, and Branch-Related File Changes documentation. |

#### `feature/gui-minimal-3tab`

| File | Change |
| :--- | :--- |
| `features/feature_systemd_scheduler/implementation/install_systemd_timer.py` | Added — single-function module installing systemd timer and service units (`install_systemd_timer`). |
| `features/feature_systemd_scheduler/implementation/get_timer_status.py` | Added — single-function module querying systemd timer status (`get_timer_status`). |
| `features/feature_systemd_scheduler/tests/test_systemd_scheduler.py` | Added — unit test suite with systemd timer status check and mocked unit installation verification. |
| `features/feature_gui_reader_pro/implementation/get_category_color.py` | Added — single-function module computing category badge color (`get_category_color`). |
| `features/feature_gui_reader_pro/implementation/calculate_reading_time_minutes.py` | Added — single-function module estimating reading time (`calculate_reading_time_minutes`). |
| `features/feature_gui_reader_pro/tests/test_gui_reader_pro.py` | Added — unit test suite for category badge hex colors and reading time estimation. |
| `features/feature_web_scraper_fallback/implementation/clean_html_simple.py` | Added — single-function module stripping HTML tags (`clean_html_simple`). |
| `features/feature_web_scraper_fallback/implementation/fetch_full_page_text.py` | Added — single-function module crawling full web page text (`fetch_full_page_text`). |
| `features/feature_web_scraper_fallback/tests/test_web_scraper_fallback.py` | Added — unit test suite for HTML cleaning and mocked webpage text fallback scraping. |
| `gui/window.py` | Modified — completely overhauled UI into a modern 3-tab layout: Tab 1 Articles Explorer (60/40 Master-Detail Split Reader), Tab 2 Subscriptions Hub (Grid + Collapsible Add & Presets Import Drawer), and Tab 3 Operations & System (Systemd Background Scheduler Telemetry & Dedicated Log Console). |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |

#### `feature/readability-extractor`

| File | Change |
| :--- | :--- |
| `core/extractors/extract_readability.py` | Added — single-function module for DOM-based readability & full-text article body extraction (`extract_readability`). |
| `core/readability.py` | Modified — delegates to `core/extractors/extract_readability.py`. |
| `core/__init__.py` | Modified — exports `ReadabilityExtractor` class at package root level. |
| `tests/test_readability_extractor.py` | Added — unit tests for HTML layout noise stripping, title parsing, word count calculation, and edge cases. |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |

#### `feature/tiered-cache-manager`

| File | Change |
| :--- | :--- |
| `core/cache/cache_manager.py` | Added — `CacheManager` class facade for memory/Redis cache & lock management. |
| `core/cache/cache_get.py` | Added — single-function module for cache retrieval (`cache_get`). |
| `core/cache/cache_set.py` | Added — single-function module for cache insertion (`cache_set`). |
| `core/cache/cache_claim_lock.py` | Added — single-function module for concurrency lock claiming (`cache_claim_lock`). |
| `core/cache/cache_release_lock.py` | Added — single-function module for concurrency lock releasing (`cache_release_lock`). |
| `core/cache/cache_clear.py` | Added — single-function module for clearing cache store (`cache_clear`). |
| `core/cache/__init__.py` | Added — re-exports single-function modules and `CacheManager` facade. |
| `core/__init__.py` | Modified — exports `CacheManager` class at package root level. |
| `tests/test_cache_manager.py` | Added — unit tests for cache hits/misses, TTL expiration, lock claiming/releasing, and store clearing. |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |

#### `feature/core-storage-fetcher-modular`

| File | Change |
| :--- | :--- |
| `core/cleaner/clean_html.py` | Added — single-function module for HTML tag stripping (`clean_html`). |
| `core/cleaner/parse_to_iso.py` | Added — single-function module for RFC-822/ISO-8601 date parsing (`parse_to_iso`). |
| `core/storage/paths.py` | Added — path definitions and dynamic getters for storage directory and files. |
| `core/storage/ensure_dir.py` | Added — single-function module for storage directory validation (`_ensure_dir`). |
| `core/storage/generate_article_id.py` | Added — single-function module for SHA-256 article ID generation (`generate_article_id`). |
| `core/storage/load_dedup_state.py` | Added — single-function module for loading deduplication index (`_load_dedup_state`). |
| `core/storage/save_dedup_state.py` | Added — single-function module for atomic deduplication persistence (`_save_dedup_state`). |
| `core/storage/is_duplicate.py` | Added — single-function module for duplicate check lookup (`is_duplicate`). |
| `core/storage/save_articles.py` | Added — single-function module for JSONL article persistence (`save_articles`). |
| `core/storage/get_stats.py` | Added — single-function module for storage dashboard metrics (`get_stats`). |
| `core/storage/load_articles.py` | Added — single-function module for article query loading and filtering (`load_articles`). |
| `core/fetcher/get_browser_headers.py` | Added — single-function module for generating HTTP Client Hints headers (`get_browser_headers`). |
| `core/fetcher/parse_local_tag.py` | Added — single-function module for XML namespace tag stripping (`parse_local_tag`). |
| `core/fetcher/parse_item_element.py` | Added — single-function module for XML item/entry element parsing (`parse_item_element`). |
| `core/fetcher/fetch_url_bytes.py` | Added — single-function module for HTTP GET transport & GZIP decompression (`fetch_url_bytes`). |
| `core/fetcher/parse_xml_bytes.py` | Added — single-function module for XML document parsing (`parse_xml_bytes`). |
| `core/fetcher/fetch_feed.py` | Added — single-function module for dual-tier single feed ingestion (`fetch_feed`). |
| `core/fetcher/fetch_all_feeds.py` | Added — single-function module for multithreaded parallel feed scraping (`fetch_all_feeds`). |
| `core/run_headless_scrape.py` | Added — single-function module for headless CLI scraper execution (`run_headless_scrape`). |
| `main.py` | Modified — delegates CLI headless scrape execution to `core/run_headless_scrape.py`. |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |

Note: older draft modules under `features/` that are **not** implemented as Git
branches (e.g. `web_scraper_fallback`, `systemd_scheduler`, `gui_reader_pro`)
are intentionally **omitted** from this branch map until their feature branches
are actually created and pushed.

#### `feature/scraping-quality-improvements`

| File | Change |
| :--- | :--- |
| `core/extractors/extract_article_text.py` | Added — BeautifulSoup-based readability extractor used as a fallback for preview-only RSS items (`extract_article_text`). |
| `core/fetcher/parse_item_element.py` | Modified — HTML entity unescaping, CDATA handling and readability fallback for short/empty article content. |
| `core/run_headless_scrape.py` | Modified — headless CLI scrape now runs with `extract_full_text=True` by default. |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |

#### `feature/feed-parsing-unicode-encoding-fixes`

| File | Change |
| :--- | :--- |
| `core/fetcher/parse_xml_bytes.py` | Fixed — replaced the Unicode-destroying XML sanitization allow-list regex (Python `\x` captures only 2 hex digits, so the old range silently stripped Λ, –, —, curly quotes, apostrophes and ñ from titles/body text) with a precise strip of only XML-invalid control chars, surrogates and `\uFFFE/\uFFFF`. |
| `core/fetcher/fetch_url_bytes.py` | Fixed — added gzip/deflate/brotli decompression and an honest `Accept-Encoding` header (only advertises encodings that can be decoded), fixing TechCrunch (served `Content-Encoding: br`) which previously failed with `not well-formed (invalid token): line 1, column 3`. |
| `scripts/feed_parse_audit.py` | Added — one-time per-feed parsing audit (loop: ping real feed → run the RSS.desktop GUI app pipeline in an isolated store → compare headline/link/date/text stats and print a summary table). |
| `tests/test_rss.py` | Modified — added regression tests: non-ASCII title/body preservation, XML-invalid control-char stripping, malformed-HTML rejection, and gzip/deflate/brotli decoding incl. a local end-to-end brotli fetch. |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |

#### `feature/readability-extraction-quality`

| File | Change |
| :--- | :--- |
| `core/boilerplate_terms.py` | Added — single shared vocabulary of boilerplate/promo/UI chrome terms consumed by both the extractor (pruning) and storage (clutter-based replacement gate). |
| `core/extractors/extract_article_text.py` | Rewritten — readability-grade extractor: block-aware inline joins (`<a>/<code>/<span>` no longer split lines), text-density main-container selection, link-density filtering that drops nav/headline-link boxes (while protecting the first heading), boilerplate/promo pruning (incl. curly-apostrophe normalization, "Continue reading", gist comment bullets, `.com` UI fragments), and event-promo copy removal. |
| `core/fetcher/parse_item_element.py` | Modified — smart preview generation (`_is_trivial_preview`/`_make_preview`) so link-artifact descriptions like HN's "Comments" never become previews; description falls back as body text only when no full content exists; readability fallback now sends `Accept`/`Accept-Language` headers; articles record `extractor_version=2`. |
| `core/storage/save_articles.py` | Modified — replacement gate now (a) refreshes stored rows when a newer `extractor_version` produced text ≥ 40 chars, (b) replaces longer junk when the new text is measurably cleaner via the shared boilerplate vocabulary, and (c) still keeps substantive stored articles safe from short clean snippets. |
| `tests/test_rss.py` | Added — extractor regression tests (inline-tag joins, paragraph structure, boilerplate/by-line/gallery pruning, link-only heading boxes, curly-apostrophe promo, UI fragment tails, "Continue reading", nav intros, header/footer stripping), preview derivation tests (trivial "Comments" description falls back to full-text lead; substantive descriptions stay), and storage tests (cleaner-shorter replacement, no clobbering of long real text, `extractor_version` refresh). |
| `SCRAPED-RESULTS/scraped_articles.jsonl` | Rebuilt — full DB rebuild from scratch using the finalized extractor: 257 articles, all `extractor_version=2`, zero "Continue reading"/"Most Popular"/"Select an option" artifacts. |
| `README.md` | Modified — updated Branch Map and Branch-Related File Changes documentation. |

#### `feature/gui-atomic-modular-refactor`

| File | Change |
| :--- | :--- |
| `gui/_00_paths_config_constant_definitions/paths_config_constants.py` | Added — `PROJECT_ROOT`, `CONFIG_PATH`, `ASSETS_DIR` constants (fix: `.parents[2]`). |
| `gui/_01_window_stylesheet_dark_modern_theme/window_stylesheet_apply.py` | Added — `STYLESHEET` QSS string + `apply_window_stylesheet(window)`. |
| `gui/_02_background_scrape_thread_worker/scrape_thread_worker.py` | Added — `ScrapeThread(QThread)` class with `log_signal` / `finished_signal`. |
| `gui/_03_ui_assembly_orchestrator/build_main_window_ui.py` | Added — `build_main_window_ui(window)` orchestrator replacing `_build_ui`. |
| `gui/_04_ui_header_bar_top_section_build/build_header_bar.py` | Added — `build_header_bar(window)` extracting header from `_build_ui`. |
| `gui/_05_ui_articles_explorer_tab_build/build_articles_tab.py` | Added — `build_articles_tab(window)` relocated from `_build_articles_tab`. |
| `gui/_06_ui_subscriptions_hub_tab_build/build_subscriptions_tab.py` | Added — `build_subscriptions_tab(window)` relocated from `_build_subscriptions_tab`. |
| `gui/_07_ui_operations_system_tab_build/build_operations_tab.py` | Added — `build_operations_tab(window)` relocated from `_build_operations_tab`. |
| `gui/_08_ui_presets_library_tab_build/build_presets_tab.py` | Added — `build_presets_tab(window)` relocated from `_build_presets_tab`. |
| `gui/_09_feed_identifier_generate_from_name/generate_feed_id.py` | Added — `generate_feed_id(name, fallback_seed)` DRY extraction of feed-ID regex. |
| `gui/_10_log_append_timestamped_message/append_timestamped_log.py` | Added — `append_log_message(window, msg)`. |
| `gui/_11_log_clear_console/clear_log_console.py` | Added — `clear_log_console(window)`. |
| `gui/_12_add_drawer_toggle_visibility/toggle_add_drawer.py` | Added — `toggle_add_drawer(window)`. |
| `gui/_13_stats_badges_update_live/update_stats_badges.py` | Added — `update_stats_badges(window)` using `core.storage.get_stats`. |
| `gui/_14_feed_config_load_from_disk/load_feeds.py` | Added — `load_feeds(window)` reading `feeds.json`. |
| `gui/_15_feed_config_save_to_disk/save_feeds.py` | Added — `save_feeds(window)` writing `feeds.json`. |
| `gui/_16_refresh_all_views_pipeline/refresh_all_views.py` | Added — `refresh_window(window)` orchestrating all three refresh functions. |
| `gui/_17_subscriptions_table_refresh_view/refresh_subscriptions_table.py` | Added — `refresh_subscriptions_table(window)` with `blockSignals` guard. |
| `gui/_18_articles_table_refresh_view/refresh_articles_table.py` | Added — `refresh_articles_table(window)` with `blockSignals` guard. |
| `gui/_19_feed_add_single_subscription/add_feed_subscription.py` | Added — `add_feed(window)`. |
| `gui/_20_feed_delete_subscription/delete_feed_subscription.py` | Added — `delete_feed(window, fid)`. |
| `gui/_21_feed_toggle_enabled_state/toggle_feed_state.py` | Added — `toggle_feed(window, fid, on)`. |
| `gui/_22_feed_update_interval_frequency/set_feed_frequency.py` | Added — `set_feed_frequency(window, fid, hours)`. |
| `gui/_23_feed_ping_endpoint_single_scrape/ping_feed_endpoint.py` | Added — `ping_feed(window, fid)`. |
| `gui/_24_preset_quick_import_single_feed/import_preset_feed.py` | Added — `import_preset(window, name, url, category)`. |
| `gui/_25_article_selection_reader_update/on_article_selected.py` | Added — `on_article_selected(window)`. |
| `gui/_26_article_link_open_in_browser/open_article_in_browser.py` | Added — `open_article_in_browser(window)`. |
| `gui/_27_article_link_copy_to_clipboard/copy_article_link.py` | Added — `copy_article_link(window)`. |
| `gui/_28_systemd_status_refresh_daemon/refresh_systemd_status.py` | Added — `refresh_systemd_status(window)`. |
| `gui/_29_systemd_timer_install_handler/handle_install_systemd.py` | Added — `handle_install_systemd(window)`. |
| `gui/_30_preset_categories_load_dropdown/load_preset_categories.py` | Added — `load_preset_categories(window)`. |
| `gui/_31_presets_table_refresh_view/refresh_presets_table.py` | Added — `refresh_presets_table(window)`. |
| `gui/_32_preset_add_single_from_catalog/add_preset_feed.py` | Added — `add_preset_feed(window, preset)`. |
| `gui/_33_preset_add_all_bulk_import/add_all_presets.py` | Added — `add_all_presets(window)`. |
| `gui/_34_scrape_start_enabled_feeds/start_scrape.py` | Added — `start_scrape(window)`. |
| `gui/_35_scrape_run_background_orchestrator/run_scrape_background.py` | Added — `run_scrape(window, feeds)` wiring `ScrapeThread` signals. |
| `gui/_36_scrape_finished_signal_handler/on_scrape_done.py` | Added — `on_scrape_done(window, new, total, errors)`. |
| `gui/_37_main_window_facade_assembly/main_window_facade.py` | Added — `MainWindow(QMainWindow)` delegating facade class. |
| `gui/_38_bootstrap_launch_window/bootstrap_launch_window.py` | Added — `launch_gui_window()` entry point moved from `__main__` block. |
| `gui/window.py` | Replaced — now a thin re-export facade (`from gui._37_… import MainWindow`). |
| `main.py` | Modified — GUI bootstrap delegated to `gui._38_bootstrap_launch_window.launch_gui_window()`. |
| `README.md` | Modified — updated Branch Map, Branch-Related File Changes, and compile command. |

#### `feature/gui-contract-tests`

| File | Change |
| :--- | :--- |
| `tests/GUI/conftest.py` | Added — shared contract-drift fixtures: offscreen Qt bootstrap, `WindowStub`, `assert_signature`, `assert_constants`, `assert_source_imports`, `assert_callables`, `assert_signals`, `patch_constant`. |
| `tests/GUI/GUI-SCRIPT-LAUNCHER/RSS-GUI-Contract-Tests.desktop` | Added — desktop launcher entry for the contract-test suite. |
| `tests/GUI/GUI-SCRIPT-LAUNCHER/files/__main__.py` | Added — launcher package entry point. |
| `tests/GUI/GUI-SCRIPT-LAUNCHER/files/launcher.py` | Added — launcher orchestrator for the contract-test suite. |
| `tests/GUI/GUI-SCRIPT-LAUNCHER/files/run_gui_tests.sh` | Added — shell wrapper running the headless contract suite. |
| `tests/GUI/GUI-SCRIPT-LAUNCHER/files/run_tests_worker.py` | Added — worker harness executing each module's snapshot. |
| `tests/GUI/GUI-SCRIPT-LAUNCHER/files/GUI-CONTRACT-TESTS-PLAN-COMPLETED.md` | Added — completion plan for the contract-test suite. |
| `tests/GUI/_00_paths_config_constant_definitions/test_contract_snapshot_of_paths_config_constant_definitions_module.py` | Added — contract-drift snapshot guarding `gui/_00_paths_config_constant_definitions`. |
| `tests/GUI/_01_window_stylesheet_dark_modern_theme/test_contract_snapshot_of_window_stylesheet_dark_modern_theme_apply_function.py` | Added — contract-drift snapshot guarding `gui/_01_window_stylesheet_dark_modern_theme`. |
| `tests/GUI/_02_background_scrape_thread_worker/test_contract_snapshot_of_background_scrape_thread_worker_class_and_signals.py` | Added — contract-drift snapshot guarding `gui/_02_background_scrape_thread_worker`. |
| `tests/GUI/_03_ui_assembly_orchestrator/test_contract_snapshot_of_ui_assembly_orchestrator_build_main_window_ui.py` | Added — contract-drift snapshot guarding `gui/_03_ui_assembly_orchestrator`. |
| `tests/GUI/_04_ui_header_bar_top_section_build/test_contract_snapshot_of_ui_header_bar_top_section_build_build_header_bar.py` | Added — contract-drift snapshot guarding `gui/_04_ui_header_bar_top_section_build`. |
| `tests/GUI/_05_ui_articles_explorer_tab_build/test_contract_snapshot_of_ui_articles_explorer_tab_build_build_articles_tab.py` | Added — contract-drift snapshot guarding `gui/_05_ui_articles_explorer_tab_build`. |
| `tests/GUI/_06_ui_subscriptions_hub_tab_build/test_contract_snapshot_of_ui_subscriptions_hub_tab_build_build_subscriptions_tab.py` | Added — contract-drift snapshot guarding `gui/_06_ui_subscriptions_hub_tab_build`. |
| `tests/GUI/_07_ui_operations_system_tab_build/test_contract_snapshot_of_ui_operations_system_tab_build_build_operations_tab.py` | Added — contract-drift snapshot guarding `gui/_07_ui_operations_system_tab_build`. |
| `tests/GUI/_08_ui_presets_library_tab_build/test_contract_snapshot_of_ui_presets_library_tab_build_build_presets_tab.py` | Added — contract-drift snapshot guarding `gui/_08_ui_presets_library_tab_build`. |
| `tests/GUI/_09_feed_identifier_generate_from_name/test_contract_snapshot_of_feed_identifier_generate_from_name_generate_feed_id_pure_function.py` | Added — contract-drift snapshot guarding `gui/_09_feed_identifier_generate_from_name`. |
| `tests/GUI/_10_log_append_timestamped_message/test_contract_snapshot_of_log_append_timestamped_message_append_log_message.py` | Added — contract-drift snapshot guarding `gui/_10_log_append_timestamped_message`. |
| `tests/GUI/_11_log_clear_console/test_contract_snapshot_of_log_clear_console_clear_log_console.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_12_add_drawer_toggle_visibility/test_contract_snapshot_of_add_drawer_toggle_visibility_toggle_add_drawer.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_13_stats_badges_update_live/test_contract_snapshot_of_stats_badges_update_live_update_stats_badges.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_14_feed_config_load_from_disk/test_contract_snapshot_of_feed_config_load_from_disk_load_feeds.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_15_feed_config_save_to_disk/test_contract_snapshot_of_feed_config_save_to_disk_save_feeds.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_16_refresh_all_views_pipeline/test_contract_snapshot_of_refresh_all_views_pipeline_refresh_window.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_17_subscriptions_table_refresh_view/test_contract_snapshot_of_subscriptions_table_refresh_view_refresh_subscriptions_table.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_18_articles_table_refresh_view/test_contract_snapshot_of_articles_table_refresh_view_refresh_articles_table.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_19_feed_add_single_subscription/test_contract_snapshot_of_feed_add_single_subscription_add_feed.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_20_feed_delete_subscription/test_contract_snapshot_of_feed_delete_subscription_delete_feed.py` | Modified — plain-language OVEREXPLAINATION comments added (non-programmer walkthrough of every test line). |
| `tests/GUI/_21_feed_toggle_enabled_state/test_contract_snapshot_of_feed_toggle_enabled_state_toggle_feed.py` | Added — contract-drift snapshot guarding `gui/_21_feed_toggle_enabled_state`. |
| `tests/GUI/_22_feed_update_interval_frequency/test_contract_snapshot_of_feed_update_interval_frequency_set_feed_frequency.py` | Added — contract-drift snapshot guarding `gui/_22_feed_update_interval_frequency`. |
| `tests/GUI/_23_feed_ping_endpoint_single_scrape/test_contract_snapshot_of_feed_ping_endpoint_single_scrape_ping_feed.py` | Added — contract-drift snapshot guarding `gui/_23_feed_ping_endpoint_single_scrape`. |
| `tests/GUI/_24_preset_quick_import_single_feed/test_contract_snapshot_of_preset_quick_import_single_feed_import_preset.py` | Added — contract-drift snapshot guarding `gui/_24_preset_quick_import_single_feed`. |
| `tests/GUI/_25_article_selection_reader_update/test_contract_snapshot_of_article_selection_reader_update_on_article_selected.py` | Added — contract-drift snapshot guarding `gui/_25_article_selection_reader_update`. |
| `tests/GUI/_26_article_link_open_in_browser/test_contract_snapshot_of_article_link_open_in_browser_open_article_in_browser.py` | Added — contract-drift snapshot guarding `gui/_26_article_link_open_in_browser`. |
| `tests/GUI/_27_article_link_copy_to_clipboard/test_contract_snapshot_of_article_link_copy_to_clipboard_copy_article_link.py` | Added — contract-drift snapshot guarding `gui/_27_article_link_copy_to_clipboard`. |
| `tests/GUI/_28_systemd_status_refresh_daemon/test_contract_snapshot_of_systemd_status_refresh_daemon_refresh_systemd_status.py` | Added — contract-drift snapshot guarding `gui/_28_systemd_status_refresh_daemon`. |
| `tests/GUI/_29_systemd_timer_install_handler/test_contract_snapshot_of_systemd_timer_install_handler_handle_install_systemd.py` | Added — contract-drift snapshot guarding `gui/_29_systemd_timer_install_handler`. |
| `tests/GUI/_30_preset_categories_load_dropdown/test_contract_snapshot_of_preset_categories_load_dropdown_load_preset_categories.py` | Added — contract-drift snapshot guarding `gui/_30_preset_categories_load_dropdown`. |
| `tests/GUI/_31_presets_table_refresh_view/test_contract_snapshot_of_presets_table_refresh_view_refresh_presets_table.py` | Added — contract-drift snapshot guarding `gui/_31_presets_table_refresh_view`. |
| `tests/GUI/_32_preset_add_single_from_catalog/test_contract_snapshot_of_preset_add_single_from_catalog_add_preset_feed.py` | Added — contract-drift snapshot guarding `gui/_32_preset_add_single_from_catalog`. |
| `tests/GUI/_33_preset_add_all_bulk_import/test_contract_snapshot_of_preset_add_all_bulk_import_add_all_presets.py` | Added — contract-drift snapshot guarding `gui/_33_preset_add_all_bulk_import`. |
| `tests/GUI/_34_scrape_start_enabled_feeds/test_contract_snapshot_of_scrape_start_enabled_feeds_start_scrape.py` | Added — contract-drift snapshot guarding `gui/_34_scrape_start_enabled_feeds`. |
| `tests/GUI/_35_scrape_run_background_orchestrator/test_contract_snapshot_of_scrape_run_background_orchestrator_run_scrape.py` | Added — contract-drift snapshot guarding `gui/_35_scrape_run_background_orchestrator`. |
| `tests/GUI/_36_scrape_finished_signal_handler/test_contract_snapshot_of_scrape_finished_signal_handler_on_scrape_done.py` | Added — contract-drift snapshot guarding `gui/_36_scrape_finished_signal_handler`. |
| `tests/GUI/_37_main_window_facade_assembly/test_contract_snapshot_of_main_window_facade_assembly_mainwindow_class_and_methods.py` | Added — contract-drift snapshot guarding `gui/_37_main_window_facade_assembly`. |
| `tests/GUI/_38_bootstrap_launch_window/test_contract_snapshot_of_bootstrap_launch_window_launch_gui_window_entry_point.py` | Added — contract-drift snapshot guarding `gui/_38_bootstrap_launch_window`. |
| `.gitignore` | Modified — ignore `__pycache__`, scraped results, and local env artifacts for the test suite. |
| `requirements.txt` | Modified — ensure `pytest` and `PyQt6` are declared for the GUI tests. |
| `gui/__init__.py` | Modified — package exports for the atomic module tree under test. |
| `README.md` | Modified — added Branch Map row + Branch-Related File Changes table for `feature/gui-contract-tests`; documented the plain-language OVEREXPLAINATION pass over `tests/GUI/_11` … `_20`. |

---

## 📄 License & Attribution

Distributed under the **MIT License**. See `LICENSE` for details.  
Maintained by the **FICUS AI Team** (`https://github.com/ficusai`).
