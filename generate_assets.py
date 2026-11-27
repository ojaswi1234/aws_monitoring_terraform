import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ASSETS_DIR = "/home/ob/devops-self-healing-project/report_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_architecture_diagram():
    # 10 x 5.8 inches for a well-proportioned landscape diagram
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background AWS Cloud VPC
    vpc = patches.FancyBboxPatch((2, 2), 96, 96, boxstyle="round,pad=1.5",
                                ec="#2563eb", fc="#f8fafc", lw=2, linestyle="--")
    ax.add_patch(vpc)
    ax.text(5, 93, "AWS Dedicated Virtual Private Cloud (VPC: 10.0.0.0/16) - us-east-1", 
            fontsize=11.5, fontweight='bold', color="#1e40af")

    # Public Subnet
    subnet = patches.FancyBboxPatch((5, 6), 90, 84, boxstyle="round,pad=1.2",
                                   ec="#0284c7", fc="#f0f9ff", lw=1.5)
    ax.add_patch(subnet)
    ax.text(8, 86, "Public Subnet (10.0.1.0/24) | Route Table & Internet Gateway Attached", 
            fontsize=10, fontweight='bold', color="#0369a1")

    # ----------------- Monitor Server EC2 -----------------
    mon_box = patches.FancyBboxPatch((8, 12), 38, 70, boxstyle="round,pad=0.8",
                                     ec="#334155", fc="#ffffff", lw=1.5)
    ax.add_patch(mon_box)
    ax.text(10, 77.5, "Monitoring Server (EC2 t2.micro)", fontsize=9.5, fontweight='bold', color="#0f172a")
    ax.text(10, 74.5, "Private IP: 10.0.1.28 | Public IP: 44.223.101.208", fontsize=8, color="#64748b")
    ax.text(10, 71.5, "Instance ID: i-0839b0eeb087d3e45 | SG: monitor-sg", fontsize=8, family="monospace", color="#334155")

    # Components inside Monitor Server
    nagios_box = patches.FancyBboxPatch((10, 51), 34, 16.5, boxstyle="round,pad=0.5", ec="#d97706", fc="#fef3c7", lw=1.2)
    ax.add_patch(nagios_box)
    ax.text(12, 62.5, "Nagios Core 4.x Monitoring Daemon", fontsize=8.5, fontweight='bold', color="#92400e")
    ax.text(12, 58.5, "• Active HTTP Polling (GET /healthz, 10s)", fontsize=7.8, color="#78350f")
    ax.text(12, 55, "• Threshold State Machine: 3/3 HARD CRITICAL", fontsize=7.8, color="#78350f")

    eh_box = patches.FancyBboxPatch((10, 32), 34, 14.5, boxstyle="round,pad=0.5", ec="#dc2626", fc="#fee2e2", lw=1.2)
    ax.add_patch(eh_box)
    ax.text(12, 41.5, "Nagios Event Handler (recover_flask.sh)", fontsize=8.5, fontweight='bold', color="#991b1b")
    ax.text(12, 37.5, "• Filter: State=CRITICAL & Type=HARD", fontsize=7.8, color="#7f1d1d")
    ax.text(12, 34, "• Sudoers Privilege: /etc/sudoers.d/nagios_recovery", fontsize=7.8, color="#7f1d1d")

    ans_box = patches.FancyBboxPatch((10, 15), 34, 13.5, boxstyle="round,pad=0.5", ec="#7c3aed", fc="#f5f3ff", lw=1.2)
    ax.add_patch(ans_box)
    ax.text(12, 23.5, "Ansible Engine (recover_flask.yml)", fontsize=8.5, fontweight='bold', color="#5b21b6")
    ax.text(12, 19.5, "• Automated Playbook Execution via SSH Key", fontsize=7.8, color="#4c1d95")
    ax.text(12, 16, "• Target: app-server (10.0.1.45)", fontsize=7.8, color="#4c1d95")

    # ----------------- Application Server EC2 -----------------
    app_box = patches.FancyBboxPatch((54, 12), 38, 70, boxstyle="round,pad=0.8",
                                    ec="#334155", fc="#ffffff", lw=1.5)
    ax.add_patch(app_box)
    ax.text(56, 77.5, "Application Server (EC2 t2.micro)", fontsize=9.5, fontweight='bold', color="#0f172a")
    ax.text(56, 74.5, "Private IP: 10.0.1.45 | Public IP: 98.84.41.102", fontsize=8, color="#64748b")
    ax.text(56, 71.5, "Instance ID: i-00f3e3f270983d9a5 | SG: app-sg", fontsize=8, family="monospace", color="#334155")

    # Components inside App Server
    nginx_box = patches.FancyBboxPatch((56, 51), 34, 16.5, boxstyle="round,pad=0.5", ec="#16a34a", fc="#dcfce7", lw=1.2)
    ax.add_patch(nginx_box)
    ax.text(58, 62.5, "Nginx Reverse Proxy & Static Host (Port 80)", fontsize=8.5, fontweight='bold', color="#166534")
    ax.text(58, 58.5, "• Edge Routing: /api/*, /healthz, /readyz", fontsize=7.8, color="#14532d")
    ax.text(58, 55, "• Serves Self-Healing Web Management Console", fontsize=7.8, color="#14532d")

    gun_box = patches.FancyBboxPatch((56, 31), 34, 16.5, boxstyle="round,pad=0.5", ec="#0284c7", fc="#e0f2fe", lw=1.2)
    ax.add_patch(gun_box)
    ax.text(58, 42.5, "Gunicorn WSGI + Python Flask 3.x", fontsize=8.5, fontweight='bold', color="#075985")
    ax.text(58, 38.5, "• Service: flask-backend.service (127.0.0.1:8000)", fontsize=7.8, color="#0c4a6e")
    ax.text(58, 35, "• Multi-worker Architecture with Health Probes", fontsize=7.8, color="#0c4a6e")

    nrpe_box = patches.FancyBboxPatch((56, 15), 34, 13.5, boxstyle="round,pad=0.5", ec="#64748b", fc="#f1f5f9", lw=1.2)
    ax.add_patch(nrpe_box)
    ax.text(58, 23.5, "Nagios NRPE Agent (Port 5666)", fontsize=8.5, fontweight='bold', color="#334155")
    ax.text(58, 19.5, "• Local Resource Checks: CPU, Disk, Memory", fontsize=7.8, color="#475569")
    ax.text(58, 16, "• Restricted to Monitoring Server IP (10.0.1.28)", fontsize=7.8, color="#475569")

    # ----------------- Interactive Flow Arrows -----------------
    # 1. Active HTTP Probe (Nagios -> App Server Nginx)
    ax.annotate("", xy=(56, 59.5), xytext=(44, 59.5),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=2.2))
    ax.text(50, 61.5, "1. HTTP /healthz Probe (10s)", fontsize=8, fontweight='bold', color="#b45309", ha="center")

    # 2. Internal Event Trigger (Nagios -> Event Handler -> Ansible)
    ax.annotate("", xy=(27, 29), xytext=(27, 32),
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.8))
    ax.text(28.5, 30.5, "On HARD CRITICAL", fontsize=6.8, color="#991b1b")

    # 3. Remediation Loop via SSH (Ansible -> App Server Systemd)
    ax.annotate("", xy=(56, 38), xytext=(44, 22),
                arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2.2, linestyle="-"))
    ax.text(50, 27, "2. Private VPC SSH (Port 22)\nRemediation Playbook", 
            fontsize=8, fontweight='bold', color="#6d28d9", ha="center")

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "architecture_diagram.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Regenerated Architecture Diagram:", out_path)

if __name__ == "__main__":
    generate_architecture_diagram()
