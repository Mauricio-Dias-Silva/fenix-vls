"""
Fenix VLS — Mission Control Server
===================================
FastAPI server with Server-Sent Events (SSE) for real-time telemetry streaming.
Runs the simulation frame by frame and pushes data to the dashboard live.
"""

import os
import json
import time
import asyncio
import random
import threading

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse

from simulations.physics_engine_vls import VLSSimulator, PPORocketController
from core.quantum_drive import QuantumInertialDrive
from core.airframe import AirframeStructure

app = FastAPI(title="Fenix VLS | Mission Control")

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Simulation State (Thread-Safe) ──────────────────────────────────────────
_sim_lock = threading.Lock()
_sim_running = False
_sim_frames = []       # Buffer de frames produzidos pela simulação
_sim_complete = False
_sim_result = None

def _run_simulation_worker(target_altitude: float, duration: float, dt: float):
    """Roda a simulação em background e empurra frames para o buffer."""
    global _sim_running, _sim_frames, _sim_complete, _sim_result

    drive = QuantumInertialDrive()
    frame_obj = AirframeStructure()
    sim = VLSSimulator()
    ppo = PPORocketController(target_altitude)

    frame_obj.apply_state_vector("HIGH_FREQ_FIELD")
    steps = int(duration / dt)
    status = "NOMINAL"

    with _sim_lock:
        _sim_frames = []
        _sim_complete = False
        _sim_result = None

    for step in range(steps):
        t = step * dt

        # Simula leitura de EEG (stress entre 8-10s)
        if 8.0 < t < 10.0:
            raw_eeg = random.uniform(0.40, 0.70)
        else:
            raw_eeg = random.uniform(0.85, 0.99)

        state_vec = (sim.altitude_m, sim.velocity_mps)
        requested_thrust = ppo.predict_action(state_vec)

        drive_active = drive.stabilize_vacuum(requested_thrust, raw_eeg)
        actual_thrust = drive.thrust_output

        status = sim.step(requested_thrust=actual_thrust, dt_seconds=dt)

        log = sim.flight_log[-1]
        frame_data = {
            "t": round(t, 2),
            "altitude": log["altitude"],
            "velocity": log["velocity"],
            "requested_thrust_N": log["requested_thrust_N"],
            "actual_thrust_N": log["actual_thrust_N"],
            "drag_N": log["drag_N"],
            "G_force": log["G_force"],
            "parachute": log["parachute"],
            "bci_coherence": round(drive.coherence_level, 1),
            "stealth": frame_obj.stealth_engaged,
            "status": status,
        }

        with _sim_lock:
            _sim_frames.append(frame_data)

        if status != "NOMINAL":
            break

        time.sleep(dt * 0.5)  # Delay de realismo (2x mais rápido que real)

    # Salvar relatório JSON
    os.makedirs(os.path.join(_BASE_DIR, "simulations", "stress_reports"), exist_ok=True)
    from datetime import datetime
    report_name = os.path.join(
        _BASE_DIR, "simulations", "stress_reports",
        f"ic_flight_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(report_name, "w") as f:
        json.dump(sim.flight_log, f, indent=4)

    with _sim_lock:
        _sim_running = False
        _sim_complete = True
        _sim_result = {"status": status, "report": report_name, "frames": len(sim.flight_log)}


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(_BASE_DIR, "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/launch")
async def launch_simulation(target_altitude: float = 30.0, duration: float = 20.0, dt: float = 0.1):
    """Inicia a simulação em background."""
    global _sim_running
    with _sim_lock:
        if _sim_running:
            return JSONResponse({"status": "already_running"}, status_code=409)
        _sim_running = True

    t = threading.Thread(
        target=_run_simulation_worker,
        args=(target_altitude, duration, dt),
        daemon=True
    )
    t.start()
    return JSONResponse({"status": "launched", "target_altitude": target_altitude, "duration": duration})


@app.get("/api/stream")
async def stream_telemetry():
    """
    Server-Sent Events (SSE) — empurra cada frame da simulação para o browser.
    O dashboard se conecta aqui e recebe dados em tempo real.
    """
    async def event_generator():
        last_sent_index = 0
        yield "data: {\"type\": \"connected\"}\n\n"

        while True:
            with _sim_lock:
                frames = _sim_frames[last_sent_index:]
                is_complete = _sim_complete
                result = _sim_result

            for frame in frames:
                yield f"data: {json.dumps({'type': 'frame', 'payload': frame})}\n\n"
                last_sent_index += 1

            if is_complete and result is not None and last_sent_index >= len(_sim_frames):
                yield f"data: {json.dumps({'type': 'complete', 'payload': result})}\n\n"
                break

            await asyncio.sleep(0.05)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.get("/api/status")
async def get_status():
    with _sim_lock:
        return JSONResponse({
            "running": _sim_running,
            "complete": _sim_complete,
            "frames_ready": len(_sim_frames),
            "result": _sim_result,
        })


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
