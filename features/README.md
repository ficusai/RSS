# Local Features & Git Branch Mapping Index

This directory provides a clear local mapping of all feature modules and their respective test suites to their corresponding Git branches under `/home/ficus-pro/Documents/RSS/features/`.

| Feature Branch Name | Local Implementation Folder | Local Test Suite | Branch Purpose & Description |
| :--- | :--- | :--- | :--- |
| **`feature/feed-presets-library`** | `features/feature_feed_presets_library/implementation/` | `features/feature_feed_presets_library/tests/test_feed_presets.py` | Pre-configured library of 239 curated RSS/Atom feed subscriptions across 22 industry categories. |

## Running Local Feature Tests

You can run unit tests for any specific feature module locally from the project root directory:

```bash
# Test Feed Presets Library Feature
python3 -m unittest features/feature_feed_presets_library/tests/test_feed_presets.py
```
