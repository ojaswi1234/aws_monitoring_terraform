#!/usr/bin/env bash
# ==============================================================================
# Nagios Event Handler: Auto-recovers Flask Backend on HARD CRITICAL
# Arguments passed by Nagios: $1=STATE, $2=STATETYPE, $3=ATTEMPT
# ==============================================================================

SERVICE_STATE="${1:-UNKNOWN}"
SERVICE_STATE_TYPE="${2:-UNKNOWN}"
SERVICE_ATTEMPT="${3:-0}"
LOG_FILE="/var/log/nagios_recovery.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Event received: State=$SERVICE_STATE, Type=$SERVICE_STATE_TYPE, Attempt=$SERVICE_ATTEMPT" >> "$LOG_FILE"

# Only trigger recovery when the failure is confirmed (HARD CRITICAL)
# SOFT states (attempt 1 or 2) are ignored to avoid premature triggers on momentary network blips
if [ "$SERVICE_STATE" = "CRITICAL" ] && [ "$SERVICE_STATE_TYPE" = "HARD" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Confirmed HARD CRITICAL failure. Running Ansible recovery playbook..." >> "$LOG_FILE"
    
    ansible-playbook -i /opt/self-healing/inventory/hosts.ini /opt/self-healing/playbooks/recover_flask.yml >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - SUCCESS: Flask backend recovered successfully." >> "$LOG_FILE"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - FAILED: Ansible recovery failed. Alert remains active." >> "$LOG_FILE"
    fi
fi
