// DevOps Self-Healing Interactive Dashboard Controller

function addLog(message, type = "info") {
    const logBox = document.getElementById("event-log");
    if (!logBox) return;
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

async function loadInfrastructure() {
    try {
        const res = await fetch("/api/v1/infrastructure");
        if (!res.ok) return;
        const data = await res.json();

        if (data.region && data.vpc_id) {
            const pill = document.getElementById("aws-region-pill");
            if (pill) pill.textContent = `Region: ${data.region} | VPC: ${data.vpc_id}`;
        }

        if (Array.isArray(data.instances)) {
            const monitor = data.instances.find(i => i.role.includes("Nagios") || i.name.includes("monitor"));
            const app = data.instances.find(i => i.role.includes("Nginx") || i.name.includes("app"));

            if (monitor) {
                const elId = document.getElementById("monitor-id");
                const elPriv = document.getElementById("monitor-private-ip");
                const elPub = document.getElementById("monitor-public-ip");
                const elSg = document.getElementById("monitor-sg");
                const elLink = document.getElementById("monitor-live-link");
                const navLink = document.getElementById("nav-aws-nagios");

                if (elId) elId.textContent = monitor.id;
                if (elPriv) elPriv.textContent = monitor.private_ip;
                if (elPub) elPub.textContent = monitor.public_ip;
                if (elSg) elSg.textContent = monitor.security_group;
                if (elLink) elLink.href = `http://${monitor.public_ip}/nagios`;
                if (navLink) navLink.href = `http://${monitor.public_ip}/nagios`;
            }

            if (app) {
                const elId = document.getElementById("app-id");
                const elPriv = document.getElementById("app-private-ip");
                const elPub = document.getElementById("app-public-ip");
                const elSg = document.getElementById("app-sg");
                const elLink = document.getElementById("app-live-link");

                if (elId) elId.textContent = app.id;
                if (elPriv) elPriv.textContent = app.private_ip;
                if (elPub) elPub.textContent = app.public_ip;
                if (elSg) elSg.textContent = app.security_group;
                if (elLink) elLink.href = `http://${app.public_ip}/`;
            }
        }
    } catch (err) {
        console.warn("Could not load infrastructure metadata:", err);
    }
}

async function refreshStatus(isManual = false) {
    const liveBadge = document.getElementById("liveness-badge");
    const readyBadge = document.getElementById("readiness-badge");
    const globalPulse = document.getElementById("global-pulse");
    const globalText = document.getElementById("global-status-text");
    const appBadge = document.getElementById("app-instance-badge");

    try {
        const res = await fetch("/healthz");
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
            if (isManual) {
                addLog("[HEALTH PROBE] GET /healthz -> 200 OK. System fully operational.", "success");
            }
        } else {
            const data = await res.json().catch(() => ({}));
            liveBadge.textContent = `CRITICAL (${res.status} FAIL)`;
            liveBadge.className = "badge fail";
            readyBadge.textContent = "DEGRADED (503)";
            readyBadge.className = "badge fail";
            globalPulse.className = "pulse-dot danger";
            globalText.textContent = "SERVICE CRITICAL (503)";
            appBadge.textContent = "SERVICE DEGRADED";
            appBadge.className = "badge fail";
            if (isManual) {
                addLog(`[HEALTH PROBE] GET /healthz -> ${res.status} CRITICAL. Service failure detected.`, "critical");
            }
        }
    } catch (err) {
        liveBadge.textContent = "OFFLINE";
        liveBadge.className = "badge fail";
        readyBadge.textContent = "UNREACHABLE";
        readyBadge.className = "badge fail";
        globalPulse.className = "pulse-dot danger";
        globalText.textContent = "SERVER OFFLINE";
        if (isManual) {
            addLog(`[NETWORK ERROR] Could not reach backend: ${err.message}`, "critical");
        }
    }

    // Fetch live uptime and metrics
    try {
        const statusRes = await fetch("/api/v1/status");
        if (statusRes.ok) {
            const data = await statusRes.json();
            const uptimeEl = document.getElementById("uptime-val");
            if (uptimeEl) uptimeEl.textContent = `${data.uptime_seconds}s`;
        }
    } catch (e) {}
}

async function simulateCrash() {
    addLog("💥 INITIATING CRASH: Sending failure signal to backend...", "warning");
    try {
        const res = await fetch("/api/v1/simulate/crash", { method: "POST" });
        const data = await res.json();
        addLog(`[BACKEND EVENT] ${data.message}`, "warning");

        // Immediately probe /healthz to show real failing state
        await refreshStatus(false);
        addLog("🚨 NAGIOS PROBE: GET /healthz failed with HTTP 503 Service Unavailable [CRITICAL]", "critical");
        fetchEndpoint("/healthz");
    } catch (err) {
        addLog(`Simulation error: ${err.message}`, "critical");
    }
}

async function triggerRecovery(useAnsible = false) {
    const actionDesc = useAnsible ? "Ansible recovery playbook (recover_flask.yml)" : "Self-healing event handler";
    addLog(`⚡ TRIGGERING RECOVERY: Invoking ${actionDesc}...`, "info");

    try {
        const url = useAnsible ? "/api/v1/simulate/recover?ansible=true" : "/api/v1/simulate/recover";
        const res = await fetch(url, { method: "POST" });
        const data = await res.json();

        if (data.ansible_summary) {
            addLog(`[ANSIBLE SUMMARY] ${data.ansible_summary}`, "info");
        }
        addLog(`[RECOVERY EVENT] ${data.message}`, "success");

        // Probe /healthz to verify real recovery
        await refreshStatus(false);
        addLog("🎉 VERIFICATION SUCCESS: GET /healthz returned HTTP 200 OK. State restored to OK!", "success");
        fetchEndpoint("/healthz");
    } catch (err) {
        addLog(`Recovery error: ${err.message}`, "critical");
    }
}

// Auto-refresh periodically and load infrastructure
document.addEventListener("DOMContentLoaded", () => {
    loadInfrastructure();
    refreshStatus(false);
    setInterval(() => refreshStatus(false), 5000);
});
