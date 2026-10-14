#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 scripts/build.py "${1:-linux}" "${2:-amd64}"
