# DevOps Project Viva & Defense Guide

This guide is specifically designed for your 4th-year DevOps presentation and external evaluation. It provides direct, technically accurate, and easy-to-explain answers to the most common questions professors and examiners ask.

---

## 1. Core Architecture & Concept

### Q1: What is the main objective of this project in one sentence?
> **Answer:** "It is a closed-loop automated DevOps system where Terraform provisions cloud infrastructure, Ansible configures servers and deploys a Python WSGI backend behind Nginx, Nagios continuously monitors health, and when a failure occurs, Nagios automatically triggers an Ansible recovery playbook to restore the service without human intervention."

### Q2: Why separate Terraform and Ansible instead of doing everything in one tool?
> **Answer:** "This follows the industry standard separation of concerns:
> - **Terraform** is an **Infrastructure as Code (IaC)** tool: it excels at declarative cloud provisioning (VPC, subnets, security groups, EC2 instances).
> - **Ansible** is a **Configuration Management (CM)** tool: it is agentless over SSH and excels at OS-level package installation, configuring systemd daemons, file templating, and executing recovery workflows."

---

## 2. Terraform (Infrastructure as Code)

### Q3: Walk me through your Terraform architecture. What resources does it create?
> **Answer:** "Inside [`terraform/`](../terraform), it creates:
> 1. A dedicated **AWS VPC** (`10.0.0.0/16`) with an **Internet Gateway** and public subnet (`10.0.1.0/24`).
> 2. Two **Security Groups**: `monitor-sg` for the Nagios server and `app-sg` for the application server.
> 3. An **AWS Key Pair** registered from our project-contained public key (`keys/id_rsa.pub`).
> 4. Two **EC2 Ubuntu 22.04 LTS Instances**: `monitor-server` (20GB root volume) and `app-server` (10GB root volume), both within the AWS Free Tier limit (30GB total).
> 5. **Outputs** that automatically supply instance IPs to our Ansible inventory."

### Q4: How did you design security groups between the two servers?
> **Answer:** "Using the principle of least privilege:
> - On **`monitor-sg`**: SSH (port 22) and Nagios Web (port 80) are restricted only to the administrator's IP.
> - On **`app-sg`**: Public HTTP (port 80) is open to the internet for the application, but **NRPE (port 5666)** and internal SSH recovery are restricted strictly to `monitor-sg`'s security group ID. This means no external entity on the internet can probe NRPE."

### Q5: What is `.terraform.lock.hcl` and why is it committed to GitHub?
> **Answer:** "The lock file records the exact version and cryptographic checksums of the provider plugins (`hashicorp/aws v5.x`). Committing it guarantees that anyone cloning the repository downloads the exact same provider binary, ensuring build reproducibility."

---

## 3. Ansible (Configuration Management)

### Q6: How does Ansible communicate with the servers? Is an agent required?
> **Answer:** "Ansible is completely **agentless**. It communicates securely over standard SSH using the private key located in [`keys/id_rsa`](../keys/id_rsa) and executes Python modules directly on the target machine."

### Q7: What is idempotency and how does your Ansible code demonstrate it?
> **Answer:** "Idempotency means running the same playbook multiple times produces the exact same result without unintended changes or duplicate side effects. In our roles, we use declarative modules like `apt`, `systemd`, `template`, and `file` rather than raw shell commands. If Nginx is already installed and running, Ansible reports `ok: [app-server]` with 0 changed tasks."

### Q8: What are handlers and why did you use them?
> **Answer:** "Handlers only run when a task reports a change (`notify`). For example, when Nginx configuration templates change, the handler triggers `nginx -t` to validate syntax and reloads Nginx. We also use `meta: flush_handlers` so the service reloads immediately before our health verification tasks execute."

---

## 4. Web & Backend Architecture (Nginx + Gunicorn + Flask)

### Q9: Why not run Flask directly to the internet using `app.run()`?
> **Answer:** "Flask's built-in development server is single-threaded, not optimized for concurrent connections, and lacks security hardening. In production:
> - **Gunicorn** is a pre-fork WSGI server that manages multiple worker processes and handles request concurrency.
> - **Nginx** is a high-performance reverse proxy that handles public HTTP connections, buffers slow clients, serves static frontend files, and proxies API requests to Gunicorn."

### Q10: Why does Gunicorn listen on `127.0.0.1:8000` instead of `0.0.0.0:8000`?
> **Answer:** "For network security isolation. By binding strictly to the loopback interface (`127.0.0.1`), Gunicorn is physically inaccessible from the outside internet. All traffic must pass through Nginx, where headers and security filtering can be applied."

### Q11: How do you verify Nginx health separately from Python backend health?
> **Answer:** "In our Nginx config ([`flask-app.conf.j2`](../ansible/roles/nginx/templates/flask-app.conf.j2)), we created a native location block `/nginx-health` that directly returns `200 "nginx-ok"` without forwarding to Python. This allows Nagios to distinctly differentiate between a web server failure and a Python backend crash."

---

## 5. Nagios Core & Self-Healing Automation (The Star Feature)

### Q12: What is the difference between a SOFT and HARD state in Nagios?
> **Answer:** "This is the most critical distinction in our monitoring logic:
> - **SOFT state**: When a check fails the first time (attempt 1 of 3), it is a temporary glitch. Nagios does not trigger recovery.
> - **HARD state**: When the service fails consecutively for `max_check_attempts` (attempt 3 of 3), Nagios confirms it is a persistent failure and transitions to `HARD CRITICAL`.
> Our self-healing handler **only** executes when `$SERVICESTATETYPE$ == HARD` to prevent premature recovery loops during transient network blips."

### Q13: How does Nagios trigger Ansible?
> **Answer:** "In Nagios command definitions, we configure an **Event Handler** command:
> ```text
> event_handler recover_flask_event_handler
> ```
> When the service enters `HARD CRITICAL`, Nagios executes our wrapper script:
> `/usr/local/bin/recover_flask.sh "$SERVICESTATE$" "$SERVICESTATETYPE$" "$SERVICEATTEMPT$"`
> This script checks the state, verifies safety locks, and invokes:
> `ansible-playbook -i /opt/self-healing/inventory/hosts.ini /opt/self-healing/playbooks/recover_flask.yml`
> over the private VPC network to restart `flask-backend.service`."

### Q14: What safety mechanisms prevent self-healing from causing a disaster?
> **Answer:** "We implemented 4 defensive engineering controls:
> 1. **Concurrency Lock (`flock`)**: Uses Linux file locking on `/var/run/recover_flask.lock` so duplicate check threads cannot launch concurrent playbooks.
> 2. **Cooldown Period (60s)**: If a recovery ran within the last 60 seconds, it skips execution to avoid restart thrashing if code is broken.
> 3. **Syntax Validation (`nginx -t`)**: In Nginx recovery, it checks configuration syntax before restarting. If syntax is invalid, it safely aborts and keeps the alert visible so administrators are notified.
> 4. **Restricted Sudoers**: In `/etc/sudoers.d/nagios_recovery`, the `nagios` user is granted passwordless execution **strictly** for `/usr/local/bin/recover_*.sh`, with zero arbitrary command execution."

### Q15: What happens if the EC2 instance itself is DOWN?
> **Answer:** "Nagios uses host-service dependencies. If the host check (`check-host-alive` via ICMP ping) fails, Nagios marks the host as DOWN and automatically **suppresses** all service-level event handlers. It does not waste resources repeatedly sending SSH restart commands to an unreachable server."
