document.addEventListener("DOMContentLoaded", () => {

    // --- DOM Elements ---
    const focusSlider = document.getElementById("focus-slider");
    const focusPct = document.getElementById("focus-pct");
    const driveStatus = document.getElementById("drive-status");
    const driveCoherence = document.getElementById("drive-coherence");
    const driveThrust = document.getElementById("drive-thrust");
    const frameIntegrity = document.getElementById("frame-integrity");
    const frameMaterial = document.getElementById("frame-material");
    const frameStealth = document.getElementById("frame-stealth");
    const clockEl = document.getElementById("clock");
    const footerTime = document.getElementById("footer-time");
    const btnHF = document.getElementById("btn-hf-field");
    const btnBase = document.getElementById("btn-base");
    const auraLogContainer = document.getElementById("aura-messages");

    // Intelligence Elements
    const orbitalBar = document.getElementById("orbital-bar");
    const orbitalPct = document.getElementById("orbital-pct");
    const etaLeo = document.getElementById("eta-leo");
    const intelAlt = document.getElementById("intel-alt");
    const intelVel = document.getElementById("intel-vel");
    const intelStatus = document.getElementById("intel-status");

    let spokenMessages = new Set();

    // --- Clock ---
    function updateClock() {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString("pt-BR");
        footerTime.textContent = now.toLocaleDateString("pt-BR");
    }
    setInterval(updateClock, 1000);
    updateClock();

    // --- Chart.js Config ---
    const CHART_MAX_POINTS = 40;

    function makeLineDataset(label, color) {
        return {
            label,
            data: [],
            borderColor: color,
            borderWidth: 2,
            pointRadius: 0,
            fill: true,
            backgroundColor: color.replace(')', ', 0.08)').replace('rgb', 'rgba'),
            tension: 0.4,
        };
    }

    const commonOptions = {
        animation: false,
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            x: { display: false },
            y: {
                display: true,
                grid: { color: 'rgba(255,255,255,0.04)' },
                ticks: { color: '#4a5a7a', font: { size: 9 } }
            }
        }
    };

    // Thrust Chart
    const thrustChart = new Chart(document.getElementById("thrustChart"), {
        type: 'line',
        data: { labels: [], datasets: [makeLineDataset("Thrust kN", "rgb(0, 212, 255)")] },
        options: { ...commonOptions, scales: { ...commonOptions.scales, y: { ...commonOptions.scales.y, min: 0 } } }
    });

    // Integrity Chart
    const integrityChart = new Chart(document.getElementById("integrityChart"), {
        type: 'line',
        data: { labels: [], datasets: [makeLineDataset("Integrity %", "rgb(0, 255, 136)")] },
        options: { ...commonOptions, scales: { ...commonOptions.scales, y: { ...commonOptions.scales.y, min: 0, max: 100 } } }
    });

    // Coherence mini chart
    const coherenceChart = new Chart(document.getElementById("coherenceChart"), {
        type: 'bar',
        data: {
            labels: [], datasets: [{
                data: [],
                backgroundColor: 'rgba(0, 212, 255, 0.35)',
                borderColor: 'rgb(0, 212, 255)',
                borderWidth: 1,
                borderRadius: 2,
            }]
        },
        options: {
            animation: false,
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { display: false },
                y: { display: false, min: 0, max: 100 }
            }
        }
    });

    // G-Force Doughnut
    const gForceChart = new Chart(document.getElementById("gForceChart"), {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [1, 9],
                backgroundColor: ['rgb(0, 212, 255)', 'rgba(255,255,255,0.04)'],
                borderWidth: 0,
                circumference: 270,
                rotation: -135
            }]
        },
        options: {
            animation: { duration: 300 },
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            cutout: '78%'
        }
    });

    function pushToChart(chart, value) {
        const ts = new Date().toLocaleTimeString("pt-BR");
        if (chart.data.labels.length >= CHART_MAX_POINTS) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
        chart.data.labels.push(ts);
        chart.data.datasets[0].data.push(value);
        chart.update('none');
    }

    function updateGForce(g) {
        const clamped = Math.min(Math.max(g, 0), 10);
        gForceChart.data.datasets[0].data = [clamped, 10 - clamped];

        // Color changes by G level
        let color = 'rgb(0, 212, 255)';
        if (clamped > 6) color = 'rgb(255, 45, 85)';
        else if (clamped > 4) color = 'rgb(255, 165, 0)';
        gForceChart.data.datasets[0].backgroundColor[0] = color;
        gForceChart.update('none');
    }

    // --- API Calls ---
    async function postJSON(url, data) {
        const r = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        return r.json();
    }

    async function fetchTelemetry() {
        try {
            const data = await (await fetch("/api/telemetry/")).json();
            updateDashboard(data);
        } catch (e) { /* silent fail */ }
    }

    function updateDashboard(data) {
        if (data.drive) {
            const d = data.drive;
            const online = d.status === "ONLINE";
            driveStatus.textContent = d.status;
            driveStatus.className = "metric-value " + (online ? "status-online" : "status-standby");
            driveCoherence.textContent = d.coherence.toFixed(1) + "%";
            driveThrust.textContent = d.thrust.toFixed(2);
            pushToChart(thrustChart, d.thrust);
            pushToChart(coherenceChart, d.coherence);

            // Estimated G-Force from thrust (F = ma, m~4.85kg)
            const g = (d.thrust * 1000 / 4.85) / 9.8;
            updateGForce(g);
        }

        if (data.airframe) {
            const a = data.airframe;
            const pct = a.integrity.toFixed(1) + "%";
            frameIntegrity.textContent = pct;
            frameMaterial.textContent = a.material;

            if (a.active_stealth) {
                frameStealth.textContent = "ACTIVE";
                frameStealth.className = "metric-value stealth-on";
                document.body.classList.add("stealth-mode");
            } else {
                frameStealth.textContent = "INACTIVE";
                frameStealth.className = "metric-value stealth-off";
                document.body.classList.remove("stealth-mode");
            }
            pushToChart(integrityChart, a.integrity);
        }

        if (data.aura_messages) {
            updateAuraLog(data.aura_messages);
        }

        if (data.intelligence) {
            updateIntelligenceUI(data.intelligence);
        }
    }

    function updateIntelligenceUI(intel) {
        // Progress Bar
        const pct = intel.insertion_progress.toFixed(1) + "%";
        orbitalPct.textContent = pct;
        orbitalBar.style.width = pct;

        // Metrics
        intelAlt.textContent = (intel.altitude_m / 1000).toFixed(2); // Show in km
        intelVel.textContent = intel.velocity_ms.toFixed(0);
        intelStatus.textContent = intel.status;
        etaLeo.textContent = "ETA: " + intel.eta_leo;

        // Color coding for status
        if (intel.status === "ORBITAL_STABLE") {
            intelStatus.className = "metric-value status-online";
        } else if (intel.status === "CRITICAL") {
            intelStatus.className = "metric-value status-standby";
        } else {
            intelStatus.className = "metric-value status-online";
        }
    }

    function updateAuraLog(messages) {
        messages.forEach(msg => {
            const msgId = msg.timestamp + msg.message;
            if (!spokenMessages.has(msgId)) {
                // Add to UI
                const msgDiv = document.createElement("div");
                msgDiv.className = "aura-msg" + (msg.priority === 'high' ? ' high-priority' : '');
                msgDiv.innerHTML = `<span class="time">[${msg.timestamp}]</span> <span class="txt">${msg.message}</span>`;
                auraLogContainer.appendChild(msgDiv);

                // Scroll to bottom
                auraLogContainer.scrollTop = auraLogContainer.scrollHeight;

                // Voice Narration
                speakAura(msg.message);

                spokenMessages.add(msgId);

                // Limit memory
                if (spokenMessages.size > 50) spokenMessages.clear();
            }
        });
    }

    function speakAura(text) {
        if (!window.speechSynthesis) return;

        // Cancel any pending speech to avoid backlog
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "pt-BR"; // Native language for Aura
        utterance.pitch = 0.9;    // Slightly deeper, more authoritative
        utterance.rate = 1.0;
        utterance.volume = 0.8;

        window.speechSynthesis.speak(utterance);
    }

    // --- Controls ---
    focusSlider.addEventListener("input", async (e) => {
        const pct = parseInt(e.target.value);
        focusPct.textContent = pct + "%";
        const coherence = pct / 100;
        const result = await postJSON("/api/set_focus/", { focus: coherence });
        if (result.drive) updateDashboard({ drive: result.drive });
    });

    btnHF.addEventListener("click", async () => {
        const result = await postJSON("/api/set_frequency/", { frequency: "high_freq_field" });
        if (result.airframe) updateDashboard({ airframe: result.airframe });
    });

    btnBase.addEventListener("click", async () => {
        const result = await postJSON("/api/set_frequency/", { frequency: "base_state" });
        if (result.airframe) updateDashboard({ airframe: result.airframe });
    });

    // --- Telemetry loop ---
    fetchTelemetry();
    setInterval(fetchTelemetry, 800);
});
