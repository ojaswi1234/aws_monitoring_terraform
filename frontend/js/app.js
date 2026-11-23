// DevOps Self-Healing Interactive Dashboard Controller

function addLog(message, type = "info") {
    const logBox = document.getElementById("event-log");
    const entry = document.createElement("div");
    entry.className = `log-entry ${type}`;
    const timestamp = new Date().toLocaleTimeString();
    entry.textContent = `[${timestamp}] ${message}`;
    logBox.appendChild(entry);
    logBox.scrollTop = logBox.scrollHeight;
}

async function fetchEndpoint(path) {
    const viewer = document.getElementById("json-output");
    viewer.textContent = `Fetching ${path}...`;
    try {
        const response = await fetch(path);
        const data = await response.json();
        viewer.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        viewer.textContent = `Error fetching ${path}: ${err.message}`;
    }
}

async function refreshStatus() {
    try {
        const res = await fetch("/healthz");
        const liveBadge = document.getElementById("liveness-badge");
        const readyBadge = document.getElementById("readiness-badge");
        const globalPulse = document.getElementById("global-pulse");
        const globalText = document.getElementById("global-status-text");
        const appBadge = document.getElementById("app-instance-badge");

        if (res.ok) {
            const data = await res.json();
            liveBadge.textContent = "ALIVE (200 OK)";
            liveBadge.className = "badge ok";
            readyBadge.textContent = "READY (200 OK)";
            readyBadge.className = "badge ok";
            globalPulse.className = "pulse-dot";
            globalText.textContent = "SYSTEM OPERATIONAL";
            appBadge.textContent = "RUNNING";
            appBadge.className = "badge ok";
        } else {
            liveBadge.textContent = `CRITICAL (${res.status} FAIL)`;
            liveBadge.className = "badge fail";
            readyBadge.textContent = "DEGRADED (503)";
            readyBadge.className = "badge fail";
            globalPulse.className = "pulse-dot danger";
            globalText.textContent = "SERVICE DEGRADED - CRITICAL";
            appBadge.textContent = "SERVICE DOWN";
            appBadge.className = "badge fail";
        }
    } catch (err) {
        const liveBadge = document.getElementById("liveness-badge");
        liveBadge.textContent = "OFFLINE";
        liveBadge.className = "badge fail";
    }

    // Fetch live uptime
    try {
        const statusRes = await fetch("/api/v1/status");
        if (statusRes.ok) {
            const data = await statusRes.json();
            document.getElementById("uptime-val").textContent = `${data.uptime_seconds}s`;
        }
    } catch (e) {}
}

async function simulateCrash() {
    addLog("💥 INITIATING SIMULATED FAILURE: Stopping Gunicorn / Flask backend...", "warning");
    try {
        const res = await fetch("/api/v1/simulate/crash", { method: "POST" });
        const data = await res.json();
        fetchEndpoint("/healthz");

        setTimeout(() => {
            addLog("[NAGIOS CHECK] GET /healthz failed -> HTTP 503 CRITICAL (Attempt 1/3 - SOFT)", "critical");
        }, 800);

        setTimeout(() => {
            addLog("[NAGIOS CHECK] GET /healthz failed -> HTTP 503 CRITICAL (Attempt 3/3 - HARD CRITICAL)", "critical");
            addLog("🚨 NAGIOS ALERT: Service 'Flask Backend Health' transitioned to HARD CRITICAL state!", "critical");
            refreshStatus();
        }, 1800);

    } catch (err) {
        addLog(`Simulation error: ${err.message}`, "critical");
    }
}

async function triggerRecovery() {
    addLog("⚡ SELF-HEALING TRIGGER: Nagios Event Handler invoked (/usr/local/bin/recover_flask.sh)", "info");
    
    setTimeout(() => {
        addLog("[EVENT HANDLER] State=CRITICAL, Type=HARD confirmed. Executing Ansible recover_flask.yml...", "info");
    }, 700);

    setTimeout(() => {
        addLog("[ANSIBLE] Connecting to app-server (10.0.1.60) via private VPC SSH...", "info");
    }, 1400);

    setTimeout(() => {
        addLog("[ANSIBLE] Task: Restarting flask-backend.service via systemd [CHANGED]", "warning");
    }, 2200);

    setTimeout(async () => {
        try {
            await fetch("/api/v1/simulate/recover", { method: "POST" });
            addLog("[ANSIBLE] Task: Probing 127.0.0.1:8000/healthz -> HTTP 200 OK [RESTORED]", "success");
            addLog("🎉 SELF-HEALING SUCCESS: Nagios check verified service restored to OK!", "success");
            refreshStatus();
            fetchEndpoint("/healthz");
        } catch (e) {}
    }, 3000);
}

// Auto-refresh periodically
document.addEventListener("DOMContentLoaded", () => {
    refreshStatus();
    setInterval(refreshStatus, 4000);
});
