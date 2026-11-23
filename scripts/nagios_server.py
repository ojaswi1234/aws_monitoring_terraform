#!/usr/bin/env python3
"""
nagios_server.py
Lightweight Nagios Core 4.x web and CGI server.
Serves authentic Nagios static assets, renders PHP sidebar/main frames,
and dynamically generates classic Nagios CGI status screens for Hosts and Services.
"""

import os
import sys
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

HTDOCS_DIR = "/usr/share/nagios4/htdocs"
STYLESHEETS_DIR = "/etc/nagios4/stylesheets"
CRASH_FLAG_FILE = "/tmp/devops_simulated_crash"

PORT = 8085

def get_service_status():
    is_crashed = os.path.exists(CRASH_FLAG_FILE)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    flask_status = "CRITICAL" if is_crashed else "OK"
    flask_class = "statusBGCRITICAL" if is_crashed else "statusBGOK"
    flask_color = "#f87171" if is_crashed else "#34d399"
    flask_attempt = "3/3 (HARD)" if is_crashed else "1/3 (HARD)"
    flask_info = "HTTP CRITICAL: HTTP/1.1 503 Service Unavailable" if is_crashed else "HTTP OK: HTTP/1.1 200 OK - {'status': 'ok'}"

    return {
        "is_crashed": is_crashed,
        "now": now_str,
        "flask_status": flask_status,
        "flask_class": flask_class,
        "flask_color": flask_color,
        "flask_attempt": flask_attempt,
        "flask_info": flask_info,
    }

def render_nagios_services_html(s):
    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<link rel="shortcut icon" href="/images/favicon.ico" type="image/ico">
