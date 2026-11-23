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
    // Check liveness
    try {
        const liveRes = await fetch("/healthz");
        const liveBadge = document.getElementById("liveness-badge");
        if (liveRes.ok) {
            const data = await liveRes.json();
            liveBadge.textContent = "ALIVE (200 OK)";
            liveBadge.className = "badge ok";
            document.getElementById("service-name").textContent = data.service || "python-backend";
        } else {
            liveBadge.textContent = `FAIL (${liveRes.status})`;
            liveBadge.className = "badge fail";
        }
    } catch (e) {
        const liveBadge = document.getElementById("liveness-badge");
        liveBadge.textContent = "OFFLINE";
        liveBadge.className = "badge fail";
    }

    // Check readiness
    try {
        const readyRes = await fetch("/readyz");
        const readyBadge = document.getElementById("readiness-badge");
        if (readyRes.ok) {
            readyBadge.textContent = "READY (200 OK)";
            readyBadge.className = "badge ok";
        } else {
            readyBadge.textContent = `UNREADY (${readyRes.status})`;
            readyBadge.className = "badge warn";
        }
    } catch (e) {
        const readyBadge = document.getElementById("readiness-badge");
        readyBadge.textContent = "DOWN";
        readyBadge.className = "badge fail";
    }

    // Check status & uptime
    try {
        const statusRes = await fetch("/api/v1/status");
        if (statusRes.ok) {
            const data = await statusRes.json();
            document.getElementById("uptime-val").textContent = `${data.uptime_seconds}s`;
        }
    } catch (e) {}
}

// Initial refresh and periodic polling every 5 seconds
document.addEventListener("DOMContentLoaded", () => {
    refreshStatus();
    setInterval(refreshStatus, 5000);
});
