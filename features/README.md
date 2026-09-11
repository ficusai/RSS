# Local Features & Git Branch Mapping Index

This directory provides a clear local mapping of all feature modules and their respective test suites to their corresponding Git branches under `/home/ficus-pro/Documents/RSS/features/`.

| Feature Branch Name | Local Implementation Folder | Local Test Suite | Branch Purpose & Description |
| :--- | :--- | :--- | :--- |
| **`feature/web-scraper-fallback`** | `features/feature_web_scraper_fallback/implementation/` | `features/feature_web_scraper_fallback/tests/test_web_scraper_fallback.py` | Extracts full text from article web pages when RSS feeds only provide short summary blurbs. |
| **`feature/systemd-scheduler`** | `features/feature_systemd_scheduler/implementation/` | `features/feature_systemd_scheduler/tests/test_systemd_scheduler.py` | Installs and manages background 12-hour Linux systemd service and timer units (`rss-scraper.timer`). |
| **`feature/feed-presets-library`** | `features/feature_feed_presets_library/implementation/` | `features/feature_feed_presets_library/tests/test_feed_presets.py` | Pre-configured library of curated RSS/Atom feed subscriptions across 15+ industry categories. |
| **`feature/gui-reader-pro`** | `features/feature_gui_reader_pro/implementation/` | `features/feature_gui_reader_pro/tests/test_gui_reader_pro.py` | Advanced GUI UX enhancements including category color badging and reading time estimators. |

## Running Local Feature Tests

You can run unit tests for any specific feature module locally from the project root directory:

```bash
# Test Web Scraper Fallback Feature
python3 -m unittest features/feature_web_scraper_fallback/tests/test_web_scraper_fallback.py

# Test Systemd Scheduler Feature
python3 -m unittest features/feature_systemd_scheduler/tests/test_systemd_scheduler.py

# Test Feed Presets Library Feature
python3 -m unittest features/feature_feed_presets_library/tests/test_feed_presets.py

# Test GUI Reader Pro Components
python3 -m unittest features/feature_gui_reader_pro/tests/test_gui_reader_pro.py
```
