document.addEventListener("DOMContentLoaded", () => {
    
    // Elements
    const focusSlider = document.getElementById("focus-slider");
    const focusDisplay = document.getElementById("focus-display");
    
    const driveStatus = document.getElementById("drive-status");
    const driveCoherence = document.getElementById("drive-coherence");
    const driveThrust = document.getElementById("drive-thrust");
    
    const frameIntegrity = document.getElementById("frame-integrity");
    const frameMaterial = document.getElementById("frame-material");
    const frameStealth = document.getElementById("frame-stealth");
    
    const btnVioletFire = document.getElementById("btn-violet-fire");
    const btnDense = document.getElementById("btn-dense");
    const bgMatrix = document.querySelector(".background-matrix");

    // Utilities to fetch API
    async function postJSON(url, data) {
        try {
            const response = await fetch(url, {
                method: "POST", 
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error("Zero-Point Link Error:", error);
        }
    }

    async function fetchTelemetry() {
        try {
            const response = await fetch("/api/telemetry/");
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error("Zero-Point Link Error:", error);
        }
    }

    function updateUI(data) {
        if(!data) return;
        
        // Drive
        if(data.drive) {
            driveStatus.innerText = data.drive.status;
            if(data.drive.status === "ONLINE") {
                driveStatus.className = "value status-online";
            } else {
                driveStatus.className = "value status-offline";
            }
            
            driveCoherence.innerText = data.drive.coherence.toFixed(2) + " %";
            driveThrust.innerText = data.drive.thrust.toFixed(2);
        }
        
        // Airframe
        if(data.airframe) {
            frameIntegrity.innerText = data.airframe.integrity.toFixed(2) + " %";
            frameMaterial.innerText = data.airframe.material;
            
            if(data.airframe.active_stealth) {
                frameStealth.innerText = "ATIVO (QUANTUM)";
                frameStealth.className = "value stealth-on";
                bgMatrix.classList.add("violet-fire-mode");
            } else {
                frameStealth.innerText = "INATIVO";
                frameStealth.className = "value stealth-off";
                bgMatrix.classList.remove("violet-fire-mode");
            }
        }
    }

    // Event Listeners
    focusSlider.addEventListener("input", async (e) => {
        const val = e.target.value;
        focusDisplay.innerText = val + "%";
        
        // Convert to 0.xx format
        const focusFloat = parseInt(val) / 100.0;
        
        const result = await postJSON("/api/set_focus/", { focus: focusFloat });
        if(result) updateUI({ drive: result.drive });
    });

    btnVioletFire.addEventListener("click", async () => {
        const result = await postJSON("/api/set_frequency/", { frequency: "violet_fire" });
        if(result) updateUI({ airframe: result.airframe });
    });

    btnDense.addEventListener("click", async () => {
        const result = await postJSON("/api/set_frequency/", { frequency: "dense" });
        if(result) updateUI({ airframe: result.airframe });
    });

    // Initial Telemetry load and polling interval
    fetchTelemetry();
    // In real app we could use SSE, for now rapid polling every 1 sec simulates realtime
    setInterval(fetchTelemetry, 1000);
});
