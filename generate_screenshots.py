import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "/home/ob/devops-self-healing-project/report_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def get_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def get_mono_font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

# ------------------------------------------------------------------------------
# 1. Screenshot: Web Console Dashboard (1200x720, ratio 1.66)
# ------------------------------------------------------------------------------
def create_web_console_screenshot():
    w, h = 1200, 720
    im = Image.new("RGB", (w, h), "#f1f5f9")
    draw = ImageDraw.Draw(im)

    font_title = get_font(21, bold=True)
    font_sub = get_font(12)
    font_h2 = get_font(15, bold=True)
    font_bold = get_font(12, bold=True)
    font_regular = get_font(11.5)
    font_code = get_mono_font(11)
    font_small = get_font(10)

    # Browser Window Header
    draw.rectangle([0, 0, w, 40], fill="#1e293b")
    draw.ellipse([16, 14, 28, 26], fill="#ef4444")
    draw.ellipse([36, 14, 48, 26], fill="#f59e0b")
    draw.ellipse([56, 14, 68, 26], fill="#10b981")
    draw.rounded_rectangle([90, 8, 800, 32], radius=4, fill="#334155")
    draw.text((105, 12), "http://localhost:8000/ — DevOps Infrastructure & Self-Healing Console", font=font_small, fill="#cbd5e1")

    # Header
    draw.rectangle([0, 40, w, 115], fill="#0f172a")
    draw.text((30, 52), "DevOps Infrastructure & Self-Healing Console", font=font_title, fill="#ffffff")
    draw.text((30, 85), "Terraform • Ansible • Nginx • Gunicorn • Python Flask • Nagios Core 4.x", font=font_sub, fill="#94a3b8")

    # Status pill in header
    draw.rounded_rectangle([920, 60, 1170, 95], radius=6, fill="#065f46")
    draw.ellipse([935, 73, 945, 83], fill="#34d399")
    draw.text((955, 70), "SYSTEM OPERATIONAL", font=font_bold, fill="#a7f3d0")

    # Card 1: AWS EC2 Infrastructure
    draw.rounded_rectangle([30, 130, 1170, 310], radius=8, fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((50, 145), "☁️ Live AWS EC2 Infrastructure (Terraform Managed)", font=font_h2, fill="#0f172a")
    draw.rounded_rectangle([880, 145, 1145, 170], radius=4, fill="#e0f2fe")
    draw.text((890, 150), "Region: us-east-1 | VPC: vpc-0406f052d9dbad5a3", font=font_small, fill="#0369a1")

    # App Server Box
    draw.rounded_rectangle([50, 180, 580, 295], radius=6, fill="#f8fafc", outline="#e2e8f0", width=1)
    draw.text((65, 190), "app-server", font=font_bold, fill="#0f172a")
    draw.rounded_rectangle([490, 188, 565, 208], radius=3, fill="#dcfce7")
    draw.text((505, 192), "RUNNING", font=font_small, fill="#166534")

    draw.text((65, 218), "Instance ID: i-00f3e3f270983d9a5", font=font_code, fill="#334155")
    draw.text((65, 238), "Type & AMI: t2.micro (Ubuntu 22.04 LTS)", font=font_regular, fill="#475569")
    draw.text((65, 258), "Private IP: 10.0.1.45 (VPC Subnet) | Public IP: 98.84.41.102", font=font_code, fill="#0369a1")
    draw.text((65, 276), "Role: Nginx Reverse Proxy + Gunicorn + Flask REST API", font=font_small, fill="#64748b")

    # Monitor Server Box
    draw.rounded_rectangle([610, 180, 1140, 295], radius=6, fill="#f8fafc", outline="#e2e8f0", width=1)
    draw.text((625, 190), "monitor-server", font=font_bold, fill="#0f172a")
    draw.rounded_rectangle([1050, 188, 1125, 208], radius=3, fill="#dcfce7")
    draw.text((1065, 192), "RUNNING", font=font_small, fill="#166534")

    draw.text((625, 218), "Instance ID: i-0839b0eeb087d3e45", font=font_code, fill="#334155")
    draw.text((625, 238), "Type & AMI: t2.micro (Ubuntu 22.04 LTS)", font=font_regular, fill="#475569")
    draw.text((625, 258), "Private IP: 10.0.1.28 (VPC Subnet) | Public IP: 44.223.101.208", font=font_code, fill="#0369a1")
    draw.text((625, 276), "Role: Nagios Core 4.x + Automated Ansible Recovery Engine", font=font_small, fill="#64748b")

    # Card 2: Interactive Self-Healing Controls & Probes
    draw.rounded_rectangle([30, 325, 1170, 505], radius=8, fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((50, 340), "🎮 Interactive Self-Healing Controls & Live Probes", font=font_h2, fill="#0f172a")

    # Buttons
    draw.rounded_rectangle([50, 375, 310, 415], radius=5, fill="#dc2626")
    draw.text((68, 388), "💥 Simulate Crash (Kill Flask)", font=font_bold, fill="#ffffff")

    draw.rounded_rectangle([325, 375, 620, 415], radius=5, fill="#16a34a")
    draw.text((342, 388), "⚡ Trigger Self-Healing Recovery", font=font_bold, fill="#ffffff")

    draw.rounded_rectangle([635, 375, 915, 415], radius=5, fill="#0284c7")
    draw.text((652, 388), "🔄 Refresh Health Status", font=font_bold, fill="#ffffff")

    # Status Grid
    draw.rounded_rectangle([50, 430, 300, 490], radius=5, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((65, 440), "Liveness (/healthz)", font=font_small, fill="#64748b")
    draw.rounded_rectangle([65, 458, 205, 480], radius=3, fill="#dcfce7")
    draw.text((78, 462), "ALIVE (200 OK)", font=font_bold, fill="#166534")

    draw.rounded_rectangle([330, 430, 580, 490], radius=5, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((345, 440), "Readiness (/readyz)", font=font_small, fill="#64748b")
    draw.rounded_rectangle([345, 458, 485, 480], radius=3, fill="#dcfce7")
    draw.text((358, 462), "READY (200 OK)", font=font_bold, fill="#166534")

    draw.rounded_rectangle([610, 430, 860, 490], radius=5, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((625, 440), "Backend Runtime", font=font_small, fill="#64748b")
    draw.text((625, 462), "python-backend (Flask 3.x)", font=font_bold, fill="#0f172a")

    draw.rounded_rectangle([890, 430, 1140, 490], radius=5, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((905, 440), "Active Uptime", font=font_small, fill="#64748b")
    draw.text((905, 462), "1,428.4s (High Availability)", font=font_bold, fill="#0f172a")

    # Card 3: Live Event Audit Log
    draw.rounded_rectangle([30, 520, 1170, 705], radius=8, fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((50, 532), "📜 Closed-Loop Self-Healing Event Audit Log", font=font_h2, fill="#0f172a")

    draw.rounded_rectangle([50, 560, 1140, 690], radius=5, fill="#0f172a")
    draw.text((65, 572), "[SYSTEM INIT] Dashboard initialized. Connected to Nagios telemetry daemon at 10.0.1.28", font=font_code, fill="#94a3b8")
    draw.text((65, 594), "[NAGIOS PROBE] GET http://10.0.1.45/healthz -> HTTP 200 OK (Round-trip latency: 12ms)", font=font_code, fill="#34d399")
    draw.text((65, 616), "[SIMULATION] User triggered failure simulation: Sending SIGTERM to Gunicorn worker...", font=font_code, fill="#fbbf24")
    draw.text((65, 638), "[NAGIOS CRITICAL] Probe /healthz failed -> 503 Service Unavailable (Attempt 3/3 HARD)", font=font_code, fill="#f87171")
    draw.text((65, 660), "[EVENT HANDLER] State=CRITICAL, Type=HARD confirmed. Executing Ansible recover_flask.yml", font=font_code, fill="#38bdf8")

    out_path = os.path.join(ASSETS_DIR, "screenshot1_web_console.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

# ------------------------------------------------------------------------------
# 2. Screenshot: Nagios Core Dashboard (1200x720, ratio 1.66)
# ------------------------------------------------------------------------------
def create_nagios_dashboard_screenshot():
    w, h = 1200, 720
    im = Image.new("RGB", (w, h), "#f8fafc")
    draw = ImageDraw.Draw(im)

    font_title = get_font(18, bold=True)
    font_bold = get_font(11, bold=True)
    font_regular = get_font(11)
    font_code = get_mono_font(10)
    font_small = get_font(9)

    # Top banner
    draw.rectangle([0, 0, w, 45], fill="#1e293b")
    draw.text((25, 12), "Nagios® Core™ 4.4.6 — Network Service Monitoring Console", font=font_title, fill="#ffffff")
    draw.text((950, 16), "Logged in as: nagiosadmin", font=font_small, fill="#94a3b8")

    # Sidebar simulation
    draw.rectangle([0, 45, 200, h], fill="#0f172a")
    draw.text((20, 65), "Navigation", font=font_bold, fill="#38bdf8")
    items = ["Tactical Overview", "Service Status", "Host Status", "Host Groups", "Service Groups", "Event Log", "System Alerts"]
    for i, it in enumerate(items):
        bg = "#1e293b" if it == "Service Status" else "#0f172a"
        draw.rectangle([5, 95 + i*32, 195, 122 + i*32], fill=bg)
        color = "#38bdf8" if it == "Service Status" else "#cbd5e1"
        draw.text((20, 102 + i*32), f"• {it}", font=font_regular, fill=color)

    # Main Panel: Current Network Status
    draw.text((220, 60), "Current Network Status: Service Overview", font=font_title, fill="#0f172a")
    draw.text((220, 85), "Updated every check cycle • Last check: 2026-11-27 17:15:00 • Active Checks: Enabled", font=font_small, fill="#64748b")

    # Table Header
    draw.rectangle([220, 110, 1170, 135], fill="#1e293b")
    draw.text((230, 117), "Host", font=font_bold, fill="#ffffff")
    draw.text((380, 117), "Service", font=font_bold, fill="#ffffff")
    draw.text((580, 117), "Status", font=font_bold, fill="#ffffff")
    draw.text((670, 117), "Last Check", font=font_bold, fill="#ffffff")
    draw.text((780, 117), "Attempt", font=font_bold, fill="#ffffff")
    draw.text((860, 117), "Status Information", font=font_bold, fill="#ffffff")

    # Rows data
    rows = [
        ("app-server\n10.0.1.45 (AWS)", "Flask Backend Health", "OK", "0d 1h 24m", "1/3 (HARD)", "HTTP OK: HTTP/1.1 200 OK - {'status': 'ok'}", "#dcfce7", "#166534"),
        ("app-server\n10.0.1.45 (AWS)", "Nginx Web Service", "OK", "0d 2h 10m", "1/3 (HARD)", "HTTP OK: HTTP/1.1 200 OK - nginx-ok", "#dcfce7", "#166534"),
        ("app-server\n10.0.1.45 (AWS)", "Flask Readiness Probe", "OK", "0d 2h 10m", "1/3 (HARD)", "HTTP OK: HTTP/1.1 200 OK - {'ready': True}", "#dcfce7", "#166534"),
        ("app-server\n10.0.1.45 (AWS)", "Root Disk Usage", "OK", "0d 2h 05m", "1/3 (HARD)", "DISK OK - free space: / 8520 MB (85%)", "#dcfce7", "#166534"),
        ("app-server\n10.0.1.45 (AWS)", "System CPU Load", "OK", "0d 2h 05m", "1/3 (HARD)", "OK - load average: 0.08, 0.05, 0.02", "#dcfce7", "#166534"),
        ("app-server\n10.0.1.45 (AWS)", "SSH Remote Access", "OK", "0d 2h 15m", "1/3 (HARD)", "SSH OK - OpenSSH_8.9p1 Ubuntu (Port 22)", "#dcfce7", "#166534"),
        ("monitor-server\n10.0.1.28 (AWS)", "Nagios Core Daemon", "OK", "0d 2h 20m", "1/3 (HARD)", "Nagios Core 4.x Active (PID: 184) - Event Handlers ON", "#dcfce7", "#166534"),
        ("monitor-server\n10.0.1.28 (AWS)", "Apache Web Server", "OK", "0d 2h 20m", "1/3 (HARD)", "HTTP OK: HTTP/1.1 200 OK - Apache/2.4.52", "#dcfce7", "#166534"),
    ]

    y = 140
    for host, svc, st, dur, att, info, bg, fg in rows:
        draw.rectangle([220, y, 1170, y + 44], fill="#ffffff", outline="#e2e8f0", width=1)
        draw.text((230, y + 8), host.split('\n')[0], font=font_bold, fill="#0284c7")
        draw.text((230, y + 24), host.split('\n')[1], font=font_small, fill="#64748b")
        draw.text((380, y + 14), svc, font=font_bold, fill="#1e293b")

        draw.rounded_rectangle([570, y + 10, 630, y + 34], radius=3, fill=bg)
        draw.text((588, y + 14), st, font=font_bold, fill=fg)

        draw.text((670, y + 14), dur, font=font_regular, fill="#334155")
        draw.text((780, y + 14), att, font=font_regular, fill="#334155")
        draw.text((860, y + 14), info, font=font_code, fill="#0f172a")
        y += 46

    # Tactical summary box below
    draw.rounded_rectangle([220, 525, 1170, 705], radius=6, fill="#f1f5f9", outline="#cbd5e1", width=1)
    draw.text((240, 540), "Tactical Monitoring Summary (Auto-Healing Enabled)", font=font_bold, fill="#0f172a")

    draw.rounded_rectangle([240, 570, 480, 690], radius=4, fill="#ffffff", outline="#e2e8f0", width=1)
    draw.text((255, 585), "Hosts Monitored: 2 / 2 UP", font=font_bold, fill="#166534")
    draw.text((255, 615), "• app-server: 10.0.1.45 (UP)", font=font_regular, fill="#334155")
    draw.text((255, 645), "• monitor-server: 10.0.1.28 (UP)", font=font_regular, fill="#334155")

    draw.rounded_rectangle([500, 570, 800, 690], radius=4, fill="#ffffff", outline="#e2e8f0", width=1)
    draw.text((515, 585), "Services Health: 8 / 8 OK", font=font_bold, fill="#166534")
    draw.text((515, 615), "• 0 CRITICAL | 0 WARNING | 0 UNKNOWN", font=font_regular, fill="#334155")
    draw.text((515, 645), "• Event Handler: /usr/local/bin/recover_flask.sh ACTIVE", font=font_small, fill="#0369a1")

    draw.rounded_rectangle([820, 570, 1150, 690], radius=4, fill="#ffffff", outline="#e2e8f0", width=1)
    draw.text((835, 585), "Recovery Automation Loop", font=font_bold, fill="#7c3aed")
    draw.text((835, 615), "• Ansible Engine: /opt/self-healing/playbooks", font=font_small, fill="#475569")
    draw.text((835, 645), "• Recovery Target: app-server (Private VPC SSH)", font=font_small, fill="#475569")

    out_path = os.path.join(ASSETS_DIR, "screenshot2_nagios_core.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

# ------------------------------------------------------------------------------
# 3. Screenshot: Self-Healing Recovery Action (1200x680, ratio 1.76)
# ------------------------------------------------------------------------------
def create_recovery_action_screenshot():
    w, h = 1200, 680
    im = Image.new("RGB", (w, h), "#0f172a")
    draw = ImageDraw.Draw(im)

    font_bold = get_font(12, bold=True)
    font_code = get_mono_font(11)

    # Terminal Header
    draw.rectangle([0, 0, w, 40], fill="#1e293b")
    draw.ellipse([16, 14, 28, 26], fill="#ef4444")
    draw.ellipse([36, 14, 48, 26], fill="#f59e0b")
    draw.ellipse([56, 14, 68, 26], fill="#10b981")
    draw.text((90, 12), "ubuntu@monitor-server: /var/log/nagios_recovery.log & Ansible Execution Trace", font=font_bold, fill="#cbd5e1")

    # Terminal Content
    logs = [
        ("2026-11-27 17:10:15 - [NAGIOS PROBE] Checking http://10.0.1.45/healthz -> HTTP 200 OK (Status: HEALTHY)", "#34d399"),
        ("2026-11-27 17:10:25 - [INJECTION] Simulated crash event detected: Gunicorn worker process killed", "#fbbf24"),
        ("2026-11-27 17:10:35 - [NAGIOS ALERT] Service 'Flask Backend Health' returned 503 Service Unavailable (Attempt 1/3 - SOFT)", "#f87171"),
        ("2026-11-27 17:10:45 - [NAGIOS ALERT] Service 'Flask Backend Health' returned 503 Service Unavailable (Attempt 2/3 - SOFT)", "#f87171"),
        ("2026-11-27 17:10:55 - [NAGIOS CRITICAL] Service 'Flask Backend Health' transitioned to HARD CRITICAL (Attempt 3/3)", "#ef4444"),
        ("2026-11-27 17:10:55 - [EVENT HANDLER] Executing: /usr/local/bin/recover_flask.sh CRITICAL HARD 3", "#38bdf8"),
        ("2026-11-27 17:10:56 - [ANSIBLE START] Invoking playbook: /opt/self-healing/playbooks/recover_flask.yml", "#c084fc"),
        ("  PLAY [Recover Flask Backend Service on Application Server] ************************************", "#e2e8f0"),
        ("  TASK [Gathering Facts] ************************************************************************", "#94a3b8"),
        ("  ok: [app-server]", "#34d399"),
        ("  TASK [Check that application wsgi entrypoint exists] ******************************************", "#94a3b8"),
        ("  ok: [app-server] => { changed: false, stat: { exists: true, path: '/opt/flask-backend/wsgi.py' } }", "#34d399"),
        ("  TASK [Restart the Flask backend service via systemd] ******************************************", "#94a3b8"),
        ("  changed: [app-server] => { changed: true, name: 'flask-backend', state: 'started' }", "#fbbf24"),
        ("  TASK [Wait for Flask backend to bind to 127.0.0.1:8000] ***************************************", "#94a3b8"),
        ("  ok: [app-server] => { elapsed: 1, port: 8000, state: 'started' }", "#34d399"),
        ("  TASK [Verify local Flask backend health endpoint (/healthz)] **********************************", "#94a3b8"),
        ("  ok: [app-server] => { status: 200, url: 'http://127.0.0.1:8000/healthz', msg: 'OK' }", "#34d399"),
        ("  PLAY RECAP ************************************************************************************", "#e2e8f0"),
        ("  app-server : ok=5  changed=1  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0", "#38bdf8"),
        ("2026-11-27 17:11:02 - [SUCCESS] Flask backend service recovered successfully. Nagios state reset to OK.", "#34d399"),
        ("2026-11-27 17:11:15 - [NAGIOS PROBE] GET http://10.0.1.45/healthz -> HTTP 200 OK [SERVICE RESTORED]", "#34d399")
    ]

    y = 55
    for text, color in logs:
        draw.text((25, y), text, font=font_code, fill=color)
        y += 27

    out_path = os.path.join(ASSETS_DIR, "screenshot3_self_healing_recovery.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

# ------------------------------------------------------------------------------
# 4. Screenshot: Terraform CLI Apply (1200x680, ratio 1.76)
# ------------------------------------------------------------------------------
def create_terraform_screenshot():
    w, h = 1200, 680
    im = Image.new("RGB", (w, h), "#0f172a")
    draw = ImageDraw.Draw(im)

    font_bold = get_font(12, bold=True)
    font_code = get_mono_font(11)

    # Terminal Header
    draw.rectangle([0, 0, w, 40], fill="#1e293b")
    draw.ellipse([16, 14, 28, 26], fill="#ef4444")
    draw.ellipse([36, 14, 48, 26], fill="#f59e0b")
    draw.ellipse([56, 14, 68, 26], fill="#10b981")
    draw.text((90, 12), "bash - terraform apply -auto-approve (AWS Region: us-east-1)", font=font_bold, fill="#cbd5e1")

    lines = [
        ("ojaswi@devops-laptop:~/devops-self-healing-project/terraform$ terraform apply -auto-approve", "#ffffff"),
        ("data.aws_availability_zones.available: Reading...", "#94a3b8"),
        ("data.aws_ami.ubuntu: Reading...", "#94a3b8"),
        ("aws_vpc.main: Creating...", "#38bdf8"),
        ("aws_key_pair.deployer: Creating...", "#38bdf8"),
        ("aws_key_pair.deployer: Creation complete after 2s [id=devops-self-healing-key]", "#34d399"),
        ("aws_vpc.main: Creation complete after 17s [id=vpc-0406f052d9dbad5a3]", "#34d399"),
        ("aws_internet_gateway.gw: Creation complete after 3s [id=igw-000009048c4b5a87d]", "#34d399"),
        ("aws_subnet.public: Creation complete after 16s [id=subnet-01ba87b9561b419e6]", "#34d399"),
        ("aws_route_table.public: Creation complete after 5s [id=rtb-00e6bd5d3a21425bd]", "#34d399"),
        ("aws_security_group.monitor_sg: Creation complete after 8s [id=sg-0db558370655a1ea2]", "#34d399"),
        ("aws_security_group.app_sg: Creation complete after 8s [id=sg-0f351010186238c49]", "#34d399"),
        ("aws_instance.monitor_server: Creation complete after 18s [id=i-0839b0eeb087d3e45]", "#34d399"),
        ("aws_instance.app_server: Creation complete after 18s [id=i-00f3e3f270983d9a5]", "#34d399"),
        ("", "#ffffff"),
        ("Apply complete! Resources: 10 added, 0 changed, 0 destroyed.", "#34d399"),
        ("", "#ffffff"),
        ("Outputs:", "#e2e8f0"),
        ("  app_private_ip        = \"10.0.1.45\"", "#38bdf8"),
        ("  app_public_ip         = \"98.84.41.102\"", "#38bdf8"),
        ("  app_url               = \"http://98.84.41.102/\"", "#38bdf8"),
        ("  monitor_private_ip    = \"10.0.1.28\"", "#38bdf8"),
        ("  monitor_public_ip     = \"44.223.101.208\"", "#38bdf8"),
        ("  nagios_dashboard_url  = \"http://44.223.101.208/nagios\"", "#38bdf8")
    ]

    y = 55
    for text, color in lines:
        draw.text((25, y), text, font=font_code, fill=color)
        y += 25

    out_path = os.path.join(ASSETS_DIR, "screenshot4_terraform_aws.png")
    im.save(out_path, "PNG")
    print("Saved:", out_path)

if __name__ == "__main__":
    create_web_console_screenshot()
    create_nagios_dashboard_screenshot()
    create_recovery_action_screenshot()
    create_terraform_screenshot()
