#!/usr/bin/env bash
# ==============================================================================
# Script: start_local.sh
# Purpose: Start both Gunicorn (Port 8000) and Nagios Core CGI Server (Port 8085)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
PID_FILE="$PROJECT_ROOT/.gunicorn.pid"
NAGIOS_PID_FILE="$PROJECT_ROOT/.nagios_web.pid"
PORT=8000
NAGIOS_PORT=8085

# 1. Start Gunicorn WSGI Server on Port 8000
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Gunicorn is already running on port $PORT (PID: $(cat "$PID_FILE"))"
else
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
fi

# 2. Start Nagios Core CGI & Web Server on Port 8085
if [ -f "$NAGIOS_PID_FILE" ] && kill -0 "$(cat "$NAGIOS_PID_FILE")" 2>/dev/null; then
    echo "Nagios Web Server is already running on port $NAGIOS_PORT"
else
    echo "==> Starting Nagios Core CGI Web Server on port $NAGIOS_PORT..."
    python3 "$SCRIPT_DIR/nagios_server.py" > /dev/null 2>&1 &
    echo $! > "$NAGIOS_PID_FILE"
    sleep 1
fi

echo "================================================================="
echo "  ALL SERVICES ARE RUNNING LIVE!                                 "
echo "  1. Main Web Console:     http://localhost:$PORT                "
echo "  2. Official Nagios Core: http://localhost:$NAGIOS_PORT         "
echo "================================================================="
echo "To stop all services, run: ./scripts/stop_local.sh"
