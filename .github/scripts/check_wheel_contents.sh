#!/usr/bin/env bash
set -euo pipefail

contents=$(unzip -l dist/*.whl)
for file in air_link/air-link.service air_link/.syncignore; do
    grep -q "$file" <<<"$contents" || { echo "The wheel is missing $file"; exit 1; }
done
