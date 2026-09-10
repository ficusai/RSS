# RSS Feed Scraper

A robust RSS feed scraping, aggregation, and management system equipped with a PyQt6 Graphical User Interface (GUI) and an automated systemd background scheduler.

## Features

- **RSS Feed Aggregation**: Scrapes configured RSS/Atom feeds periodically or on demand.
- **Data Storage**: Stores scraped feed data in append-friendly JSONL (JSON Lines) format for high throughput, seamless streaming, and easy parsing.
- **PyQt6 GUI**: Desktop user interface to monitor feed statuses, view scraped news articles, manage feed configurations, and trigger manual scraping jobs.
- **systemd Background Scheduler**: Linux systemd service and timer integration to execute automated scraping tasks in the background at regular intervals.

## Project Structure

```
/home/ficus-pro/Documents/RSS/
├── config/
│   └── feeds.json          # Seed feed configurations and settings
├── core/                   # Core scraping, parsing, and storage logic
├── gui/                    # PyQt6 GUI interface code
├── SCRAPED-RESULTS/        # Output directory for stored JSONL data files
├── .gitignore
└── README.md
```

## Configuration

Feeds are specified in `config/feeds.json`. Enabled feeds will be processed automatically by the scheduler or on-demand via the GUI/CLI.