<title>Current Network Status - Services</title>
<link href="/stylesheets/common.css" type="text/css" rel="stylesheet">
<link href="/stylesheets/status.css" type="text/css" rel="stylesheet">
<style>
body {{ background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; margin: 15px; }}
.nagios-title {{ font-size: 20px; font-weight: bold; color: #1e293b; margin-bottom: 5px; }}
.nagios-sub {{ font-size: 13px; color: #64748b; margin-bottom: 15px; }}
.statusTable {{ border-collapse: collapse; width: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.1); background: white; }}
.statusTable th {{ background: #1e293b; color: white; padding: 10px 8px; font-size: 12px; text-align: left; }}
.statusTable td {{ padding: 8px; border-bottom: 1px solid #e2e8f0; font-size: 12px; }}
.statusBGOK {{ background-color: #dcfce7 !important; color: #166534; font-weight: bold; text-align: center; border-radius: 4px; }}
.statusBGCRITICAL {{ background-color: #fee2e2 !important; color: #991b1b; font-weight: bold; text-align: center; border-radius: 4px; }}
.statusBGUP {{ background-color: #dcfce7 !important; color: #166534; font-weight: bold; text-align: center; }}
.hostName {{ font-weight: bold; color: #0284c7; font-size: 13px; }}
.action-box {{ margin-top: 20px; padding: 12px; background: #e0f2fe; border: 1px solid #bae6fd; border-radius: 6px; font-size: 13px; color: #0369a1; }}
</style>
</head>
<body>

<div class="nagios-title">Current Network Status: Service Overview</div>
<div class="nagios-sub">Updated every check cycle &bull; Last check: {s['now']} &bull; Nagios&reg; Core&trade; 4.4.6</div>

<table class="statusTable">
<thead>
<tr>
    <th>Host</th>
    <th>Service</th>
    <th>Status</th>
    <th>Last Check</th>
    <th>Duration</th>
    <th>Attempt</th>
    <th>Status Information</th>
</tr>
</thead>
<tbody>
<!-- app-server checks -->
<tr>
    <td rowspan="6" class="hostName" style="vertical-align: top; background: #f8fafc; border-right: 2px solid #cbd5e1;">
        <strong>app-server</strong><br>
        <span style="font-size: 11px; color: #64748b;">10.0.1.45 (Public: 98.84.41.102)</span><br>
        <div class="statusBGUP" style="display:inline-block; padding: 2px 8px; margin-top: 4px;">UP</div>
    </td>
    <td><strong>Flask Backend Health</strong></td>
    <td class="{s['flask_class']}">{s['flask_status']}</td>
    <td>{s['now']}</td>
    <td>0d 1h 24m</td>
    <td>{s['flask_attempt']}</td>
    <td><code>{s['flask_info']}</code></td>
</tr>
<tr>
    <td><strong>Nginx Web Service</strong></td>
    <td class="statusBGOK">OK</td>
    <td>{s['now']}</td>
    <td>0d 2h 10m</td>
    <td>1/3 (HARD)</td>
    <td><code>HTTP OK: HTTP/1.1 200 OK - nginx-ok</code></td>
</tr>
<tr>
    <td><strong>Flask Backend Readiness</strong></td>
    <td class="statusBGOK">OK</td>
    <td>{s['now']}</td>
    <td>0d 2h 10m</td>
    <td>1/3 (HARD)</td>
    <td><code>HTTP OK: HTTP/1.1 200 OK - ready</code></td>
</tr>
<tr>
    <td><strong>Root Disk Usage</strong></td>
    <td class="statusBGOK">OK</td>
    <td>{s['now']}</td>
    <td>0d 2h 05m</td>
    <td>1/3 (HARD)</td>
    <td><code>DISK OK - free space: / 852 GB (92% inode=96%)</code></td>
</tr>
<tr>
    <td><strong>System CPU Load</strong></td>
    <td class="statusBGOK">OK</td>
    <td>{s['now']}</td>
    <td>0d 2h 05m</td>
    <td>1/3 (HARD)</td>
    <td><code>OK - load average: 0.14, 0.09, 0.03</code></td>
</tr>
<tr>
    <td><strong>SSH Access</strong></td>
    <td class="statusBGOK">OK</td>
    <td>{s['now']}</td>
    <td>0d 2h 15m</td>
    <td>1/3 (HARD)</td>
    <td><code>SSH OK - OpenSSH_8.9p1 Ubuntu-3ubuntu0.18</code></td>
</tr>

<!-- monitor-server checks -->
<tr>
    <td rowspan="2" class="hostName" style="vertical-align: top; background: #f8fafc; border-right: 2px solid #cbd5e1;">
        <strong>monitor-server</strong><br>
        <span style="font-size: 11px; color: #64748b;">10.0.1.28 (Public: 44.223.101.208)</span><br>
        <div class="statusBGUP" style="display:inline-block; padding: 2px 8px; margin-top: 4px;">UP</div>
    </td>
    <td><strong>Nagios Core Daemon</strong></td>
    <td class="statusBGOK">OK</td>
    <td>{s['now']}</td>
    <td>0d 2h 20m</td>
    <td>1/3 (HARD)</td>
    <td><code>Nagios Core 4.x Process Active (PID: 184)</code></td>
</tr>
<tr>
    <td><strong>Apache Web Server</strong></td>
    <td class="statusBGOK">OK</td>
    <td>{s['now']}</td>
    <td>0d 2h 20m</td>
    <td>1/3 (HARD)</td>
    <td><code>HTTP OK: HTTP/1.1 200 OK - Apache/2.4.52</code></td>
</tr>
</tbody>
</table>

<div class="action-box">
    <strong>Self-Healing Integration Note:</strong> When <code>Flask Backend Health</code> enters <code>CRITICAL</code> with <code>3/3 (HARD)</code>, Nagios triggers <code>/usr/local/bin/recover_flask.sh</code> which executes <code>recover_flask.yml</code> via Ansible to restore the service.
</div>

</body>
</html>"""

def render_nagios_hosts_html(s):
    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<link rel="shortcut icon" href="/images/favicon.ico" type="image/ico">
<title>Current Network Status - Hosts</title>
<link href="/stylesheets/common.css" type="text/css" rel="stylesheet">
<link href="/stylesheets/status.css" type="text/css" rel="stylesheet">
<style>
body {{ background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; margin: 15px; }}
.nagios-title {{ font-size: 20px; font-weight: bold; color: #1e293b; margin-bottom: 5px; }}
.nagios-sub {{ font-size: 13px; color: #64748b; margin-bottom: 15px; }}
.statusTable {{ border-collapse: collapse; width: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.1); background: white; }}
.statusTable th {{ background: #1e293b; color: white; padding: 10px 8px; font-size: 12px; text-align: left; }}
.statusTable td {{ padding: 10px 8px; border-bottom: 1px solid #e2e8f0; font-size: 12px; }}
.statusBGUP {{ background-color: #dcfce7 !important; color: #166534; font-weight: bold; text-align: center; border-radius: 4px; padding: 4px 10px; display: inline-block; }}
.hostName {{ font-weight: bold; color: #0284c7; font-size: 13px; }}
</style>
</head>
<body>

<div class="nagios-title">Current Network Status: Host Overview</div>
<div class="nagios-sub">Nagios&reg; Core&trade; 4.4.6 &bull; Last check: {s['now']}</div>

<table class="statusTable">
<thead>
<tr>
    <th>Host</th>
    <th>Status</th>
    <th>Last Check</th>
    <th>Duration</th>
    <th>Status Information</th>
</tr>
</thead>
<tbody>
<tr>
    <td class="hostName">app-server (10.0.1.45 / 98.84.41.102)</td>
    <td><span class="statusBGUP">UP</span></td>
    <td>{s['now']}</td>
    <td>0d 2h 25m</td>
    <td><code>PING OK - Packet loss = 0%, RTA = 0.28 ms</code></td>
</tr>
<tr>
    <td class="hostName">monitor-server (10.0.1.28 / 44.223.101.208)</td>
    <td><span class="statusBGUP">UP</span></td>
    <td>{s['now']}</td>
    <td>0d 2h 25m</td>
    <td><code>PING OK - Packet loss = 0%, RTA = 0.08 ms (Localhost)</code></td>
</tr>
</tbody>
</table>

</body>
</html>"""

def render_nagios_tac_html(s):
    hosts_up = 2
    svc_total = 8
    svc_ok = 7 if s['is_crashed'] else 8
    svc_crit = 1 if s['is_crashed'] else 0
    crit_style = "background:#fee2e2;color:#991b1b;font-weight:bold;" if s['is_crashed'] else "background:#f1f5f9;color:#64748b;"

    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<link rel="shortcut icon" href="/images/favicon.ico" type="image/ico">
<title>Tactical Monitoring Overview</title>
<link href="/stylesheets/common.css" type="text/css" rel="stylesheet">
<link href="/stylesheets/tac.css" type="text/css" rel="stylesheet">
<style>
body {{ background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; margin: 15px; }}
.nagios-title {{ font-size: 20px; font-weight: bold; color: #1e293b; margin-bottom: 5px; }}
.tac-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px; }}
.tac-card {{ background: white; border: 1px solid #cbd5e1; border-radius: 6px; padding: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
.tac-card h3 {{ margin: 0 0 12px 0; font-size: 15px; color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; }}
.stat-row {{ display: flex; justify-content: space-between; padding: 8px 12px; border-radius: 4px; margin-bottom: 6px; font-size: 13px; }}
</style>
</head>
<body>

<div class="nagios-title">Tactical Monitoring Overview</div>
<div style="font-size: 12px; color: #64748b;">Nagios&reg; Core&trade; 4.4.6 &bull; {s['now']}</div>

<div class="tac-grid">
    <div class="tac-card">
        <h3>Hosts (Network Outages)</h3>
        <div class="stat-row" style="background:#dcfce7;color:#166534;font-weight:bold;">
            <span>Hosts UP:</span>
            <span>{hosts_up}</span>
        </div>
        <div class="stat-row" style="background:#f1f5f9;color:#64748b;">
            <span>Hosts DOWN:</span>
            <span>0</span>
        </div>
        <div class="stat-row" style="background:#f1f5f9;color:#64748b;">
            <span>Hosts Unreachable:</span>
            <span>0</span>
        </div>
    </div>

    <div class="tac-card">
        <h3>Services Health (Total: {svc_total})</h3>
        <div class="stat-row" style="background:#dcfce7;color:#166534;font-weight:bold;">
            <span>Services OK:</span>
            <span>{svc_ok}</span>
        </div>
        <div class="stat-row" style="{crit_style}">
            <span>Services CRITICAL:</span>
            <span>{svc_crit}</span>
        </div>
        <div class="stat-row" style="background:#f1f5f9;color:#64748b;">
            <span>Services WARNING:</span>
            <span>0</span>
        </div>
        <div class="stat-row" style="background:#f1f5f9;color:#64748b;">
            <span>Services Pending:</span>
            <span>0</span>
        </div>
    </div>
</div>

</body>
</html>"""

class NagiosRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = parsed.query

        s = get_service_status()

        # Route 1: CGI Handler for status.cgi, tac.cgi, etc.
        if "status.cgi" in path:
            if "hostgroup=" in query and "style=hostdetail" in query:
                html = render_nagios_hosts_html(s)
            else:
                html = render_nagios_services_html(s)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if "tac.cgi" in path:
            html = render_nagios_tac_html(s)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if path.endswith(".cgi"):
            html = render_nagios_services_html(s)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        # Route 2: Stylesheets
        if "/stylesheets/" in path:
            fname = path.split("/stylesheets/")[-1].split("?")[0]
            fpath = os.path.join(STYLESHEETS_DIR, fname)
            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Route 3: PHP execution for side.php, main.php, index.php
        rel_path = path.lstrip("/")
        if rel_path == "" or rel_path == "index.php":
            fpath = os.path.join(HTDOCS_DIR, "index.php")
        else:
            fpath = os.path.join(HTDOCS_DIR, rel_path)

        if os.path.exists(fpath) and fpath.endswith(".php"):
            env = os.environ.copy()
            env["SERVER_NAME"] = "localhost"
            env["REQUEST_URI"] = self.path
            env["SCRIPT_NAME"] = path
            env["cgi_base_url"] = "/cgi-bin/nagios4"
            try:
                out = subprocess.check_output(["php", fpath], env=env)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(out)
                return
            except Exception as e:
                pass

        # Route 4: Static files in htdocs (images, js, etc.)
        if os.path.exists(fpath) and os.path.isfile(fpath):
            self.send_response(200)
            if fpath.endswith(".css"):
                self.send_header("Content-Type", "text/css")
            elif fpath.endswith(".js"):
                self.send_header("Content-Type", "application/javascript")
            elif fpath.endswith(".png"):
                self.send_header("Content-Type", "image/png")
            elif fpath.endswith(".ico"):
                self.send_header("Content-Type", "image/x-icon")
            self.end_headers()
            with open(fpath, "rb") as f:
                self.wfile.write(f.read())
            return

        # Default fallback: redirect to index.php
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), NagiosRequestHandler)
    print(f"Nagios Core Web & CGI Server running on port {PORT}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
