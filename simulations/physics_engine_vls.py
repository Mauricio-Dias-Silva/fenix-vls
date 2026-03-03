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
        
        # Subsistemas
        self.edf_current_thrust = 0.0 # Empuxo real entregue pelo motor
        self.edf_spool_time_constant = 0.25 # Tempo para o motor girar e bater o empuxo (Lag)
        self.parachute_deployed = False
        self.parachute_area_m2 = 1.5 # Área do paraquedas de emergência
        self.parachute_cd = 1.7 # Coeficiente de arrasto do paraquedas
        self.flight_log = []

    def calculate_drag(self, velocity):
        """ Equação de Arrasto: Fd = 1/2 * rho * v^2 * Cd * A """
        if velocity == 0: return 0.0
        
        # O arrasto muda se o paraquedas estiver aberto
        if self.parachute_deployed:
            area = self.parachute_area_m2
            cd = self.parachute_cd
        else:
            area = self.frontal_area_m2
            cd = self.drag_coefficient_cd
            
        drag = 0.5 * self.rho * (velocity**2) * cd * area
        return drag if velocity > 0 else -drag

    def calculate_weight_force(self):
        """ Força Peso: Fg = m * g """
        return self.mass_kg * self.g

    def deploy_parachute(self):
        """ Desdobra o paraquedas balístico de emergência """
        if not self.parachute_deployed:
            self.parachute_deployed = True
            # Adiciona massa extra do paraquedas sendo puxado? (simplificado)

    def step(self, requested_thrust, dt_seconds=0.1):
        """ 
        Avança a simulação 1 frame de tempo.
        """
        # [MODO IC] Inércia do Motor (EDF Spool-up Lag) - Simulação de Primeira Ordem
        # O motor não dá o empuxo instantaneamente. Ele precisa acelerar a massa de ar.
        delta_thrust = requested_thrust - self.edf_current_thrust
        self.edf_current_thrust += (delta_thrust / self.edf_spool_time_constant) * dt_seconds
        
        # Se requested_thrust for negativo (impossível para EDF) ou 0
        if self.edf_current_thrust < 0:
            self.edf_current_thrust = 0.0

        # Forças Atuantes
        force_gravity = self.calculate_weight_force()
        force_drag = self.calculate_drag(self.velocity_mps)
        
        # Força Resultante
        net_force = self.edf_current_thrust - force_gravity - force_drag
        
        # 2ª Lei de Newton: F = m*a
        self.acceleration_mps2 = net_force / self.mass_kg
        
        # Cinemática Clássica
        self.velocity_mps += self.acceleration_mps2 * dt_seconds
        self.altitude_m += self.velocity_mps * dt_seconds
        
        # [FAIL-SAFE DE OURO] Disparar paraquedas se em queda livre mortal
        if self.velocity_mps < -8.0 and self.altitude_m < 20.0 and self.edf_current_thrust < force_gravity:
            self.deploy_parachute()

        # Prevenindo túnel abaixo do chão
        if self.altitude_m < 0:
            self.altitude_m = 0.0
            self.velocity_mps = 0.0
            if self.acceleration_mps2 < -20.0 and not self.parachute_deployed:  # Impacto fatal > 2G negativo
                return "CRITICAL_G_IMPACT_FRACTURE"
            elif self.parachute_deployed:
                return "SAFE_PARACHUTE_LANDING"

        # G-Force experenciada pela estrutura
        g_force = (self.acceleration_mps2 + self.g) / self.g

        # Registro de Telemetria
        log_entry = {
            "altitude": round(self.altitude_m, 2),
            "velocity": round(self.velocity_mps, 2),
            "requested_thrust_N": round(requested_thrust, 2),
            "actual_thrust_N": round(self.edf_current_thrust, 2), # Realismo do motor
            "drag_N": round(force_drag, 2),
            "G_force": round(g_force, 2),
            "parachute": self.parachute_deployed
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
            requested_thrust = 80.0 
        # Se estamos chegando perto, reduz pro peso exato (Hover)
        elif error > 0.0:
            requested_thrust = sim.calculate_weight_force() + (error * 3.0) # Aumentando ganho proporcional devido ao lag
        # Se passamos, corta o motor pra gravidade compensar
        else:
            requested_thrust = 0.0
            
        status = sim.step(requested_thrust=requested_thrust, dt_seconds=dt)
        
        if step % 10 == 0:  # Print a cada 1 segundo
            log = sim.flight_log[-1]
            p_msg = "[PARA]" if log['parachute'] else ""
            print(f"T+{current_time:.1f}s | Alt: {log['altitude']}m | Vel: {log['velocity']}m/s | P_Req: {log['requested_thrust_N']}N | P_Real: {log['actual_thrust_N']}N {p_msg} | Status: {status}")
            
        if status != "NOMINAL":
            print(f"EVENTO DE FIM DE SIMULAÇÃO T+{current_time:.1f}s: {status}")
            break

    # Salva o Relatório
    report_name = f"stress_reports/flight_report_{datetime.now().strftime('%Y%H%M%S')}.json"
    with open(report_name, "w") as f:
        json.dump(sim.flight_log, f, indent=4)
        
    print("-" * 50)
    print(f"[END] Simulação Concluída. Report salvo em: {report_name}")

if __name__ == "__main__":
    run_test_flight()
