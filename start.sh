#!/bin/bash
set -e
cd "$(dirname "$0")"

# ── Check python3 ─────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
  echo "[Installer Script] python3 not found. Installing..."
  if command -v apt-get &>/dev/null; then
    sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
  elif command -v pacman &>/dev/null; then
    sudo pacman -Sy --noconfirm python
  elif command -v dnf &>/dev/null; then
    sudo dnf install -y python3 python3-pip
  else
    echo "[Installer Script] ERROR: Cannot install python3 — please install it manually."
    exit 1
  fi
fi

# ── Create venv if missing ─────────────────────────────────────────────────────
if [ ! -d "venv" ]; then
  echo "[Installer Script] Creating virtual environment..."
  python3 -m venv venv
fi

# ── Install/update dependencies ───────────────────────────────────────────────
echo "[Installer Script] Installing dependencies..."
venv/bin/pip install --quiet --upgrade pip
venv/bin/pip install --quiet -r requirements.txt

# ── Launch ────────────────────────────────────────────────────────────────────
echo "[Installer Script] Starting server → http://localhost:3000"
venv/bin/python -m uvicorn server:app --host 0.0.0.0 --port 3000
