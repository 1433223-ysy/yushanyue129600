#!/usr/bin/env bash
set -euo pipefail

# Build a single-file Linux executable (named .exe per requirement).
# Optional: pass custom python binary, e.g. ./build_exe.sh python3.10
PY_BIN="${1:-python3}"

if ! command -v "$PY_BIN" >/dev/null 2>&1; then
  echo "[ERROR] Python not found: $PY_BIN"
  exit 1
fi

if ! "$PY_BIN" -m PyInstaller --version >/dev/null 2>&1; then
  echo "[ERROR] PyInstaller is not installed in current environment."
  echo "        Install with: $PY_BIN -m pip install pyinstaller"
  exit 1
fi

"$PY_BIN" -m PyInstaller \
python -m PyInstaller \
  --onefile \
  --name ai_packet_tool.exe \
  --clean \
  main.py

echo "Build done: dist/ai_packet_tool.exe"
