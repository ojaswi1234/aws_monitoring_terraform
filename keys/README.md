# Project SSH Keypair Directory

## Purpose
This directory holds the project-specific SSH key pair used by:
1. **Terraform**: Registers `keys/id_rsa.pub` as the `aws_key_pair` on EC2 instances.
2. **Ansible**: Uses `keys/id_rsa` as `ansible_ssh_private_key_file` for configuration management and self-healing automation.

## Security Notice
- **`keys/id_rsa` (Private Key)**: Stored locally with `chmod 600` permissions. It is strictly excluded from Git tracking via `.gitignore`.
- **`keys/id_rsa.pub` (Public Key)**: Public identity key registered with cloud providers.
- **Git Tracking**: Only `keys/.gitkeep` and this `README.md` are committed to version control.
