#!/usr/bin/env bash
# ==============================================================================
# Script: start_local.sh
# Purpose: Start the production Gunicorn WSGI server and Flask backend locally
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
PID_FILE="$PROJECT_ROOT/.gunicorn.pid"
PORT=8000

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Gunicorn is already running with PID $(cat "$PID_FILE") on port $PORT"
    echo "Open in browser: http://127.0.0.1:$PORT"
    exit 0
fi

echo "==> Starting Gunicorn WSGI server on port $PORT..."
cd "$BACKEND_DIR"

gunicorn \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --pid "$PID_FILE" \
    --daemon \
    --access-logfile "$PROJECT_ROOT/access.log" \
    --error-logfile "$PROJECT_ROOT/error.log" \
    wsgi:app

sleep 1

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "================================================================="
    echo "  SUCCESS: Application is running locally!                       "
    echo "  PID: $(cat "$PID_FILE")                                       "
    echo "  Dashboard URL: http://127.0.0.1:$PORT                          "
    echo "  Liveness:      http://127.0.0.1:$PORT/healthz                  "
    echo "  Readiness:     http://127.0.0.1:$PORT/readyz                   "
    echo "  Status API:    http://127.0.0.1:$PORT/api/v1/status            "
    echo "================================================================="
    echo "To stop the server, run: ./scripts/stop_local.sh"
else
    echo "ERROR: Failed to start Gunicorn. Check error.log for details." >&2
    exit 1
fi
