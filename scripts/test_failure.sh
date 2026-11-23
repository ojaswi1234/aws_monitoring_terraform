#!/usr/bin/env bash
# ==============================================================================
# Script: test_failure.sh
# Purpose: Interactive test suite to simulate service failures and observe
#          automated self-healing recovery actions.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INVENTORY_FILE="$PROJECT_ROOT/ansible/inventory/hosts.ini"

if [ ! -f "$INVENTORY_FILE" ]; then
    echo "ERROR: Inventory file $INVENTORY_FILE not found! Run scripts/generate_inventory.sh first." >&2
    exit 1
fi

show_menu() {
    echo "================================================================="
    echo "  DevOps Infrastructure Self-Healing Failure Simulation Suite   "
    echo "================================================================="
    echo "1) Simulate Flask Backend Failure (Stop flask-backend.service)"
    echo "2) Simulate Nginx Web Server Failure (Stop nginx.service)"
    echo "3) Simulate Invalid Nginx Config (Safe Failure / Alert Verification)"
    echo "4) Tail Nagios Self-Healing Recovery Log on Monitoring Server"
    echo "5) Check Application Endpoints Health (Live Status)"
    echo "6) Exit"
    echo "================================================================="
    read -rp "Select an option [1-6]: " choice
    echo ""
}

check_health() {
    echo "==> Testing Application Health Endpoints..."
    APP_HOST=$(grep -A 1 "\[webservers\]" "$INVENTORY_FILE" | grep "ansible_host" | awk -F'ansible_host=' '{print $2}' | awk '{print $1}')
    if [ -z "$APP_HOST" ]; then
        echo "Could not parse app-server IP from inventory."
        return
    fi
    echo "Checking http://$APP_HOST/nginx-health :"
    curl -s --connect-timeout 3 "http://$APP_HOST/nginx-health" || echo "FAILED"
    echo ""
    echo "Checking http://$APP_HOST/healthz (Flask Backend) :"
    curl -s --connect-timeout 3 "http://$APP_HOST/healthz" || echo "FAILED"
    echo ""
    echo "Checking http://$APP_HOST/api/v1/status :"
    curl -s --connect-timeout 3 "http://$APP_HOST/api/v1/status" || echo "FAILED"
    echo ""
}

simulate_flask_failure() {
    echo "==> Simulating Flask Backend Failure..."
    echo "Stopping flask-backend.service on app-server..."
    ansible webservers -i "$INVENTORY_FILE" -b -m systemd -a "name=flask-backend state=stopped"
    echo ""
    echo "Service stopped. Current endpoint test:"
    check_health
    echo ""
    echo "==> Nagios will detect CRITICAL on /healthz within 60 seconds."
    echo "==> Observe Nagios Web Dashboard or tail the recovery log to see Ansible restore the service."
}

simulate_nginx_failure() {
    echo "==> Simulating Nginx Web Server Failure..."
    echo "Stopping nginx.service on app-server..."
    ansible webservers -i "$INVENTORY_FILE" -b -m systemd -a "name=nginx state=stopped"
    echo ""
    echo "Service stopped. Current endpoint test:"
    check_health
    echo ""
    echo "==> Nagios will detect CRITICAL on port 80 within 60 seconds."
    echo "==> Nagios event handler will trigger recover_nginx.sh and Ansible playbook."
}

simulate_invalid_config() {
    echo "==> Simulating Corrupt Nginx Configuration..."
    echo "Injecting intentional syntax error into test configuration..."
    ansible webservers -i "$INVENTORY_FILE" -b -m copy -a "content='invalid_syntax_error;' dest=/etc/nginx/conf.d/corrupt_test.conf"
    echo "Attempting recovery run via Ansible to verify safe abort..."
    ansible-playbook -i "$INVENTORY_FILE" "$PROJECT_ROOT/ansible/playbooks/recover_nginx.yml" || echo "==> Playbook safely aborted as expected! Corrupt config was not restarted."
    echo "Cleaning up corrupt test config..."
    ansible webservers -i "$INVENTORY_FILE" -b -m file -a "path=/etc/nginx/conf.d/corrupt_test.conf state=absent"
    echo "Restoring Nginx to healthy state..."
    ansible-playbook -i "$INVENTORY_FILE" "$PROJECT_ROOT/ansible/playbooks/recover_nginx.yml"
}

tail_recovery_log() {
    echo "==> Tailing /var/log/nagios_recovery.log on monitor-server (Ctrl+C to stop)..."
    ansible monitoring -i "$INVENTORY_FILE" -b -m shell -a "tail -n 30 -f /var/log/nagios_recovery.log"
}

while true; do
    show_menu
    case "$choice" in
        1) simulate_flask_failure ;;
        2) simulate_nginx_failure ;;
        3) simulate_invalid_config ;;
        4) tail_recovery_log ;;
        5) check_health ;;
        6) echo "Exiting failure simulation."; exit 0 ;;
        *) echo "Invalid option." ;;
    esac
    echo ""
done
