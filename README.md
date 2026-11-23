# Automated DevOps Infrastructure & Self-Healing System

A production-style DevOps implementation combining Infrastructure as Code (Terraform), Configuration Management (Ansible), a Python Flask REST backend behind Nginx and Gunicorn, continuous monitoring with Nagios Core, and automated closed-loop self-healing via event handlers.

---

## Architecture Summary

```
                      +-------------------+
                      |   Administrator   |
                      +---------+---------+
                                |
               +----------------+----------------+
               | HTTP (80)                       | HTTP (80)
               v                                 v
     +-------------------+             +-------------------+
     | Monitoring Server |             | Application Server|
     | (monitor-server)  |             | (app-server)      |
     |                   |             |                   |
     |  Nagios Core 4.x  |== HTTP ====>| Nginx (:80)       |
     |  Nagios Plugins   |  (/healthz) |   | (proxy)       |
     |  Event Handlers   |             |   v               |
     |  Ansible Engine   |== SSH =====>| Gunicorn (:8000)  |
     |  (Self-Healing)   |  (Recovery) |   | (WSGI)        |
     +-------------------+             |   v               |
                                       | Flask Application |
                                       +-------------------+
```

### Components and Responsibilities

- **Terraform (`terraform/`)**: Provisions the AWS VPC, public subnet, security groups (`monitor-sg`, `app-sg`), SSH key-pairs, and two EC2 Ubuntu instances.
- **Ansible (`ansible/`)**: Automates system configuration, package dependencies, Python virtualenv setup, systemd services, Nginx reverse proxy routing, and Nagios Core configuration.
- **Python Backend (`backend/`)**: Modular REST API built with Flask factory pattern (`create_app()`), providing `/healthz`, `/readyz`, `/api/v1/status`, `/api/v1/info`, and `/api/v1/metrics`.
- **Gunicorn & Nginx**: Gunicorn serves the WSGI application locally on `127.0.0.1:8000`. Nginx acts as the public reverse proxy and static asset server.
- **Nagios Core (`monitoring/`)**: Performs periodic health checks against `/healthz`, `/readyz`, and system resources via NRPE.
- **Self-Healing Automation (`monitoring/scripts/`, `ansible/playbooks/recover_*.yml`)**: When a service reaches `HARD CRITICAL`, Nagios triggers an event handler that acquires a file lock, verifies cooldown timers, and executes a targeted Ansible recovery playbook over private VPC networking.

---

## Directory Layout

```text
devops-self-healing-project/
├── backend/                  # Flask REST API, WSGI entrypoint & pytest suite
├── frontend/                 # Lightweight dashboard consuming backend APIs
├── terraform/                # AWS infrastructure provisioning definitions
├── ansible/
│   ├── ansible.cfg           # Ansible configuration
│   ├── inventory/            # Inventory definitions & templates
│   ├── playbooks/            # Site, deploy, monitoring, and recovery playbooks
│   └── roles/                # Modular Ansible roles (backend, nginx, nagios, etc.)
├── monitoring/
│   ├── nagios/               # Custom host/service check definitions
│   └── scripts/              # Event handlers for self-healing (recover_flask.sh, recover_nginx.sh)
├── scripts/                  # Orchestration utilities (deploy, validate, test_failure, destroy)
└── docs/                     # Technical specifications and architectural diagrams
```

---

## Validation & Testing

Run the automated pre-flight validation suite:
```bash
./scripts/validate.sh
```

This verifies:
1. Python unit tests via `pytest` (all 7 endpoints and error handlers).
2. Terraform syntax and resource validation (`terraform validate`).
3. Ansible syntax across all 5 playbooks.
4. HTTP probes on running infrastructure (when deployed).

---

## Failure Simulation & Recovery Workflow

To test automated self-healing interactively:
```bash
./scripts/test_failure.sh
```

Select:
- **Option 1**: Stops `flask-backend.service`. Nagios detects `CRITICAL` on `/healthz` and triggers `recover_flask.sh` to restart the service automatically.
- **Option 2**: Stops `nginx.service`. Nagios detects HTTP failure and triggers `recover_nginx.sh`.
- **Option 3**: Injects invalid configuration syntax into Nginx to verify that the recovery playbook halts safely without creating crash loops.
- **Option 4**: Streams `/var/log/nagios_recovery.log` from the monitoring server in real time.
