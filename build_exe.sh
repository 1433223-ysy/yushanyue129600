#!/usr/bin/env bash
set -euo pipefail

# Build a single-file Linux executable (named .exe per requirement).
python -m PyInstaller \
  --onefile \
  --name ai_packet_tool.exe \
  --clean \
  main.py

echo "Build done: dist/ai_packet_tool.exe"
