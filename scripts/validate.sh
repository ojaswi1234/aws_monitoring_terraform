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

# 4. Live Service Endpoint Probes (if deployed)
echo "[4/4] Probing Live Infrastructure Services..."
if [ -f "$INVENTORY_FILE" ]; then
    APP_IP=$(grep -A 1 "\[webservers\]" "$INVENTORY_FILE" | grep "ansible_host" | awk -F'ansible_host=' '{print $2}' | awk '{print $1}')
    MONITOR_IP=$(grep -A 1 "\[monitoring\]" "$INVENTORY_FILE" | grep "ansible_host" | awk -F'ansible_host=' '{print $2}' | awk '{print $1}')

    if [ -n "$APP_IP" ] && [ "$APP_IP" != "203.0.113.20" ]; then
        echo "Testing App Server at $APP_IP:"
        curl -fsS --connect-timeout 5 "http://$APP_IP/nginx-health" && echo " [OK] /nginx-health"
        curl -fsS --connect-timeout 5 "http://$APP_IP/healthz" && echo " [OK] /healthz (Flask Backend)"
        curl -fsS --connect-timeout 5 "http://$APP_IP/readyz" && echo " [OK] /readyz"
        curl -fsS --connect-timeout 5 "http://$APP_IP/api/v1/status" && echo " [OK] /api/v1/status"
        curl -fsS --connect-timeout 5 "http://$APP_IP/api/v1/info" && echo " [OK] /api/v1/info"
    fi

    if [ -n "$MONITOR_IP" ] && [ "$MONITOR_IP" != "203.0.113.10" ]; then
        echo "Testing Monitoring Server at $MONITOR_IP:"
        curl -fsS --connect-timeout 5 -o /dev/null -w "%{http_code}\n" "http://$MONITOR_IP/nagios/" && echo " [OK] Nagios Dashboard HTTP reachable"
    fi
else
    echo "Infrastructure not yet deployed to AWS. Local pre-flight checks completed."
fi

echo "================================================================="
echo "   All automated validation checks completed successfully!      "
echo "================================================================="
