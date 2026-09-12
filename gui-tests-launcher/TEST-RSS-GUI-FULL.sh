#!/bin/bash
# Launch RSS GUI contract test suite
export PYTHONPATH="/home/ficus-pro/Documents/RSS:/home/ficus-pro/Documents/RSS/tests/GUI/GUI-SCRIPT-LAUNCHER/files:$PYTHONPATH"
cd /home/ficus-pro/Documents/RSS/tests/GUI/GUI-SCRIPT-LAUNCHER/files
exec python3 launcher.py "$@"
