#!/usr/bin/env bash
# ==============================================================================
# Script: stop_local.sh
# Purpose: Stop locally running Gunicorn and Nagios web servers
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PID_FILE="$PROJECT_ROOT/.gunicorn.pid"
NAGIOS_PID_FILE="$PROJECT_ROOT/.nagios_web.pid"

# Stop Gunicorn
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "==> Stopping Gunicorn process (PID: $PID)..."
        kill -15 "$PID" 2>/dev/null || kill -9 "$PID" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
fi

# Stop Nagios Python Web Server
if [ -f "$NAGIOS_PID_FILE" ]; then
    N_PID=$(cat "$NAGIOS_PID_FILE")
    if kill -0 "$N_PID" 2>/dev/null; then
        echo "==> Stopping Nagios web process (PID: $N_PID)..."
        kill -15 "$N_PID" 2>/dev/null || kill -9 "$N_PID" 2>/dev/null || true
    fi
    rm -f "$NAGIOS_PID_FILE"
fi

# Clean up any stray processes on 8085
pkill -f "nagios_server.py" 2>/dev/null || true

echo "==> All local servers have been stopped."
