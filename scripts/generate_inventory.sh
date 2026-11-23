#!/usr/bin/env bash
# ==============================================================================
# Script: generate_inventory.sh
# Purpose: Extract dynamic EC2 instance IPs from Terraform and generate
#          Ansible hosts.ini inventory file automatically.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TERRAFORM_DIR="$PROJECT_ROOT/terraform"
INVENTORY_FILE="$PROJECT_ROOT/ansible/inventory/hosts.ini"

echo "==> Extracting inventory from Terraform outputs..."

if [ ! -d "$TERRAFORM_DIR/.terraform" ]; then
    echo "ERROR: Terraform has not been initialized. Please run 'terraform init' in $TERRAFORM_DIR." >&2
    exit 1
fi

if ! terraform -chdir="$TERRAFORM_DIR" output ansible_inventory > /dev/null 2>&1; then
    echo "ERROR: Could not read 'ansible_inventory' output from Terraform." >&2
    echo "Please ensure 'terraform apply' has successfully executed." >&2
    exit 1
fi

mkdir -p "$(dirname "$INVENTORY_FILE")"
terraform -chdir="$TERRAFORM_DIR" output -raw ansible_inventory > "$INVENTORY_FILE"

echo "==> Successfully generated $INVENTORY_FILE"
echo "----------------------------------------------------"
cat "$INVENTORY_FILE"
echo "----------------------------------------------------"
echo "==> Testing Ansible connectivity (ansible all -m ping)..."
ansible all -m ping || echo "WARNING: One or more hosts are not yet reachable. Check SSH and Security Group rules."
