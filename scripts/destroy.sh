#!/usr/bin/env bash
# ==============================================================================
# Script: destroy.sh
# Purpose: Safe, controlled teardown of all provisioned cloud infrastructure.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TERRAFORM_DIR="$PROJECT_ROOT/terraform"

echo "================================================================="
echo "   WARNING: TEARDOWN AND DESTRUCTION OF ALL AWS RESOURCES       "
echo "================================================================="
echo "This will destroy the following provisioned infrastructure:"
echo " - Monitoring EC2 Instance (Nagios Core & Self-Healing)"
echo " - Application EC2 Instance (Flask, Gunicorn & Nginx)"
echo " - AWS Security Groups (monitor-sg, app-sg)"
echo " - AWS VPC, Subnet, Route Table & Internet Gateway"
echo " - Associated EBS Root Volumes & Key Pairs"
echo "================================================================="
echo ""

read -rp "Are you absolutely sure you want to proceed with infrastructure destruction? (type 'DESTROY' to confirm): " confirm

if [ "$confirm" != "DESTROY" ]; then
    echo "Destruction aborted by user. No resources were modified."
    exit 0
fi

echo "==> Executing 'terraform destroy'..."
cd "$TERRAFORM_DIR"
terraform destroy -auto-approve

# Clean up generated local inventory
rm -f "$PROJECT_ROOT/ansible/inventory/hosts.ini"

echo "==> Teardown complete. All AWS infrastructure has been removed."
