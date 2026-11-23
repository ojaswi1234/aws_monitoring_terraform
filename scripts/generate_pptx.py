#!/usr/bin/env python3
"""
generate_pptx.py
Generates an elegant, high-impact, professional presentation (.pptx)
for the DevOps Automated Infrastructure & Self-Healing Project.
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==========================================
# Color Palette Definition (Modern Dark Slate)
# ==========================================
BG_COLOR       = RGBColor(15, 23, 42)    # #0F172A - Deep Navy/Slate
CARD_BG        = RGBColor(30, 41, 59)   # #1E293B - Card Dark Navy
CARD_BORDER    = RGBColor(51, 65, 85)   # #334155 - Subtle Border
ACCENT_BLUE    = RGBColor(56, 189, 248) # #38BDF8 - Sky Blue / Cyan
ACCENT_CYAN    = RGBColor(14, 165, 233) # #0EA5E9 - Bright Blue
ACCENT_GREEN   = RGBColor(34, 197, 94)  # #22C55E - Emerald / Restored
ACCENT_AMBER   = RGBColor(245, 158, 11) # #F59E0B - Warning / Alert
TEXT_PRIMARY   = RGBColor(248, 250, 252)# #F8FAFC - Bright Off-White
TEXT_MUTED     = RGBColor(148, 163, 184)# #94A3B8 - Slate Light Gray
CODE_BG        = RGBColor(10, 15, 28)   # #0A0F1C - Deep Code Editor Dark

FONT_HEADING = "Helvetica"
FONT_BODY    = "Segoe UI"
FONT_CODE    = "Consolas"

def create_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.color.rgb = BG_COLOR
        return bg

    def add_header(slide, title, category="AUTOMATED DEVOPS INFRASTRUCTURE & SELF-HEALING"):
        # Category tracker badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        # Main slide title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_PRIMARY

    def add_card(slide, left, top, width, height, title, bullets, badge=None, badge_color=ACCENT_BLUE):
        # Card Background Shape
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Card Content Box
        pad = Inches(0.28)
        content_box = slide.shapes.add_textbox(left + pad, top + pad, width - (pad * 2), height - (pad * 2))
        tf = content_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Optional Badge
        if badge:
            p_b = tf.paragraphs[0]
            p_b.text = f"● {badge.upper()}"
            p_b.font.name = FONT_HEADING
            p_b.font.size = Pt(9)
            p_b.font.bold = True
            p_b.font.color.rgb = badge_color
            p_b.space_after = Pt(4)
            p_title = tf.add_paragraph()
        else:
            p_title = tf.paragraphs[0]

        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = ACCENT_BLUE
        p_title.space_after = Pt(12)

        for b in bullets:
            p = tf.add_paragraph()
            p.space_after = Pt(8)
            p.font.name = FONT_BODY
            p.font.size = Pt(12)
            
            # Format label vs detail if colon exists
            if ":" in b:
                parts = b.split(":", 1)
                run1 = p.add_run()
                run1.text = "• " + parts[0] + ":"
                run1.font.bold = True
                run1.font.color.rgb = TEXT_PRIMARY
                run2 = p.add_run()
                run2.text = parts[1]
                run2.font.color.rgb = TEXT_MUTED
            else:
                run = p.add_run()
                run.text = "• " + b
                run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative glow rectangle
    glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(4.8))
    glow.fill.solid()
    glow.fill.fore_color.rgb = ACCENT_BLUE
    glow.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.2), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_super = tf1.paragraphs[0]
    p_super.text = "ENTERPRISE DEVOPS & INFRASTRUCTURE AUTOMATION"
    p_super.font.name = FONT_HEADING
    p_super.font.size = Pt(13)
    p_super.font.bold = True
    p_super.font.color.rgb = ACCENT_BLUE
    p_super.space_after = Pt(14)

    p_main = tf1.add_paragraph()
    p_main.text = "Automated Cloud Infrastructure,\nPython Monitoring & Self-Healing System"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(38)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_PRIMARY
    p_main.space_after = Pt(20)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Closed-loop failure detection and autonomous recovery integrating Terraform, Ansible, Nginx, Gunicorn, Flask REST API & Nagios Core 4.x"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_after = Pt(36)

    p_tech = tf1.add_paragraph()
    p_tech.text = "Stack: Terraform | Ansible | Nagios Core | Python Flask | Gunicorn WSGI | Nginx | AWS EC2 (Ubuntu 22.04 LTS)"
    p_tech.font.name = FONT_CODE
    p_tech.font.size = Pt(12)
    p_tech.font.color.rgb = ACCENT_GREEN

    # ==========================================
    # SLIDE 2: Problem Statement & Motivation
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement: The Operational Gap in DevOps", "Context & Industry Motivation")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Passive Monitoring",
             [
                 "Traditional Alert Fatigue: Monitoring tools send endless emails/pages requiring humans to wake up.",
                 "High MTTR (Mean Time to Recover): Critical services remain down while on-call engineers triage.",
                 "Manual Runbooks: Operators execute repetitive restart scripts, introducing human error.",
                 "No Closed-Loop: Monitoring remains completely disconnected from orchestration."
             ], badge="The Bottleneck", badge_color=ACCENT_AMBER)

    add_card(s2, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Configuration Drift",
             [
                 "Snowflake Servers: Manually modified production systems that cannot be reliably reproduced.",
                 "Fragile Dependencies: Python applications crashing due to unmanaged environment paths.",
                 "Security Gaps: Unrestricted root permissions and unmanaged sudo access across servers.",
                 "Slow Provisioning: Hours spent configuring packages, users, and web reverse proxies."
             ], badge="Infrastructure Risk", badge_color=ACCENT_AMBER)

    add_card(s2, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "The Solution Paradigm",
             [
                 "Zero-Touch IaC: Reproducible cloud infrastructure provisioned in seconds via Terraform.",
                 "Automated CM: Ansible handles all system configuration, dependencies, and WSGI.",
                 "Automated Self-Healing: Nagios detects failures and triggers targeted Ansible playbooks.",
                 "Guaranteed Safety: Concurrency locks, cooldown timers, and pre-restart syntax checks."
             ], badge="Proposed Solution", badge_color=ACCENT_GREEN)

    # ==========================================
    # SLIDE 3: Key Project Objectives
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Engineering Objectives & Success Criteria", "Project Scope")

    cards_data = [
        ("1. Reproducible Cloud IaC", [
            "AWS VPC Architecture: Dedicated VPC, subnet, gateway, route tables.",
            "Least-Privilege Security: Strict security group boundaries between servers.",
            "Dynamic Automation: Terraform outputs feed directly into Ansible."
        ]),
        ("2. Production WSGI Backend", [
            "Factory Architecture: Clean Flask application factory (create_app).",
            "Gunicorn WSGI: Local socket/port binding isolated from public internet.",
            "Nginx Reverse Proxy: Single public entry point handling static + APIs."
        ]),
        ("3. Continuous Multi-Layer Probes", [
            "Nagios Core 4.x: Real-time checks for hosts, HTTP, and system load.",
            "Granular Endpoints: /healthz liveness and /readyz readiness checks.",
            "NRPE Remote Probes: System resource utilization without root exposure."
        ]),
        ("4. Autonomous Self-Healing", [
            "Event-Driven Integration: Nagios event handlers invoke Ansible playbooks.",
            "Controlled Execution: File locking (flock) prevents race conditions.",
            "Verified Recovery: Nagios verifies service health before returning to OK."
        ])
    ]

    for idx, (title, bullets) in enumerate(cards_data):
        row = idx // 2
        col = idx % 2
        c_left = Inches(0.8 + col * 6.0)
        c_top = Inches(1.6 + row * 2.7)
        add_card(s3, c_left, c_top, Inches(5.7), Inches(2.5), title, bullets)

    # ==========================================
    # SLIDE 4: High-Level Architecture
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Two-Node Cloud System Architecture", "System Design & Networking")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Server 1: Monitoring Server",
             [
                 "Hostname & OS: monitor-server (Ubuntu 22.04 LTS).",
                 "Nagios Core 4.x: Core monitoring daemon evaluating check intervals.",
                 "Apache Web Server: Hosts the secure Nagios operational web console.",
                 "Recovery Handler: Restricted shell wrapper (/usr/local/bin/recover_*.sh).",
                 "Ansible Engine: Local playbooks triggered over private VPC network.",
                 "Security Ingress: SSH & HTTP restricted exclusively to Administrator IP."
             ], badge="Orchestrator Node", badge_color=ACCENT_BLUE)

    add_card(s4, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Server 2: Application Server",
             [
                 "Hostname & OS: app-server (Ubuntu 22.04 LTS).",
                 "Nginx Reverse Proxy: Port 80 public entry point for static & API traffic.",
                 "Gunicorn WSGI: Production server bound locally to 127.0.0.1:8000.",
                 "Python Flask App: REST APIs, liveness (/healthz), and readiness (/readyz).",
                 "NRPE Daemon: Port 5666 remote agent locked strictly to monitor-server.",
                 "systemd Supervised: Managed as flask-backend.service with auto-restart."
             ], badge="Workload Node", badge_color=ACCENT_GREEN)

    # ==========================================
    # SLIDE 5: Infrastructure as Code (Terraform)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Infrastructure as Code (IaC) via Terraform", "Automated Cloud Provisioning")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Cloud Networking",
             [
                 "Dedicated VPC: 10.0.0.0/16 with DNS hostnames and resolution enabled.",
                 "Public Subnet: 10.0.1.0/24 mapped to availability zones automatically.",
                 "Internet Gateway: Attached to VPC with default route in public route table.",
                 "Isolated Subnets: Internal VPC traffic travels over high-speed private IPs."
             ], badge="VPC & Routing")

    add_card(s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Security Group Rules",
             [
                 "monitor-sg (Ingress): TCP 22 & TCP 80 locked strictly to admin CIDR.",
                 "app-sg (Ingress): TCP 80 open to public; TCP 22 open to admin & monitor-sg.",
                 "NRPE Protection: TCP 5666 restricted strictly to monitor-sg security ID.",
                 "Stateful Filtering: Full outbound access for package repositories."
             ], badge="Network Security")

    add_card(s5, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Compute & Outputs",
             [
                 "Canonical Ubuntu AMI: Dynamic lookup for latest 22.04 LTS Jammy image.",
                 "Free-Tier Storage: Encrypted gp3 root volumes (20GB + 10GB = 30GB total).",
                 "SSH Key Deployment: Automatically registers admin public key in AWS.",
                 "Dynamic Inventory: Generates Ansible hosts.ini with internal/public IPs."
             ], badge="EC2 & Inventory")

    # ==========================================
    # SLIDE 6: Configuration Management (Ansible)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Automated Server Configuration via Ansible", "Configuration Management")

    roles = [
        ("common", [
            "Apt cache update and foundational packages (curl, git, htop, net-tools).",
            "Configures systemd-timesyncd for microsecond clock synchronization."
        ]),
        ("python_backend", [
            "Creates dedicated unprivileged flaskapp system user and isolated virtualenv.",
            "Deploys application source code and installs version-pinned requirements.",
            "Creates and manages flask-backend.service systemd unit with hardening flags."
        ]),
        ("nginx", [
            "Installs Nginx, removes default config, and deploys reverse proxy template.",
            "Configures /nginx-health probe, header forwarding, and static doc root.",
            "Runs automated syntax checks (nginx -t) before reloading service."
        ]),
        ("nagios & recovery", [
            "Installs Nagios 4.x, CGI binaries, Apache web UI, and monitoring plugins.",
            "Enables event handlers (enable_event_handlers=1) and deploys host configs.",
            "Deploys recovery playbooks, wrapper scripts, and restricted sudoers rules."
        ])
    ]

    for idx, (title, bullets) in enumerate(roles):
        row = idx // 2
        col = idx % 2
        c_left = Inches(0.8 + col * 6.0)
        c_top = Inches(1.6 + row * 2.7)
        add_card(s6, c_left, c_top, Inches(5.7), Inches(2.5), f"Role: {title}", bullets, badge="Ansible Role")

    # ==========================================
    # SLIDE 7: Python Backend & Gunicorn Architecture
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Production Python REST API & WSGI Server", "Backend Architecture")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Flask REST API Implementation",
             [
                 "Application Factory: Clean create_app() pattern separating config and routes.",
                 "GET /healthz: Liveness probe confirming process execution (Nagios target).",
                 "GET /readyz: Readiness probe ensuring configs and runtime are operational.",
                 "GET /api/v1/status: Reports application state, version, and live uptime.",
                 "GET /api/v1/info: Safe environment metadata (no secrets, IPs or keys).",
                 "GET /api/v1/metrics: Real-time uptime and total request telemetry.",
                 "Automated Pytest: 7 comprehensive unit tests passing with 100% success."
             ], badge="Flask REST Backend", badge_color=ACCENT_BLUE)

    add_card(s7, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Gunicorn WSGI & systemd Supervision",
             [
                 "Production WSGI: Multi-worker process model avoiding Flask dev server.",
                 "Local Binding: Listens exclusively on 127.0.0.1:8000 (never public).",
                 "Isolated Environment: Executes inside /opt/flask-backend/venv.",
                 "Dedicated Service User: Runs under non-root user flaskapp.",
                 "Hardened systemd Unit: ProtectSystem=full and PrivateTmp=true enabled.",
                 "Auto-Restart on Crash: Restart=on-failure with 3-second restart delay.",
                 "Systemd Journal: Structured stdout/stderr logging streamed to journald."
             ], badge="Gunicorn WSGI Server", badge_color=ACCENT_GREEN)

    # ==========================================
    # SLIDE 8: Nginx Web Server & Reverse Proxy
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Nginx Reverse Proxy & Traffic Routing", "Web Server Architecture")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Reverse Proxy Routing Logic",
             [
                 "Public HTTP Entry (:80): Public interface receiving all inbound requests.",
                 "API Forwarding: location /api/ passes requests to 127.0.0.1:8000.",
                 "Probe Forwarding: location /healthz and /readyz routed directly to Flask.",
                 "Native Nginx Probe: location /nginx-health returns HTTP 200 text/plain.",
                 "Distinct Verification: Isolates Nginx web server health from backend health.",
                 "Static UI Hosting: Serves real-time frontend dashboard at / from /var/www/html."
             ], badge="Traffic Management", badge_color=ACCENT_BLUE)

    add_card(s8, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Security & Performance Optimization",
             [
                 "Header Sanitization: Passes Host, X-Real-IP, and X-Forwarded-Proto.",
                 "Audit Tracking: Preserves client IP addresses through X-Forwarded-For.",
                 "Upstream Timeouts: Strict proxy_connect_timeout (5s) and read timeout (15s).",
                 "Graceful Failovers: Custom 502/503/504 error handler routing.",
                 "Pre-Flight Validation: nginx -t runs automatically before any reload.",
                 "Zero Unhandled Crash: Invalid syntax halts deployment safely."
             ], badge="Proxy Hardening", badge_color=ACCENT_GREEN)

    # ==========================================
    # SLIDE 9: Infrastructure & Application Monitoring
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Continuous Monitoring via Nagios Core 4.x", "Proactive Observability")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Host Level Checks",
             [
                 "check-host-alive: ICMP echo ping to verify EC2 instance network state.",
                 "check_ssh: Confirms SSH daemon responsiveness on port 22.",
                 "Host Failure Isolation: If host is DOWN, service restart scripts are suppressed.",
                 "No False Recoveries: Prevents firing restart commands into an unreachable host."
             ], badge="Host Layer")

    add_card(s9, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Service Level Checks",
             [
                 "Nginx Health: check_http against /nginx-health for web layer uptime.",
                 "Flask Liveness: check_http against /healthz verifying backend process.",
                 "Flask Readiness: check_http against /readyz ensuring service dependency.",
                 "Check Thresholds: 1-minute regular intervals, 1-minute retry cycles."
             ], badge="Application Layer")

    add_card(s9, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "NRPE System Metrics",
             [
                 "Root Disk Usage: check_disk warns at 20% free, critical at 10% free.",
                 "System CPU Load: check_load monitors 1, 5, and 15-minute load averages.",
                 "Daemon Counts: check_procs ensures active Gunicorn and Nginx worker pools.",
                 "Port 5666 Restricted: Only accessible by Nagios server's private IP."
             ], badge="Resource Layer")

    # ==========================================
    # SLIDE 10: The Self-Healing Engine (Nagios + Ansible)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Closed-Loop Event-Driven Self-Healing Engine", "Automated Remediation")

    steps = [
        ("Step 1: Failure Detection", [
            "Flask process crashes or is stopped.",
            "Nagios probe fails -> enters SOFT state.",
            "Consecutive retries transition service to HARD CRITICAL."
        ]),
        ("Step 2: Event Handler Dispatch", [
            "Nagios fires /usr/local/bin/recover_flask.sh.",
            "Passes $SERVICESTATE$, $SERVICESTATETYPE$, $SERVICEATTEMPT$.",
            "Handler ignores SOFT states; acts exclusively on HARD CRITICAL."
        ]),
        ("Step 3: Playbook Execution", [
            "Handler acquires non-blocking file lock (flock).",
            "Verifies 60s cooldown timer has elapsed.",
            "Invokes Ansible recover_flask.yml over internal VPC SSH."
        ]),
        ("Step 4: Verification & Restoration", [
            "Ansible restarts systemd service & probes 127.0.0.1:8000/healthz.",
            "Next scheduled Nagios check returns HTTP 200 OK.",
            "Nagios marks service OK; resets state with zero human intervention."
        ])
    ]

    for idx, (title, bullets) in enumerate(steps):
        row = idx // 2
        col = idx % 2
        c_left = Inches(0.8 + col * 6.0)
        c_top = Inches(1.6 + row * 2.7)
        add_card(s10, c_left, c_top, Inches(5.7), Inches(2.5), title, bullets, badge=f"Phase {idx+1}", badge_color=ACCENT_CYAN)

    # ==========================================
    # SLIDE 11: Safety Controls & Defensive Design
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Defensive Engineering & Safety Controls", "Reliability & Integrity")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Concurrency & Cooldown",
             [
                 "Non-Blocking flock: flock -n /var/run/recover_*.lock guarantees single execution.",
                 "Prevents Race Conditions: Parallel check threads cannot launch concurrent recoveries.",
                 "Enforced Cooldown: 60-second cooldown window prevents restart thrashing.",
                 "Audit Logging: All attempts logged to /var/log/nagios_recovery.log."
             ], badge="Execution Control")

    add_card(s11, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Configuration Validation",
             [
                 "Syntax Pre-Flight: recover_nginx.yml always executes nginx -t first.",
                 "Safe Failure Abort: If configuration is invalid, restart is aborted immediately.",
                 "Preserves Alert State: Service remains in CRITICAL; alert sent to operator.",
                 "Zero Masking: System never hides human configuration mistakes."
             ], badge="Syntax Protection")

    add_card(s11, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Privilege Boundaries",
             [
                 "Restricted Sudoers: nagios ALL=(ALL) NOPASSWD only for exact wrapper binaries.",
                 "Zero Arbitrary Input: Handlers do not accept shell commands from arguments.",
                 "Dedicated Users: nagios user runs monitoring; flaskapp user runs backend.",
                 "Private VPC Networking: SSH commands pass strictly through internal subnets."
             ], badge="Least Privilege")

    # ==========================================
    # SLIDE 12: Failure Simulation & Testing Results
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Interactive Failure Simulation & Validation Results", "Verification & Testing")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Test 1: Flask Backend Crash",
             [
                 "Action: systemctl stop flask-backend.",
                 "Detection: Nagios check on /healthz transitions to CRITICAL.",
                 "Recovery: recover_flask.sh triggers Ansible recover_flask.yml.",
                 "Outcome: Service restarted and verified in <60 seconds. Restored to OK."
             ], badge="Backend Test", badge_color=ACCENT_GREEN)

    add_card(s12, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Test 2: Nginx Web Server Down",
             [
                 "Action: systemctl stop nginx.",
                 "Detection: Nagios check on /nginx-health reports CRITICAL.",
                 "Recovery: recover_nginx.sh validates syntax and restarts Nginx.",
                 "Outcome: Reverse proxy restored; traffic resumed to backend seamlessly."
             ], badge="Web Server Test", badge_color=ACCENT_GREEN)

    add_card(s12, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "Test 3: Corrupt Nginx Syntax",
             [
                 "Action: Injected invalid configuration error into Nginx.",
                 "Validation: nginx -t syntax validation catches corrupt config.",
                 "Safety: Ansible playbook aborts safely without restarting.",
                 "Outcome: Service remains CRITICAL; failure logged clearly."
             ], badge="Safety Guard Test", badge_color=ACCENT_AMBER)

    # ==========================================
    # SLIDE 13: Security & Cost Architecture
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Security Hardening & Cloud Cost Optimization", "Governance & Economics")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Cloud Cost Engineering (AWS Free Tier)",
             [
                 "Instance Selection: t2.micro / t3.micro (750 free compute hours/month).",
                 "Storage Allocation: 20GB (Monitor) + 10GB (App) = 30GB total EBS (within free tier).",
                 "Zero Expensive Add-ons: No NAT Gateways, Elastic Load Balancers, or managed DBs.",
                 "Reproducible Destruction: ./scripts/destroy.sh removes 100% of cloud resources.",
                 "Zero Dormant Charges: Prevents orphaned IPs and leftover EBS snapshots."
             ], badge="Cost Optimization", badge_color=ACCENT_GREEN)

    add_card(s13, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Enterprise Security Architecture",
             [
                 "Credential Sanitization: No AWS keys or private SSH keys committed to Git.",
                 "Strict Ingress Control: Nagios UI and SSH restricted to administrator IP.",
                 "Internal Communication: Monitoring and recovery traffic runs on private IPs.",
                 "Gunicorn Isolation: Internal loopback binding prevents direct public access.",
                 "Safe API Responses: /api/v1/info discloses no internal passwords or paths."
             ], badge="Security Governance", badge_color=ACCENT_BLUE)

    # ==========================================
    # SLIDE 14: Conclusion & Key Learnings
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Conclusion & Project Summary", "Key Takeaways & Viva Readiness")

    add_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Summary of Accomplishments",
             [
                 "Complete Pipeline: Built an integrated system connecting IaC, CM, WSGI, and monitoring.",
                 "Real Backend Application: Modular Flask API with factory design and full pytest test suite.",
                 "Closed-Loop DevOps: Successfully bridged passive Nagios monitoring with active Ansible self-healing.",
                 "Defensive Engineering: Implemented concurrency locks, cooldown timers, and pre-restart checks.",
                 "GitHub Ready: Comprehensive documentation, Mermaid diagrams, and one-click validation."
             ], badge="Core Takeaways", badge_color=ACCENT_GREEN)

    add_card(s14, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Technical Competencies Demonstrated",
             [
                 "Terraform: State management, HCL, dynamic data lookups, provider lock files.",
                 "Ansible: Role modularity, idempotency, systemd templates, handler flushing.",
                 "Linux Administration: Systemd units, file locks (flock), sudoers boundaries.",
                 "Python & WSGI: Flask application factory, WSGI multi-worker routing, pytest fixtures.",
                 "Observability: Nagios Core 4.x, event handlers, NRPE agents, exit code semantics."
             ], badge="DevOps Skills", badge_color=ACCENT_BLUE)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully saved to {output_path}")

if __name__ == "__main__":
    out_file = "/home/ob/devops-self-healing-project/DevOps_Self_Healing_Infrastructure.pptx"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    create_presentation(out_file)
