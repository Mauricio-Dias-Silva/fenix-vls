import time
import logging
import random
from core.quantum_drive import QuantumInertialDrive
from core.airframe import AirframeStructure
from simulations.physics_engine_vls import VLSSimulator, datetime, json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Fenix-Main")

def run_ic_simulation():
    print("="*60)
    logger.info("AURA CLOUD POWERED | SOVEREIGN COMMAND - VLS IC")
    print("="*60)
    time.sleep(1)

    drive = QuantumInertialDrive()
    frame = AirframeStructure()
    sim = VLSSimulator()

    print("\n[ FASE 1: RECONHECIMENTO DO AIRFRAME ]")
    frame.apply_state_vector("HIGH_FREQ_FIELD")
    
    print("\n[ FASE 2: VOO DINÂMICO BCI (Brain-Computer Interface) ]")
    target_altitude = 30.0
    dt = 0.1
    duration = 15.0
    steps = int(duration / dt)
    
    status = "NOMINAL"
    base_focus = 0.95 # Começa com foco alto
    
    for step in range(steps):
        current_time = step * dt
        
        # Simula a leitura de um EEG (introduz ruído natural do cérebro)
        # Evento de estresse aos 8 segundos (Foco do piloto cai drasticamente)
        if 8.0 < current_time < 10.0:
            raw_eeg = random.uniform(0.40, 0.70)
        else:
            raw_eeg = random.uniform(0.85, 0.99)
            
        # O Cérebro Digital tenta estabilizar na altitude
        error = target_altitude - sim.altitude_m
        if error > 5.0:
            requested_thrust = 80.0 
        elif error > 0.0:
            requested_thrust = sim.calculate_weight_force() + (error * 3.0)
        else:
            requested_thrust = 0.0
            
        # Passo Crítico: O Motor só entrega o thrust se a Coerência Neural (Q-Drive) permitir
        drive_active = drive.stabilize_vacuum(requested_thrust, raw_eeg)
        actual_requested_thrust = drive.thrust_output
            
        # Alimenta o motor físico
        status = sim.step(requested_thrust=actual_requested_thrust, dt_seconds=dt)
        
        if step % 10 == 0:  # Print a cada 1 segundo
            log = sim.flight_log[-1]
            p_msg = "[FAIL-SAFE ACTIVATED! PARACHUTE OPEN!]" if log['parachute'] else ""
            print(f"T+{current_time:.1f}s | BCI: {drive.coherence_level:.0f}% | Alt: {log['altitude']}m | Vel: {log['velocity']}m/s | {p_msg}")
            
        if status != "NOMINAL":
            print(f"EVENTO T+{current_time:.1f}s: {status}")
            break

    # Salva o Relatório Univesp
    report_name = f"simulations/stress_reports/ic_flight_report_{datetime.now().strftime('%Y%H%M%S')}.json"
    with open(report_name, "w") as f:
        json.dump(sim.flight_log, f, indent=4)
        
    print("\n" + "="*60)
    logger.info("RELATÓRIO DE SIMULAÇÃO IC SALVO")
    logger.info(f"Relatório gerado em: {report_name}")
    print("="*60)

if __name__ == "__main__":
    run_ic_simulation()
