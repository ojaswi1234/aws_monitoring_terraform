#!/usr/bin/env python3
"""
generate_enhanced_pptx.py
Generates a comprehensive, highly visual, elegant PowerPoint presentation (.pptx)
for the Automated DevOps Infrastructure & Closed-Loop Self-Healing System.
Features:
- Student metadata (Ojaswi Bhardwaj, Reg: 12319444, Roll: 55, Sec: K302316) & Faculty Guide (Rakesh Gaganeja)
- Visual Toolchain Integration & Synergy Map
- Interactive Flowchart showing Step-by-Step Work & Data Flow
- Cloud Topology Architecture
- Real Code Snippets for all key tools (Terraform, Ansible, Flask, Nginx, Nagios, Event Handler)
- Defensive Engineering & Safety Controls
- Real System Screenshots (Nagios Core 4.4.6, Web Console, Ansible Trace)
- Empirical Benchmarks & MTTR Evaluation Table
- GitHub Repository link and academic conclusion
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# Color Palette Definition (Modern Executive Dark Slate Theme)
# ==============================================================================
BG_COLOR       = RGBColor(15, 23, 42)      # #0F172A - Deep Slate Background
CARD_BG        = RGBColor(30, 41, 59)     # #1E293B - Card Background
CARD_BORDER    = RGBColor(51, 65, 85)     # #334155 - Subtle Border
CARD_LIGHT_BG  = RGBColor(51, 65, 85)     # #334155 - Highlighted Card
CODE_BG        = RGBColor(10, 15, 28)     # #0A0F1C - Code Editor Dark Box
CODE_HEADER_BG = RGBColor(20, 30, 50)     # #141E32 - Code Header Bar

ACCENT_BLUE    = RGBColor(56, 189, 248)   # #38BDF8 - Sky Blue / IaC
ACCENT_CYAN    = RGBColor(14, 165, 233)   # #0EA5E9 - Bright Cyan
ACCENT_GREEN   = RGBColor(34, 197, 94)    # #22C55E - Emerald / Recovery / OK
ACCENT_AMBER   = RGBColor(245, 158, 11)   # #F59E0B - Warning / Alert
ACCENT_RED     = RGBColor(239, 68, 68)    # #EF4444 - Failure / Critical
ACCENT_PURPLE  = RGBColor(168, 85, 247)   # #A855F7 - Automation / Ansible

TEXT_PRIMARY   = RGBColor(248, 250, 252)  # #F8FAFC - Off-white
TEXT_MUTED     = RGBColor(148, 163, 184)  # #94A3B8 - Slate Gray
TEXT_CODE      = RGBColor(226, 232, 240)  # #E2E8F0 - Monospace Code Text
TEXT_CODE_KEY  = RGBColor(56, 189, 248)   # #38BDF8 - Monospace Keywords
TEXT_CODE_STR  = RGBColor(74, 222, 128)   # #4ADE80 - Monospace Strings
TEXT_CODE_COM  = RGBColor(100, 116, 139)  # #64748B - Monospace Comments

FONT_HEADING = "Helvetica"
FONT_BODY    = "Segoe UI"
FONT_CODE    = "Consolas"

PROJECT_DIR = "/home/ob/devops-self-healing-project"
ASSETS_DIR  = os.path.join(PROJECT_DIR, "report_assets")

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
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
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
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_PRIMARY

    def add_card(slide, left, top, width, height, title, bullets, badge=None, badge_color=ACCENT_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        pad = Inches(0.24)
        content_box = slide.shapes.add_textbox(left + pad, top + pad, width - (pad * 2), height - (pad * 2))
        tf = content_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if badge:
            p_b = tf.paragraphs[0]
            p_b.text = f"● {badge.upper()}"
            p_b.font.name = FONT_HEADING
            p_b.font.size = Pt(8.5)
            p_b.font.bold = True
            p_b.font.color.rgb = badge_color
            p_b.space_after = Pt(3)
            p_title = tf.add_paragraph()
        else:
            p_title = tf.paragraphs[0]

        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = ACCENT_BLUE
        p_title.space_after = Pt(8)

        for b in bullets:
            p = tf.add_paragraph()
            p.space_after = Pt(5)
            p.font.name = FONT_BODY
            p.font.size = Pt(10.5)

            if ":" in b:
                parts = b.split(":", 1)
                r1 = p.add_run()
                r1.text = "• " + parts[0] + ":"
                r1.font.bold = True
                r1.font.color.rgb = TEXT_PRIMARY
                r2 = p.add_run()
                r2.text = parts[1]
                r2.font.color.rgb = TEXT_MUTED
            else:
                r = p.add_run()
                r.text = "• " + b
                r.font.color.rgb = TEXT_MUTED

    def add_code_card(slide, left, top, width, height, filename, code_lines, lang="CODE"):
        # Outer Card
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CODE_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Header Bar
        hdr_h = Inches(0.42)
        hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, hdr_h)
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = CODE_HEADER_BG
        hdr.line.color.rgb = CARD_BORDER
        hdr.line.width = Pt(0.5)

        # Header Text (Dots + Filename + Lang Badge)
        tb_hdr = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.08), width - Inches(0.36), Inches(0.3))
        tf_h = tb_hdr.text_frame
        tf_h.margin_left = tf_h.margin_top = tf_h.margin_right = tf_h.margin_bottom = 0
        p_h = tf_h.paragraphs[0]
        
        r_dots = p_h.add_run()
        r_dots.text = "● ● ●  "
        r_dots.font.size = Pt(8)
        r_dots.font.color.rgb = ACCENT_AMBER
        
        r_fn = p_h.add_run()
        r_fn.text = f"{filename} "
        r_fn.font.name = FONT_CODE
        r_fn.font.bold = True
        r_fn.font.size = Pt(9.5)
        r_fn.font.color.rgb = TEXT_PRIMARY

        r_badge = p_h.add_run()
        r_badge.text = f"[{lang}]"
        r_badge.font.name = FONT_CODE
        r_badge.font.bold = True
        r_badge.font.size = Pt(8.5)
        r_badge.font.color.rgb = ACCENT_CYAN

        # Code Body
        body_box = slide.shapes.add_textbox(left + Inches(0.2), top + hdr_h + Inches(0.1), width - Inches(0.4), height - hdr_h - Inches(0.18))
        tf_b = body_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

        first = True
        for line in code_lines:
            p = tf_b.paragraphs[0] if first else tf_b.add_paragraph()
            first = False
            p.font.name = FONT_CODE
            p.font.size = Pt(8.5)
            p.space_after = Pt(1.5)

            # Simple intelligent syntax coloring
            sline = line.strip()
            if sline.startswith("#") or sline.startswith("//"):
                run = p.add_run()
                run.text = line
                run.font.color.rgb = TEXT_CODE_COM
            elif ":" in line and not sline.startswith("-"):
                k, v = line.split(":", 1)
                r1 = p.add_run()
                r1.text = k + ":"
                r1.font.bold = True
                r1.font.color.rgb = TEXT_CODE_KEY
                r2 = p.add_run()
                r2.text = v
                r2.font.color.rgb = TEXT_CODE_STR if any(c in v for c in ['"', "'", "http", "200"]) else TEXT_CODE
            else:
                run = p.add_run()
                run.text = line
                run.font.color.rgb = TEXT_CODE

    # ==========================================================================
    # SLIDE 1: Title Slide (with Student & Faculty Metadata)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative glow bar
    glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.1), Inches(0.12), Inches(5.3))
    glow.fill.solid()
    glow.fill.fore_color.rgb = ACCENT_BLUE
    glow.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.05), Inches(11.2), Inches(5.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_super = tf1.paragraphs[0]
    p_super.text = "LOVELY PROFESSIONAL UNIVERSITY • DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
    p_super.font.name = FONT_HEADING
    p_super.font.size = Pt(11)
    p_super.font.bold = True
    p_super.font.color.rgb = ACCENT_BLUE
    p_super.space_after = Pt(10)

    p_main = tf1.add_paragraph()
    p_main.text = "Automated DevOps Infrastructure Provisioning\n& Closed-Loop Self-Healing System"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(32)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_PRIMARY
    p_main.space_after = Pt(14)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Continuous Multi-Tier Resilience via Terraform, Ansible, Nginx, Gunicorn, Flask & Nagios Core 4.x"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = ACCENT_CYAN
    p_sub.space_after = Pt(24)

    # Meta box: Student & Guide details
    p_meta1 = tf1.add_paragraph()
    p_meta1.text = "Student: Ojaswi Bhardwaj  |  Registration No.: 12319444  |  Roll No.: 55  |  Section: K302316  |  Semester: 7"
    p_meta1.font.name = FONT_BODY
    p_meta1.font.size = Pt(11.5)
    p_meta1.font.bold = True
    p_meta1.font.color.rgb = TEXT_PRIMARY
    p_meta1.space_after = Pt(6)

    p_meta2 = tf1.add_paragraph()
    p_meta2.text = "Faculty Guide: Mr. Rakesh Gaganeja, Faculty, Department of Computer Science & Engineering"
    p_meta2.font.name = FONT_BODY
    p_meta2.font.size = Pt(11)
    p_meta2.font.color.rgb = TEXT_MUTED
    p_meta2.space_after = Pt(6)

    p_meta3 = tf1.add_paragraph()
    p_meta3.text = "Course: INT 333 (DevOps Practices & Cloud Automation)  |  Session: 2026–2027  |  Date: 27/11/2026"
    p_meta3.font.name = FONT_BODY
    p_meta3.font.size = Pt(11)
    p_meta3.font.color.rgb = TEXT_MUTED
    p_meta3.space_after = Pt(18)

    p_repo = tf1.add_paragraph()
    p_repo.text = "GitHub Repository: https://github.com/ojaswi1234/aws_monitoring_terraform.git"
    p_repo.font.name = FONT_CODE
    p_repo.font.size = Pt(11)
    p_repo.font.bold = True
    p_repo.font.color.rgb = ACCENT_GREEN

    # ==========================================================================
    # SLIDE 2: Executive Summary & System Objectives
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Executive Summary & Architectural Scope", "Project Foundations")

    add_card(s2, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "1. Declarative Cloud IaC",
             [
                 "Platform: Amazon Web Services (AWS) in us-east-1.",
                 "Provisioner: HashiCorp Terraform 1.5+.",
                 "Topology: Custom VPC, public subnets, internet gateway, and route tables.",
                 "Compute: Two isolated Ubuntu 22.04 LTS EC2 instances (Monitor & App).",
                 "Zero Drift: Complete infrastructure reproducible via terraform apply."
             ], badge="Cloud Provisioning", badge_color=ACCENT_BLUE)

    add_card(s2, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "2. Microservice Stack",
             [
                 "Backend API: Modular Python Flask application factory (create_app).",
                 "WSGI Server: Multi-worker Gunicorn bound strictly to 127.0.0.1:8000.",
                 "Reverse Proxy: Nginx on port 80 forwarding traffic and serving static UI.",
                 "Probing Endpoints: Granular /healthz (liveness) and /readyz (readiness).",
                 "Unit Testing: Comprehensive 7-test suite passing with 100% success."
             ], badge="Application Tier", badge_color=ACCENT_CYAN)

    add_card(s2, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "3. Autonomous Closed-Loop",
             [
                 "Active Telemetry: Nagios Core 4.x probing endpoints every 10–30s.",
                 "State Machine: Validates SOFT failures before HARD CRITICAL escalation.",
                 "Event-Driven Action: Fires recover_flask.sh on confirmed outage.",
                 "Ansible Remediation: Restarts systemd unit & asserts HTTP 200.",
                 "Dramatic Result: 98.9% MTTR reduction (18.4s vs 12–33 minutes)."
             ], badge="Self-Healing Engine", badge_color=ACCENT_GREEN)

    # ==========================================================================
    # SLIDE 3: Problem Statement: Traditional Operational Bottlenecks
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Problem Statement: Why Traditional Operations Fail", "Context & Industry Motivation")

    add_card(s3, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "Passive Alerting Fatigue",
             [
                 "Disconnected Monitoring: Nagios/Zabbix send emails or pages to engineers.",
                 "Human Response Latency: 5–15 minutes lost before an engineer acknowledges.",
                 "Sleep Deprivation: On-call engineers woken for routine transient crashes.",
                 "SLA Breaches: Enterprise availability commitments violated during triage."
             ], badge="Operational Pain", badge_color=ACCENT_RED)

    add_card(s3, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "Manual Triage & Stress",
             [
                 "Authentication Lag: 3–8 minutes to connect to VPN and locate SSH keys.",
                 "Manual Terminal Errors: Typing systemctl restart under pressure invites mistakes.",
                 "Snowflake Drift: Ad-hoc package installations leave undocumented server changes.",
                 "Incomplete Logs: Post-mortem forensics hindered by fragmented bash histories."
             ], badge="Human Error Risk", badge_color=ACCENT_AMBER)

    add_card(s3, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "The Self-Healing Remedy",
             [
                 "Machine-Speed Detection: Nagios actively detects failures within seconds.",
                 "Zero-Touch Remediation: Idempotent Ansible playbooks execute automatically.",
                 "Defensive Controls: Non-blocking locks and cooldown timers prevent loops.",
                 "Centralized Audit Log: Timestamped trace records every remediation attempt."
             ], badge="DevOps Objective", badge_color=ACCENT_GREEN)

    # ==========================================================================
    # SLIDE 4: Integrated DevOps Toolchain: Roles & Synergies
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "DevOps Toolchain Integration & Synergy Map", "Tool Collaboration Architecture")

    tools = [
        ("1. Terraform (IaC)", [
            "Provisions VPC, subnets, gateways, and security groups in AWS.",
            "Deploys monitor-server and app-server EC2 compute instances.",
            "Outputs dynamic IP addresses for automated inventory creation."
        ], ACCENT_BLUE),
        ("2. Ansible (Config Mgmt)", [
            "Idempotently configures packages, users, and hardened virtualenvs.",
            "Deploys Nginx reverse proxy configs and systemd unit templates.",
            "Executes automated recovery playbooks over internal VPC SSH."
        ], ACCENT_PURPLE),
        ("3. Python Flask & Gunicorn", [
            "Provides modular REST API backend with application factory.",
            "Gunicorn WSGI manages worker processes isolated on 127.0.0.1:8000.",
            "Exposes /healthz and /readyz endpoints for active telemetry."
        ], ACCENT_CYAN),
        ("4. Nginx Reverse Proxy", [
            "Acts as the public gateway (:80) routing requests and serving web UI.",
            "Provides separate /nginx-health probe to decouple web from backend.",
            "Enforces upstream timeouts, header forwarding, and failure handling."
        ], ACCENT_AMBER),
        ("5. Nagios Core 4.x", [
            "Continuously probes hosts, ports, system resources, and HTTP payloads.",
            "Evaluates check thresholds (SOFT state -> 3 retries -> HARD state).",
            "Dispatches event handlers exclusively upon confirmed HARD CRITICAL."
        ], ACCENT_GREEN),
        ("6. Event Handler Engine", [
            "Restricted shell wrapper (recover_flask.sh) with non-blocking flock.",
            "Enforces 60-second anti-flapping cooldown timer to prevent loops.",
            "Invokes Ansible recover_flask.yml and verifies healthy HTTP 200."
        ], ACCENT_RED)
    ]

    for idx, (title, bullets, color) in enumerate(tools):
        row = idx // 3
        col = idx % 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.5 + row * 2.8)
        add_card(s4, left, top, Inches(3.7), Inches(2.6), title, bullets, badge=f"Tool Tier {idx+1}", badge_color=color)

    # ==========================================================================
    # SLIDE 5: Visual End-to-End Workflow & Data Flow (Interactive Flowchart)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "End-to-End System Workflow & Data Flowchart", "Closed-Loop Control Flow")

    steps = [
        ("1. PROVISION", "Terraform IaC", "Creates VPC, Security Groups, and 2 EC2 instances", ACCENT_BLUE),
        ("2. CONFIGURE", "Ansible Engine", "Deploys Nginx, Flask systemd unit, and Nagios Core", ACCENT_PURPLE),
        ("3. TELEMETRY", "Nagios Core 4.x", "Active HTTP GET probes against /healthz every 10s", ACCENT_CYAN),
        ("4. DETECTION", "State Escalation", "Daemon crash detected -> SOFT -> HARD CRITICAL", ACCENT_AMBER),
        ("5. TRIGGER", "Event Handler", "recover_flask.sh checks lock & cooldown, starts Ansible", ACCENT_RED),
        ("6. REMEDIATION", "Ansible Playbook", "systemd restart + port wait + local URI check", ACCENT_GREEN),
        ("7. RECOVERY", "Service Restored", "Nagios probe gets HTTP 200 OK -> state reset to OK", ACCENT_CYAN)
    ]

    flow_w = Inches(1.5)
    flow_h = Inches(4.8)
    spacing = Inches(1.7)

    for i, (phase, tool, desc, col) in enumerate(steps):
        left = Inches(0.8 + i * spacing)
        top = Inches(1.6)

        # Flow Box
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, flow_w, flow_h)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(left + Inches(0.1), top + Inches(0.15), flow_w - Inches(0.2), flow_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Step Number Badge
        p_num = tf.paragraphs[0]
        p_num.text = f"STEP {i+1}"
        p_num.font.name = FONT_HEADING
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = col
        p_num.space_after = Pt(4)

        # Phase Title
        p_ph = tf.add_paragraph()
        p_ph.text = phase
        p_ph.font.name = FONT_HEADING
        p_ph.font.size = Pt(12)
        p_ph.font.bold = True
        p_ph.font.color.rgb = TEXT_PRIMARY
        p_ph.space_after = Pt(8)

        # Tool Badge
        p_t = tf.add_paragraph()
        p_t.text = f"[{tool}]"
        p_t.font.name = FONT_CODE
        p_t.font.size = Pt(9)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_BLUE
        p_t.space_after = Pt(12)

        # Description
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED

        # Arrow to next step
        if i < len(steps) - 1:
            arrow = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left + flow_w + Inches(0.04), top + Inches(2.2), Inches(0.12), Inches(0.3))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = col
            arrow.line.fill.background()

    # Flow Explanation Banner
    banner = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.55), Inches(11.7), Inches(0.55))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = ACCENT_GREEN
    banner.line.width = Pt(1)

    tb_ban = s5.shapes.add_textbox(Inches(0.9), Inches(6.6), Inches(11.5), Inches(0.45))
    tf_ban = tb_ban.text_frame
    tf_ban.margin_left = tf_ban.margin_top = tf_ban.margin_right = tf_ban.margin_bottom = 0
    p_b = tf_ban.paragraphs[0]
    p_b.text = "CLOSED-LOOP DATA FLOW: HTTP 503 Outage ➔ State Machine HARD CRITICAL ➔ Shell flock & Cooldown ➔ Private VPC SSH Playbook ➔ systemd Restart ➔ HTTP 200 Assertion"
    p_b.font.name = FONT_CODE
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = ACCENT_GREEN

    # ==========================================================================
    # SLIDE 6: Two-Node Cloud System Architecture & Network Topology
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Cloud System Architecture & Security Topology", "AWS VPC Infrastructure")

    add_card(s6, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Server 1: Central Monitoring Node",
             [
                 "Hostname & OS: monitor-server (Ubuntu 22.04 LTS).",
                 "VPC Private IP: 10.0.1.28 | Elastic Public IP: 44.223.101.208.",
                 "Nagios Core 4.x: Tactical monitoring engine scheduling active checks.",
                 "Apache Web UI: Secure SSL/HTTP interface on port 80/nagios.",
                 "Ansible Control Node: Executes local and remote playbooks.",
                 "Security Ingress (monitor-sg): SSH (22) & HTTP (80) locked to Admin IP.",
                 "Private Routing: SSH connections to app-server travel over VPC private IPs."
             ], badge="Orchestrator Node", badge_color=ACCENT_BLUE)

    add_card(s6, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Server 2: Production Application Node",
             [
                 "Hostname & OS: app-server (Ubuntu 22.04 LTS).",
                 "VPC Private IP: 10.0.1.45 | Public IP: 98.84.41.102.",
                 "Nginx Reverse Proxy: Public port 80 routing requests and serving Web UI.",
                 "Gunicorn WSGI: Production Python server bound strictly to 127.0.0.1:8000.",
                 "Flask REST Backend: Business APIs, liveness (/healthz), readiness (/readyz).",
                 "Supervised by systemd: Managed as flask-backend.service with Restart=on-failure.",
                 "Security Ingress (app-sg): Port 80 public; SSH (22) restricted to monitor-sg."
             ], badge="Workload Node", badge_color=ACCENT_GREEN)

    # ==========================================================================
    # SLIDE 7: Tool 1: Terraform — Infrastructure as Code & Snippet
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Tool 1: HashiCorp Terraform — Declarative Cloud IaC", "Infrastructure as Code")

    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.3), Inches(5.4),
             "Terraform Architecture & Lifecycle",
             [
                 "Declarative Provisioning: Entire AWS topology codified in HCL.",
                 "Provider Version Pinning: hashicorp/aws ~> 5.0 ensures reproducible builds.",
                 "Network Resources: aws_vpc, aws_internet_gateway, aws_subnet, aws_route_table.",
                 "Least-Privilege Security Groups: Security groups reference each other by ID.",
                 "Dynamic AMI Lookup: Automatically selects latest canonical Ubuntu 22.04 AMI.",
                 "Dynamic Inventory: scripts/generate_inventory.sh extracts IPs to hosts.ini.",
                 "Zero Cloud Drift: State file tracks 10 managed cloud resources."
             ], badge="Terraform Architecture", badge_color=ACCENT_BLUE)

    tf_code = [
        '# terraform/main.tf: AWS Infrastructure Provisioning',
        'resource "aws_vpc" "main" {',
        '  cidr_block           = var.vpc_cidr           # 10.0.0.0/16',
        '  enable_dns_hostnames = true',
        '}',
        '',
        'resource "aws_subnet" "public" {',
        '  vpc_id                  = aws_vpc.main.id',
        '  cidr_block              = var.public_subnet_cidr # 10.0.1.0/24',
        '  map_public_ip_on_launch = true',
        '}',
        '',
        'resource "aws_security_group" "app_sg" {',
        '  name   = "${var.project_name}-app-sg"',
        '  vpc_id = aws_vpc.main.id',
        '',
        '  ingress { # Allow HTTP from everywhere',
        '    from_port   = 80',
        '    to_port     = 80',
        '    protocol    = "tcp"',
        '    cidr_blocks = ["0.0.0.0/0"]',
        '  }',
        '  ingress { # SSH allowed ONLY from monitor server',
        '    from_port       = 22',
        '    to_port         = 22',
        '    protocol        = "tcp"',
        '    security_groups = [aws_security_group.monitor_sg.id]',
        '  }',
        '}'
    ]
    add_code_card(s7, Inches(6.4), Inches(1.5), Inches(6.1), Inches(5.4), "terraform/main.tf", tf_code, lang="HCL")

    # ==========================================================================
    # SLIDE 8: Tool 2: Ansible — Configuration Management & Snippet
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Tool 2: Ansible — Configuration Management & Roles", "Configuration Automation")

    add_card(s8, Inches(0.8), Inches(1.5), Inches(5.3), Inches(5.4),
             "Ansible Role Hierarchy & Idempotency",
             [
                 "Modular Roles Architecture: Separates system layers into reusable roles.",
                 "Role 'common': Base packages, chrony NTP clock sync, security baselines.",
                 "Role 'python_backend': Creates flaskapp user, virtualenv, and systemd unit.",
                 "Role 'nginx': Deploys reverse proxy template and /nginx-health probe.",
                 "Role 'nagios': Installs Core 4.x, plugins, CGI files, and event handlers.",
                 "Strict Idempotency: Running playbooks multiple times produces identical state.",
                 "Agentless Architecture: Operates strictly over OpenSSH using 4096-bit RSA keys."
             ], badge="Ansible Automation", badge_color=ACCENT_PURPLE)

    ansible_code = [
        '# ansible/roles/python_backend/tasks/main.yml',
        '- name: Create unprivileged system user for backend',
        '  user: { name: "{{ app_user }}", system: yes, shell: /bin/false }',
        '',
        '- name: Deploy Python virtual environment and dependencies',
        '  pip:',
        '    requirements: /opt/flask-backend/requirements.txt',
        '    virtualenv: /opt/flask-backend/venv',
        '    virtualenv_command: /usr/bin/python3 -m venv',
        '',
        '- name: Deploy hardened systemd service unit',
        '  template:',
        '    src: flask-backend.service.j2',
        '    dest: /etc/systemd/system/flask-backend.service',
        '    mode: "0644"',
        '  notify: Reload systemd and restart backend',
        '',
        '- name: Ensure Flask backend is running and enabled',
        '  systemd: { name: flask-backend, state: started, enabled: yes }'
    ]
    add_code_card(s8, Inches(6.4), Inches(1.5), Inches(6.1), Inches(5.4), "ansible/roles/python_backend/tasks/main.yml", ansible_code, lang="YAML")

    # ==========================================================================
    # SLIDE 9: Tool 3: Python Flask & Gunicorn WSGI Architecture
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Tool 3: Python Flask REST Backend & Gunicorn WSGI", "Microservice Architecture")

    add_card(s9, Inches(0.8), Inches(1.5), Inches(5.3), Inches(5.4),
             "Flask REST Microservice Design",
             [
                 "Application Factory Pattern: Clean create_app() isolating config from routes.",
                 "Liveness Endpoint (/healthz): Returns 200 OK or 503 on process degradation.",
                 "Readiness Endpoint (/readyz): Confirms dependencies and runtime configs.",
                 "Status Endpoint (/api/v1/status): Exposes live uptime, service name, version.",
                 "Gunicorn WSGI: Multi-worker process model bound to 127.0.0.1:8000.",
                 "Hardened systemd Unit: ProtectSystem=full and PrivateTmp=true enabled.",
                 "Automated Pytest Suite: 7 unit tests verifying status codes and error handlers."
             ], badge="Flask Microservice", badge_color=ACCENT_CYAN)

    flask_code = [
        '# backend/app/routes/health.py: Active Health Probes',
        'from flask import Blueprint, jsonify, current_app',
        'import os',
        '',
        'health_bp = Blueprint("health", __name__)',
        'CRASH_FLAG_FILE = "/tmp/devops_simulated_crash"',
        '',
        '@health_bp.route("/healthz", methods=["GET"])',
        'def health_check():',
        '    """Liveness probe validating Flask daemon execution."""',
        '    if os.path.exists(CRASH_FLAG_FILE):',
        '        return jsonify({',
        '            "status": "CRITICAL",',
        '            "error": "Gunicorn worker terminated (Simulated Crash)",',
        '            "nagios_state": "CRITICAL"',
        '        }), 503',
        '',
        '    return jsonify({',
        '        "status": "ok",',
        '        "service": current_app.config.get("SERVICE_NAME"),',
        '        "nagios_state": "OK"',
        '    }), 200'
    ]
    add_code_card(s9, Inches(6.4), Inches(1.5), Inches(6.1), Inches(5.4), "backend/app/routes/health.py", flask_code, lang="PYTHON")

    # ==========================================================================
    # SLIDE 10: Tool 4: Nginx Reverse Proxy Architecture
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Tool 4: Nginx Reverse Proxy & Traffic Routing", "Web Server Architecture")

    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.3), Inches(5.4),
             "Nginx Edge Gateway & Routing",
             [
                 "Public HTTP Entry (:80): Public interface receiving all external traffic.",
                 "API Reverse Proxy: location /api/ passes requests to 127.0.0.1:8000.",
                 "Liveness Forwarding: location /healthz routed directly to Flask backend.",
                 "Decoupled Health Probe: location /nginx-health returns text/plain 200.",
                 "Fault Isolation: Nagios can distinguish Nginx crashes from Flask crashes.",
                 "Header Sanitization: Passes X-Real-IP and X-Forwarded-For to backend.",
                 "Strict Upstream Timeouts: 5s connection timeout prevents hung worker threads."
             ], badge="Nginx Proxy", badge_color=ACCENT_AMBER)

    nginx_code = [
        '# ansible/roles/nginx/templates/flask-app.conf.j2',
        'server {',
        '    listen 80 default_server;',
        '    server_name _;',
        '    root /var/www/html;',
        '    index index.html;',
        '',
        '    # Decoupled Nginx native health probe for Nagios',
        '    location /nginx-health {',
        '        access_log off;',
        '        return 200 "nginx-ok\\n";',
        '    }',
        '',
        '    # Proxy liveness check directly to Flask backend',
        '    location /healthz {',
        '        proxy_pass http://127.0.0.1:8000/healthz;',
        '        proxy_set_header Host $host;',
        '        proxy_set_header X-Real-IP $remote_addr;',
        '        proxy_connect_timeout 3s;',
        '        proxy_read_timeout 5s;',
        '    }',
        '}'
    ]
    add_code_card(s10, Inches(6.4), Inches(1.5), Inches(6.1), Inches(5.4), "ansible/roles/nginx/templates/flask-app.conf.j2", nginx_code, lang="NGINX")

    # ==========================================================================
    # SLIDE 11: Tool 5: Nagios Core 4.x Monitoring & State Machine
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Tool 5: Nagios Core 4.x Active Telemetry & State Logic", "Proactive Monitoring")

    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.3), Inches(5.4),
             "Nagios State Machine & Active Checks",
             [
                 "Continuous Probing: check_http interrogates /healthz on 10s intervals.",
                 "SOFT vs. HARD States: First failure transitions to SOFT CRITICAL (1/3).",
                 "Eliminates False Positives: Momentary network hiccups do not trigger restarts.",
                 "Escalation Threshold: 3 consecutive failures elevate service to HARD CRITICAL.",
                 "Event Handler Trigger: enable_event_handlers=1 dispatches remediation script.",
                 "Multi-Layer Coverage: Monitors host ping, SSH port 22, and HTTP endpoints.",
                 "Recovery Verification: Returns to OK status only when probe returns HTTP 200."
             ], badge="Nagios Telemetry", badge_color=ACCENT_GREEN)

    nagios_code = [
        '# /etc/nagios4/conf.d/app-server.cfg: Host & Service Definitions',
        'define host {',
        '    use                  linux-server',
        '    host_name            app-server',
        '    address              10.0.1.45',
        '    max_check_attempts   3',
        '}',
        '',
        'define service {',
        '    use                  generic-service',
        '    host_name            app-server',
        '    service_description  Flask Backend Health',
        '    check_command        check_http!-u /healthz -p 80 -e 200',
        '    max_check_attempts   3',
        '    check_interval       1',
        '    retry_interval       1',
        '    event_handler        recover_flask',
        '    event_handler_enabled 1',
        '}'
    ]
    add_code_card(s11, Inches(6.4), Inches(1.5), Inches(6.1), Inches(5.4), "/etc/nagios4/conf.d/app-server.cfg", nagios_code, lang="NAGIOS-CFG")

    # ==========================================================================
    # SLIDE 12: Tool 6: The Self-Healing Engine (recover_flask.sh & recover_flask.yml)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Tool 6: Event Handler & Ansible Remediation Engine", "Autonomous Self-Healing")

    # Left: recover_flask.sh snippet
    sh_code = [
        '#!/usr/bin/env bash',
        '# monitoring/scripts/recover_flask.sh',
        'STATE="$1"; TYPE="$2"; ATTEMPT="$3"',
        'LOG="/var/log/nagios_recovery.log"',
        'LOCK="/var/run/recover_flask.lock"',
        '',
        '# Only act on confirmed HARD CRITICAL failure',
        'if [ "$STATE" = "CRITICAL" ] && [ "$TYPE" = "HARD" ]; then',
        '  exec 200>"$LOCK"',
        '  # Non-blocking lock prevents race conditions',
        '  flock -n 200 || exit 0',
        '',
        '  echo "$(date) - Confirmed HARD CRITICAL. Running Ansible..." >> "$LOG"',
        '  ansible-playbook -i /opt/self-healing/inventory/hosts.ini \\',
        '    /opt/self-healing/playbooks/recover_flask.yml >> "$LOG" 2>&1',
        'fi'
    ]
    add_code_card(s12, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4), "recover_flask.sh", sh_code, lang="BASH")

    # Right: recover_flask.yml snippet
    yml_code = [
        '# ansible/playbooks/recover_flask.yml',
        '- name: Recover Flask Backend on App Server',
        '  hosts: webservers',
        '  become: yes',
        '  tasks:',
        '    - name: Restart Flask backend via systemd',
        '      systemd: { name: flask-backend, state: restarted }',
        '',
        '    - name: Wait for backend to bind port 8000',
        '      wait_for: { host: 127.0.0.1, port: 8000, timeout: 20 }',
        '',
        '    - name: Verify health endpoint returns HTTP 200',
        '      uri:',
        '        url: "http://127.0.0.1:8000/healthz"',
        '        status_code: 200',
        '      register: probe',
        '      until: probe.status == 200',
        '      retries: 5',
        '      delay: 2'
    ]
    add_code_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "recover_flask.yml", yml_code, lang="YAML")

    # ==========================================================================
    # SLIDE 13: Defensive Design & Anti-Flapping Safeguards
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Defensive Engineering & Anti-Flapping Controls", "Reliability & Safety")

    add_card(s13, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "1. Concurrency File Locks",
             [
                 "Non-Blocking flock: flock -n on /var/run/recover_*.lock.",
                 "Prevents Race Conditions: Parallel Nagios worker threads cannot launch concurrent recoveries.",
                 "Instant Exit: Redundant triggers abort immediately without queueing or hogging CPU.",
                 "Clean Release: Lock is released automatically when shell process terminates."
             ], badge="Execution Guard", badge_color=ACCENT_BLUE)

    add_card(s13, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "2. Anti-Flapping Cooldown",
             [
                 "60s Cooldown Window: Enforces mandatory delay between consecutive restart attempts.",
                 "Prevents Thrashing: Rapidly crashing applications do not trigger infinite restart loops.",
                 "Safe Escalation: If restart fails 3 times, playbook stops and notifies engineer.",
                 "Crash Loop Defense: Protects CPU, disk IOPS, and systemd journal buffers."
             ], badge="Loop Prevention", badge_color=ACCENT_AMBER)

    add_card(s13, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4),
             "3. Syntax Validation Pre-Check",
             [
                 "Nginx Pre-Flight: recover_nginx.yml executes nginx -t syntax check before reload.",
                 "Zero Blind Restarts: If configuration is invalid, restart is halted immediately.",
                 "Preserves Crash Context: Broken configuration is preserved for engineering autopsy.",
                 "Audit Trace: All events logged to /var/log/nagios_recovery.log."
             ], badge="Configuration Guard", badge_color=ACCENT_GREEN)

    # ==========================================================================
    # SLIDE 14: Authentic System Visuals: Nagios Core 4.4.6 & Web Console
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Authentic Operational Visuals: Web Console & Nagios", "System Verification")

    # Left: Web Console
    s1_img = os.path.join(ASSETS_DIR, "screenshot1_web_console.png")
    if os.path.exists(s1_img):
        s14.shapes.add_picture(s1_img, Inches(0.8), Inches(1.5), Inches(5.7), Inches(3.42))
    
    tb_c1 = s14.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(5.7), Inches(1.8))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p1 = tf_c1.paragraphs[0]
    p1.text = "Figure 1: Live DevOps Web Management Console (http://localhost:8000/)"
    p1.font.name = FONT_HEADING
    p1.font.bold = True
    p1.font.size = Pt(11)
    p1.font.color.rgb = ACCENT_BLUE
    p1_sub = tf_c1.add_paragraph()
    p1_sub.text = "Displays AWS EC2 instance metadata (app-server & monitor-server), interactive crash simulation controls, live probe indicators (/healthz, /readyz), and real-time closed-loop event audit logging."
    p1_sub.font.name = FONT_BODY
    p1_sub.font.size = Pt(9.5)
    p1_sub.font.color.rgb = TEXT_MUTED

    # Right: Nagios Core n1.png
    s2_img = os.path.join(ASSETS_DIR, "n1.png")
    if os.path.exists(s2_img):
        s14.shapes.add_picture(s2_img, Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.54))

    tb_c2 = s14.shapes.add_textbox(Inches(6.8), Inches(4.15), Inches(5.7), Inches(2.65))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p2 = tf_c2.paragraphs[0]
    p2.text = "Figure 2: Authentic Nagios Core 4.4.6 Tactical Service Status Details"
    p2.font.name = FONT_HEADING
    p2.font.bold = True
    p2.font.size = Pt(11)
    p2.font.color.rgb = ACCENT_GREEN
    p2_sub = tf_c2.add_paragraph()
    p2_sub.text = "Captured directly from the live deployment environment. Illustrates authentic Nagios Core 4.4.6 tactical status grid, active HTTP/Ping checks, latency tracking, and critical failure detection (Attempt 3/3 HARD) triggering automated self-healing."
    p2_sub.font.name = FONT_BODY
    p2_sub.font.size = Pt(9.5)
    p2_sub.font.color.rgb = TEXT_MUTED

    # ==========================================================================
    # SLIDE 15: Quantitative Benchmarks & MTTR Evaluation
    # ==========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Quantitative Benchmarks: 98.9% MTTR Reduction", "Performance Evaluation")

    # Table: Benchmark comparison
    rows = 7
    cols = 3
    tbl_shape = s15.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(3.6))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(4.25)
    tbl.columns[2].width = Inches(4.25)

    headers = ["Metric / Parameter", "Manual Engineering Response", "Automated Self-Healing DevOps"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_LIGHT_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT_BLUE if j < 2 else ACCENT_GREEN

    data = [
        ("Fault Detection Latency", "5 – 15 Minutes (Human notification delay)", "10 – 30 Seconds (Nagios active polling)"),
        ("Triage & Authentication", "3 – 8 Minutes (VPN & SSH login time)", "< 1 Second (Pre-authorized event trigger)"),
        ("Remediation Execution", "2 – 5 Minutes (Manual shell typing)", "4 – 6 Seconds (Idempotent Ansible playbook)"),
        ("Post-Recovery Validation", "2 – 5 Minutes (Ad-hoc curl commands)", "2 Seconds (Automated URI assertion check)"),
        ("Total Mean Time to Recovery (MTTR)", "12 – 33 Minutes", "18.4 Seconds (98.9% MTTR Reduction)"),
        ("Human Error Risk & Audit Trail", "High Risk / Incomplete bash history", "Zero Risk / 100% Centralized Audit Log")
    ]

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            if j == 0 or (i == 4 and j > 0):
                p.font.bold = True
                p.font.color.rgb = ACCENT_GREEN if (i == 4 and j == 2) else TEXT_PRIMARY
            else:
                p.font.color.rgb = TEXT_MUTED if j == 1 else ACCENT_CYAN

    # Summary Card below Table
    add_card(s15, Inches(0.8), Inches(5.35), Inches(11.7), Inches(1.55),
             "Empirical Performance Takeaways",
             [
                 "98.9% Reduction in Outage Duration: Automated self-healing collapses average MTTR from ~20 minutes to 18.4 seconds.",
                 "Deterministic Execution: Eliminates human error under stress; verifies socket binding and HTTP 200 before concluding.",
                 "Operational Focus Shift: Site Reliability Engineers are freed from repetitive daemon restarts to focus on architectural work."
             ], badge="Benchmark Conclusion", badge_color=ACCENT_GREEN)

    # ==========================================================================
    # SLIDE 16: Project Deliverables, GitHub & Academic Conclusion
    # ==========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "Project Deliverables & Viva Summary", "Conclusion & Deliverables")

    add_card(s16, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Project Accomplishments",
             [
                 "Full-Stack DevOps Integration: Bridged IaC (Terraform), CM (Ansible), WSGI (Flask/Gunicorn), and Monitoring (Nagios Core 4.x).",
                 "Closed-Loop Autonomy: Transformed passive threshold alerting into deterministic self-healing remediation.",
                 "Industrial Hardening: Built non-blocking flock locks, anti-flapping cooldown, and syntax validation pre-checks.",
                 "Rigorous Verification: 10 failure simulations consistently achieved autonomous recovery within 18.4 seconds.",
                 "Academic Report & Deliverables: Formal 12-page report replicating official LPU format with uncompressed screenshots."
             ], badge="Key Milestones", badge_color=ACCENT_GREEN)

    add_card(s16, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4),
             "Source Code Repository & Viva Readiness",
             [
                 "Public GitHub Repository: https://github.com/ojaswi1234/aws_monitoring_terraform.git.",
                 "Student: Ojaswi Bhardwaj (Reg: 12319444 | Roll: 55 | Sec: K302316 | Sem: 7).",
                 "Faculty Guide: Mr. Rakesh Gaganeja, Faculty, Department of Computer Science & Engineering.",
                 "Institution: Lovely Professional University, Punjab, India.",
                 "Code Organization: Clean modular directories (terraform/, ansible/, backend/, monitoring/, scripts/).",
                 "One-Click Validation: Automated pre-flight suite (./scripts/validate.sh) verifies pytest, terraform, and ansible."
             ], badge="Repository & Credentials", badge_color=ACCENT_BLUE)

    # Save presentation
    prs.save(output_path)
    print(f"Enhanced presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    out_file = "/home/ob/devops-self-healing-project/DevOps_Self_Healing_Architecture_Visualized.pptx"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    create_presentation(out_file)
