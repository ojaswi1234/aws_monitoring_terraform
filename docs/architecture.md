# System Architecture & Technical Specifications

## High-Level Architectural Overview

This project implements an automated, production-grade cloud infrastructure supporting a Python REST backend, reverse-proxied by Nginx, monitored continuously by Nagios Core, and restored autonomously via Ansible event-driven self-healing.

```mermaid
flowchart TD
    subgraph Internet ["Public Internet / Administrator"]
        Admin["Administrator / User Browser"]
    end

    subgraph AWS ["AWS Cloud: Dedicated VPC (10.0.0.0/16)"]
        subgraph Subnet ["Public Subnet (10.0.1.0/24)"]
            subgraph MonitorNode ["Server 1: Monitoring Server (monitor-server)"]
                Nagios["Nagios Core 4.x Engine"]
                NagiosWeb["Apache HTTP / Nagios Dashboard (:80)"]
                Handler["Restricted Recovery Wrapper (/usr/local/bin/recover_*.sh)"]
                AnsibleRec["Ansible Playbook Engine (/opt/self-healing)"]
            end

            subgraph AppNode ["Server 2: Application Server (app-server)"]
                Nginx["Nginx Reverse Proxy (:80)"]
                Gunicorn["Gunicorn WSGI Server (127.0.0.1:8000)"]
                Flask["Python Flask Application"]
                NRPE["NRPE Daemon (:5666)"]
            end
        end
    end

    Admin -->|SSH :22 / HTTP :80| NagiosWeb
    Admin -->|HTTP :80| Nginx
    Nagios -->|HTTP Check /healthz & /readyz| Nginx
    Nagios -->|NRPE Remote System Probes :5666| NRPE
    Nginx -->|Reverse Proxy /api/* & /healthz| Gunicorn
    Gunicorn -->|WSGI In-Process| Flask

    Nagios -.->|On HARD CRITICAL| Handler
    Handler -->|Trigger Playbook| AnsibleRec
    AnsibleRec -.->|SSH Private VPC Connection :22| AppNode
```

## Network & Security Group Mapping

| Security Group | Ingress Port | Protocol | Source | Purpose |
|---|---|---|---|---|
| `monitor-sg` | `22` | TCP | `admin_ip` | Secure SSH administrative access |
| `monitor-sg` | `80` | TCP | `admin_ip` | Nagios Core Web UI access |
| `monitor-sg` | ICMP | Echo | `admin_ip` | Ping verification |
| `app-sg` | `22` | TCP | `admin_ip` & `monitor-sg` | SSH admin access and Ansible self-healing SSH |
| `app-sg` | `80` | TCP | `0.0.0.0/0` | Public application demonstration & Nginx entry |
| `app-sg` | `5666` | TCP | `monitor-sg` strictly | NRPE host resource monitoring |
| `app-sg` | ICMP | Echo | `monitor-sg` strictly | Nagios host alive ping |

## Request Flow
```mermaid
sequenceDiagram
    autonumber
    actor Client as User / Nagios Check
    participant Nginx as Nginx (:80)
    participant Gunicorn as Gunicorn (127.0.0.1:8000)
    participant Flask as Flask REST API

    Client->>Nginx: GET /healthz
    Note over Nginx: Proxies request via 127.0.0.1:8000
    Nginx->>Gunicorn: Forward request
    Gunicorn->>Flask: Invoke WSGI Application Factory
    Flask-->>Gunicorn: Return 200 OK {"status": "ok"}
    Gunicorn-->>Nginx: HTTP 200 JSON Response
    Nginx-->>Client: HTTP 200 OK
```
