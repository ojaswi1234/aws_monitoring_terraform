#!/usr/bin/env bash
# ==============================================================================
# Script: deploy.sh
# Purpose: Orchestrates end-to-end configuration and application deployment
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
INVENTORY_FILE="$PROJECT_ROOT/ansible/inventory/hosts.ini"

echo "================================================================="
echo "  Deploying DevOps Self-Healing System via Ansible Automation   "
echo "================================================================="

if [ ! -f "$INVENTORY_FILE" ]; then
    echo "==> Generating Ansible inventory from Terraform..."
    "$SCRIPT_DIR/generate_inventory.sh"
fi

echo "==> Validating Ansible syntax across playbooks..."
ansible-playbook -i "$INVENTORY_FILE" "$PROJECT_ROOT/ansible/playbooks/site.yml" --syntax-check

echo "==> Executing master site playbook (site.yml)..."
ansible-playbook -i "$INVENTORY_FILE" "$PROJECT_ROOT/ansible/playbooks/site.yml"

echo "==> Deployment completed successfully!"
echo "==> Running health check validation..."
"$SCRIPT_DIR/validate.sh"
