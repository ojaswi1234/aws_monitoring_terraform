#!/usr/bin/env bash
# ==============================================================================
# Script: validate.sh
# Purpose: Comprehensive validation suite testing Python backend,
#          Terraform configuration, Ansible syntax, and live HTTP services.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INVENTORY_FILE="$PROJECT_ROOT/ansible/inventory/hosts.ini"

echo "================================================================="
echo "   DevOps Self-Healing Project: Comprehensive Validation Suite   "
echo "================================================================="

# 1. Run Python Backend Unit Tests
echo "[1/4] Running Python Flask pytest test suite..."
(cd "$PROJECT_ROOT/backend" && PYTHONPATH=. python3 -m pytest -v)
echo "==> Python Backend tests PASSED."
echo ""

# 2. Validate Terraform Configuration
echo "[2/4] Validating Terraform configuration..."
(cd "$PROJECT_ROOT/terraform" && terraform validate)
echo "==> Terraform validation PASSED."
echo ""

# 3. Validate Ansible Playbook Syntax
echo "[3/4] Validating Ansible playbooks syntax..."
CHK_INV="$INVENTORY_FILE"
if [ ! -f "$CHK_INV" ]; then
    CHK_INV="$PROJECT_ROOT/ansible/inventory/hosts.ini.example"
fi

export ANSIBLE_CONFIG="$PROJECT_ROOT/ansible/ansible.cfg"
ansible-playbook -i "$CHK_INV" "$PROJECT_ROOT/ansible/playbooks/site.yml" --syntax-check
ansible-playbook -i "$CHK_INV" "$PROJECT_ROOT/ansible/playbooks/recover_flask.yml" --syntax-check
ansible-playbook -i "$CHK_INV" "$PROJECT_ROOT/ansible/playbooks/recover_nginx.yml" --syntax-check
echo "==> Ansible playbooks syntax check PASSED."
echo ""

# 4. Live Service Endpoint Probes
echo "[4/4] Probing Infrastructure Services..."

# Check Local Stack (WSL)
if curl -s --connect-timeout 2 "http://127.0.0.1:8000/healthz" > /dev/null 2>&1; then
    echo "==> Local Flask Backend is active at http://127.0.0.1:8000"
    echo "  - GET /healthz: $(curl -s http://127.0.0.1:8000/healthz)"
    echo "  - GET /api/v1/status: $(curl -s http://127.0.0.1:8000/api/v1/status)"
fi

if curl -s --connect-timeout 2 "http://127.0.0.1:8085/" > /dev/null 2>&1; then
    echo "==> Local Nagios Core Dashboard is active at http://127.0.0.1:8085"
fi

# Check AWS Cloud Stack (if hosts.ini exists and instances are online)
if [ -f "$INVENTORY_FILE" ]; then
    APP_IP=$(grep -A 1 "\[webservers\]" "$INVENTORY_FILE" | grep "ansible_host" | awk -F'ansible_host=' '{print $2}' | awk '{print $1}')
    MONITOR_IP=$(grep -A 1 "\[monitoring\]" "$INVENTORY_FILE" | grep "ansible_host" | awk -F'ansible_host=' '{print $2}' | awk '{print $1}')

    if [ -n "$APP_IP" ] && [ "$APP_IP" != "203.0.113.20" ]; then
        if curl -fsS --connect-timeout 3 "http://$APP_IP/healthz" > /dev/null 2>&1; then
            echo "==> AWS Application Server is ONLINE at http://$APP_IP"
            echo "  - /healthz: OK"
        else
            echo "==> AWS Application Server ($APP_IP): Standby / Stopped (Not reachable)"
        fi
    fi

    if [ -n "$MONITOR_IP" ] && [ "$MONITOR_IP" != "203.0.113.10" ]; then
        if curl -fsS --connect-timeout 3 "http://$MONITOR_IP/nagios/" > /dev/null 2>&1; then
            echo "==> AWS Nagios Server is ONLINE at http://$MONITOR_IP/nagios"
        else
            echo "==> AWS Nagios Server ($MONITOR_IP): Standby / Stopped (Not reachable)"
        fi
    fi
fi

echo "================================================================="
echo "   All automated validation checks completed successfully!      "
echo "================================================================="
