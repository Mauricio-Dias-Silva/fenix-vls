import time
import logging
from core.quantum_drive import QuantumAuraDrive
from core.airframe import AirframeStructure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Fenix-Main")

def run_simulation():
    print("="*50)
    logger.info("INICIANDO PROTOCOLO AURA SOVEREIGN COMMAND - FÊNIX VLS")
    print("="*50)
    time.sleep(1)

    drive = QuantumAuraDrive()
    frame = AirframeStructure()

    print("\n[ FASE 1: PREPARAÇÃO DO AIRFRAME ]")
    # 1. Aplicando Fogo Violeta (Ressonância) para garantir Stealth e Integridade
    frame.apply_digital_alchemy("violet_fire")
    status_frame = frame.get_telemetry()
    logger.info(f"Telemetria Airframe: {status_frame}")
    
    time.sleep(1)
    
    print("\n[ FASE 2: TENTATIVA DE DECOLAGEM COM COERÊNCIA BAIXA ]")
    # 2. Iniciando Drive com foco baixo (Simulando dispersão mental)
    success_fail = drive.stabilize_vacuum(intent_vector=5.0, user_focus=0.60)
    
    time.sleep(1)
    
    print("\n[ FASE 3: DECOLAGEM VLS - SUPERPOSIÇÃO INERCIAL ALCANÇADA ]")
    # 3. Iniciando Drive com foco alto (Coerência Quântica real)
    success_pass = drive.stabilize_vacuum(intent_vector=12.0, user_focus=0.98)
    status_drive = drive.report_status()
    
    print("\n" + "="*50)
    logger.info("RELATÓRIO DE VOO ZERO-POINT")
    logger.info(f"AIRFRAME: {status_frame}")
    logger.info(f"QUANTUM DRIVE: {status_drive}")
    print("="*50)

if __name__ == "__main__":
    run_simulation()
