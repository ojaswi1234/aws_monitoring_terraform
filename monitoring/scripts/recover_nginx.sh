#!/usr/bin/env bash
# ==============================================================================
# Script: recover_nginx.sh
# Purpose: Controlled Nagios Event Handler to recover failed Nginx web server
# Usage: recover_nginx.sh <SERVICESTATE> <SERVICESTATETYPE> <SERVICEATTEMPT>
# ==============================================================================

set -euo pipefail

LOG_FILE="/var/log/nagios_recovery.log"
LOCK_FILE="/var/run/recover_nginx.lock"
COOLDOWN_FILE="/var/run/recover_nginx.last_run"
COOLDOWN_SECONDS=60
MAX_ATTEMPTS=3

SERVICE_STATE="${1:-UNKNOWN}"
SERVICE_STATE_TYPE="${2:-UNKNOWN}"
SERVICE_ATTEMPT="${3:-0}"

timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

log() {
    echo "[$(timestamp)] [NGINX-RECOVERY] $*" | tee -a "$LOG_FILE"
}

# Ensure log file exists and is writable
touch "$LOG_FILE" 2>/dev/null || true

log "Event Handler triggered with STATE=$SERVICE_STATE, TYPE=$SERVICE_STATE_TYPE, ATTEMPT=$SERVICE_ATTEMPT"

# Case 1: Soft State
if [ "$SERVICE_STATE_TYPE" = "SOFT" ]; then
    log "Nginx is in SOFT state ($SERVICE_ATTEMPT/$MAX_ATTEMPTS). Waiting for state to stabilize or become HARD."
    exit 0
fi

# Case 2: Service has recovered to OK state
if [ "$SERVICE_STATE" = "OK" ]; then
    log "Nginx has returned to OK state. Resetting cooldown."
    rm -f "$COOLDOWN_FILE" 2>/dev/null || true
    exit 0
fi

# Case 3: Supported failure state: HARD CRITICAL
if [ "$SERVICE_STATE" = "CRITICAL" ] && [ "$SERVICE_STATE_TYPE" = "HARD" ]; then
    log "Confirmed HARD CRITICAL failure for Nginx! Initiating recovery sequence..."

    # Concurrency control: prevent duplicate recovery runs using file lock
    exec 200>"$LOCK_FILE"
    if ! flock -n 200; then
        log "WARNING: Another recovery process is currently running for Nginx. Exiting to prevent race condition."
        exit 0
    fi

    # Cooldown check: prevent thrashing recovery loops
    if [ -f "$COOLDOWN_FILE" ]; then
        LAST_RUN=$(cat "$COOLDOWN_FILE")
        NOW=$(date +%s)
        ELAPSED=$((NOW - LAST_RUN))
        if [ "$ELAPSED" -lt "$COOLDOWN_SECONDS" ]; then
            log "WARNING: Cooldown in effect ($ELAPSED seconds since last run, cooldown is $COOLDOWN_SECONDS s). Skipping restart."
            exit 0
        fi
    fi

    # Update cooldown timestamp
    date +%s > "$COOLDOWN_FILE"

    # Execute predefined Ansible recovery playbook
    PLAYBOOK_PATH="/opt/self-healing/playbooks/recover_nginx.yml"
    INVENTORY_PATH="/opt/self-healing/inventory/hosts.ini"

    if [ ! -f "$PLAYBOOK_PATH" ]; then
        log "ERROR: Recovery playbook not found at $PLAYBOOK_PATH!"
        exit 1
    fi

    log "Executing Ansible recovery playbook: $PLAYBOOK_PATH"
    
    if ansible-playbook -i "$INVENTORY_PATH" "$PLAYBOOK_PATH" >> "$LOG_FILE" 2>&1; then
        log "SUCCESS: Ansible recovery playbook completed successfully. Nginx restarted and verified."
    else
        log "CRITICAL: Ansible recovery playbook FAILED! Configuration may be corrupt. Manual administrator intervention required."
        exit 1
    fi
else
    log "Event ignored for STATE=$SERVICE_STATE, TYPE=$SERVICE_STATE_TYPE."
fi

exit 0
