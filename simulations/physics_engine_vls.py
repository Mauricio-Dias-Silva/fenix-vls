"""
Fenix VLS - Digital Twin Physics Simulation Engine

Simulador Termodinâmico e Cinético para testar Integridade do Chassi e Propulsão.
Calcula a taxa de G, Empuxo EDF (Electric Ducted Fans) e Arrasto (Drag).

Material Alpha: Titânio Ti-6Al-4V + CFRP (Carbon Fiber Reinforced Polymer)
"""

import math
import time
import json
from datetime import datetime

class VLSSimulator:
    def __init__(self):
        # Constantes Físicas (Terra)
        self.g = 9.80665 # m/s^2 (Gravidade)
        self.rho = 1.225 # kg/m^3 (Densidade do ar ao nível do mar)
        
        # Parâmetros do Chassi (Protótipo 1.2m)
        self.mass_kg = 4.85 # Massa seca (Chassi + Bateria + Avionics)
        self.frontal_area_m2 = 0.045 # Área frontal (Aerodinâmica de Míssil/Foguete)
        self.drag_coefficient_cd = 0.25 # Coeficiente de Arrasto (Afilado)
        
        # Estado Inicial
        self.altitude_m = 0.0
        self.velocity_mps = 0.0
        self.acceleration_mps2 = 0.0
        
        # Telemetria Histórica
        self.flight_log = []

    def calculate_drag(self, velocity):
        """ Equação de Arrasto: Fd = 1/2 * rho * v^2 * Cd * A """
        if velocity == 0: return 0.0
        drag = 0.5 * self.rho * (velocity**2) * self.drag_coefficient_cd * self.frontal_area_m2
        return drag if velocity > 0 else -drag

    def calculate_weight_force(self):
        """ Força Peso: Fg = m * g """
        return self.mass_kg * self.g

    def step(self, thrust_newtons, dt_seconds=0.1):
        """ 
        Avança a simulação 1 frame de tempo baseado no empuxo fornecido pelo motor.
        """
        # Forças Atuantes
        force_gravity = self.calculate_weight_force()
        force_drag = self.calculate_drag(self.velocity_mps)
        
        # Força Resultante (Empuxo aponta para cima, Peso e Arrasto para baixo)
        # Se caindo, arrasto aponta para cima (se opõe à queda)
        net_force = thrust_newtons - force_gravity - force_drag
        
        # 2ª Lei de Newton: F = m*a
        self.acceleration_mps2 = net_force / self.mass_kg
        
        # Cinemática Clássica
        self.velocity_mps += self.acceleration_mps2 * dt_seconds
        self.altitude_m += self.velocity_mps * dt_seconds
        
        # Prevenindo túnel abaixo do chão
        if self.altitude_m < 0:
            self.altitude_m = 0.0
            self.velocity_mps = 0.0
            if self.acceleration_mps2 < -20.0:  # Impacto fatal > 2G negativo bruto
                return "CRITICAL_G_IMPACT_FRACTURE"

        # G-Force experenciada pela estrutura
        g_force = (self.acceleration_mps2 + self.g) / self.g

        # Registro de Telemetria
        log_entry = {
            "altitude": round(self.altitude_m, 2),
            "velocity": round(self.velocity_mps, 2),
            "thrust_N": round(thrust_newtons, 2),
            "drag_N": round(force_drag, 2),
            "G_force": round(g_force, 2)
        }
        self.flight_log.append(log_entry)
        
        return "NOMINAL"

def run_test_flight():
    print("[INIT] Fenix VLS Physics Engine - Protótipo Alpha")
    sim = VLSSimulator()
    
    # Plano de Voo (10 segundos)
    # Target: Levantar rapidamente e tentar estabilizar (Hovering) em 50 metros
    target_altitude = 50.0
    dt = 0.1
    duration = 10.0
    steps = int(duration / dt)
    
    status = "NOMINAL"
    print(f"Massa Real Estimada: {sim.mass_kg} kg")
    print(f"Força Peso a Vencer (Hover Thrust Required): {sim.calculate_weight_force():.2f} N")
    print("-" * 50)
    
    for step in range(steps):
        current_time = step * dt
        
        # Algoritmo de Controle PID Básico (Digital Twin Cérebro)
        error = target_altitude - sim.altitude_m
        
        # Se estamos abaixo do alvo, empuxo no máximo tolerável pelo atuador (ex: 80 Newtons = ~8kg de empuxo EDF)
        if error > 5.0:
            thrust = 80.0 
        # Se estamos chegando perto, reduz pro peso exato (Hover)
        elif error > 0.0:
            thrust = sim.calculate_weight_force() + (error * 2.0)
        # Se passamos, corta o motor pra gravidade compensar
        else:
            thrust = 0.0
            
        status = sim.step(thrust_newtons=thrust, dt_seconds=dt)
        
        if step % 10 == 0:  # Print a cada 1 segundo
            log = sim.flight_log[-1]
            print(f"T+{current_time:.1f}s | Alt: {log['altitude']}m | Vel: {log['velocity']}m/s | Gs: {log['G_force']} | Status: {status}")
            
        if status != "NOMINAL":
            print(f"FALHA CATASTRÓFICA EM T+{current_time:.1f}s")
            break

    # Salva o Relatório
    report_name = f"stress_reports/flight_report_{datetime.now().strftime('%Y%H%M%S')}.json"
    with open(report_name, "w") as f:
        json.dump(sim.flight_log, f, indent=4)
        
    print("-" * 50)
    print(f"[END] Simulação Concluída. Report salvo em: {report_name}")

if __name__ == "__main__":
    run_test_flight()
