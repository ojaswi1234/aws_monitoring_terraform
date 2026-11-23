# Python Flask Backend — DevOps Self-Healing Application

## Overview
This is the core Python backend component for the automated DevOps infrastructure project. It is structured as a production-ready REST API using the Flask application factory pattern (`create_app()`), served via **Gunicorn** WSGI application server, and exposed through an **Nginx** reverse proxy.

## Directory Structure
```text
backend/
├── app/
│   ├── __init__.py            # Flask application factory (create_app)
│   ├── config.py              # Environment configuration classes
│   ├── routes/
│   │   ├── __init__.py        # Blueprint exports
│   │   ├── health.py          # /healthz (liveness) & /readyz (readiness)
│   │   ├── status.py          # /api/v1/status
│   │   └── info.py            # / (landing), /api/v1/info, /api/v1/metrics
│   └── services/
│       ├── __init__.py
│       └── metrics_tracker.py # In-memory metrics & uptime tracker
├── tests/
│   ├── conftest.py            # Pytest test client fixtures
│   ├── test_health.py         # Liveness and readiness tests
│   ├── test_status.py         # Status and uptime tests
│   └── test_info.py           # Info, metrics, and error handling tests
├── requirements.txt           # Python package dependencies
└── wsgi.py                    # Gunicorn entrypoint module
```

## API Endpoints

| Method | Endpoint | Description | Expected Status |
|---|---|---|---|
| `GET` | `/` | Application landing summary | 200 OK |
| `GET` | `/healthz` | Liveness probe (monitored by Nagios) | 200 OK |
| `GET` | `/readyz` | Readiness probe (dependency & config check) | 200 OK / 503 |
| `GET` | `/api/v1/status` | Application status, version, and uptime | 200 OK |
| `GET` | `/api/v1/info` | Non-sensitive runtime and architecture info | 200 OK |
| `GET` | `/api/v1/metrics` | Safe operational metrics (uptime, request count)| 200 OK |

## Local Testing
Run pytest from the `backend/` directory:
```bash
python3 -m pytest -v
```

## Running with Gunicorn Locally
```bash
gunicorn --bind 127.0.0.1:8000 wsgi:app
```
