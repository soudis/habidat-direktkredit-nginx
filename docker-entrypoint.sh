#!/bin/bash
set -e

echo "Generating config files..."
python3 scripts/generate_config.py

exec "$@"