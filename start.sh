#!/bin/bash
# GraphMind Backend Startup Script
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║       GraphMind Backend  v1.0.0          ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "→ Creating virtual environment…"
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install deps
echo "→ Installing dependencies…"
pip install -q -r requirements.txt

echo ""
echo "→ Starting server at http://localhost:8000"
echo "→ API docs at    http://localhost:8000/docs"
echo "→ Press Ctrl+C to stop"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
