#!/usr/bin/env bash
# Launcher for the RSS GUI contract-drift test suite.
# Double-click the .desktop file, or run this script directly.
set -euo pipefail

# Resolve directories relative to THIS script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

export QT_QPA_PLATFORM=offscreen
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"

cd "${SCRIPT_DIR}"
exec python3 -m GUI_SCRIPT_LAUNCHER "$@"
