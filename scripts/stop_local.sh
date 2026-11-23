#!/usr/bin/env bash
# ==============================================================================
# Script: stop_local.sh
# Purpose: Stop the locally running Gunicorn WSGI server
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PID_FILE="$PROJECT_ROOT/.gunicorn.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "==> Stopping Gunicorn process (PID: $PID)..."
        kill -15 "$PID" 2>/dev/null || kill -9 "$PID" 2>/dev/null || true
        rm -f "$PID_FILE"
        echo "==> Application stopped successfully."
        exit 0
    fi
    rm -f "$PID_FILE"
fi

echo "No running Gunicorn instance found."
