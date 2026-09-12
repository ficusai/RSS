#!/usr/bin/env bash
# Launcher for the RSS GUI contract-drift test suite.
# Double-click the .desktop file to run.
set -euo pipefail

# Resolve directories relative to THIS script's location
LAUNCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${LAUNCHER_DIR}/../../../../.." && pwd)"

export QT_QPA_PLATFORM=offscreen
export PYTHONPATH="${PROJECT_ROOT}:${LAUNCHER_DIR}:${PYTHONPATH:-}"

exec python3 -m GUI_SCRIPT_LAUNCHER "$@"
