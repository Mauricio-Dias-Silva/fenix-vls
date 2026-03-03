"""
Aura Intelligence Suite - Fenix VLS
Módulo de análise preditiva, cálculo orbital e detecção de anomalias.
"""

import math
import time

class AuraIntelligence:
    def __init__(self):
        self.orbital_radius_earth = 6371000  # metros
        self.leo_altitude_target = 300000    # 300km (Baixa Órbita)
        self.target_velocity = 7700          # ~7.7 km/s para LEO
        
        self.current_altitude = 0.0          # metros
        self.horizontal_velocity = 0.0       # m/s
        self.vertical_velocity = 0.0         # m/s
        self.vibration_history = []
        self.last_update_ts = time.time()

    def update_simulation(self, thrust_kn, g_force, coherence):
        """
        Atualiza o estado preditivo com base na telemetria atual.
        """
        now = time.time()
        dt = now - self.last_update_ts
        self.last_update_ts = now

        # Simulação simplificada de ascensão
        # F = ma -> a = F/m. Massa aproximada do protótipo: 5kg
        mass = 5.0
        acceleration = (thrust_kn * 1000) / mass
        
        # Assume-se que parte do empuxo vira velocidade vertical e parte horizontal
        # Proporcional à coerência (coerência alta = melhor vetorização)
        self.vertical_velocity += acceleration * dt * 0.7 * coherence
        self.horizontal_velocity += acceleration * dt * 0.3 * coherence
        
        self.current_altitude += self.vertical_velocity * dt
        
        # Limitar altitude para simulação científica
        if self.current_altitude < 0: self.current_altitude = 0

    def calculate_orbital_insertion(self):
        """
        Calcula a porcentagem de progresso para inserção em LEO.
        """
        alt_progress = (self.current_altitude / self.leo_altitude_target) * 0.5
        vel_progress = (self.horizontal_velocity / self.target_velocity) * 0.5
        
        insertion_pct = (alt_progress + vel_progress) * 100
        return min(max(insertion_pct, 0.0), 100.0)

    def detect_anomalies(self, integrity, coherence):
        """
        Procura por padrões de falha iminente.
        """
        anomalies = []
        
        # 1. Ressonância Harmônica (Simulada por jitter na integridade)
        if integrity < 98.0 and integrity > 90.0:
            anomalies.append({
                "type": "VIBRATION",
                "severity": "low",
                "message": "Detectada ressonância harmônica leve no chassi CFRP."
            })
            
        # 2. Decaimento de Coerência Súbito
        if coherence < 0.5:
             anomalies.append({
                "type": "COHERENCE_DECAY",
                "severity": "medium",
                "message": "Decaimento instável de coerência. Vetorização comprometida."
            })
            
        return anomalies

    def get_intelligence_report(self):
        """Retorna o snapshot analítico completo."""
        insertion = self.calculate_orbital_insertion()
        status = "CRITICAL" if insertion < 10 else "NOMINAL"
        if insertion > 95: status = "ORBITAL_STABLE"

        return {
            "altitude_m": round(float(self.current_altitude), 2),
            "velocity_ms": round(float(math.sqrt(self.vertical_velocity**2 + self.horizontal_velocity**2)), 2),
            "insertion_progress": round(float(insertion), 2),
            "status": status,
            "eta_leo": "CALCULATING..." if insertion < 5 else f"{max(0, int(300 - insertion))}s"
        }

# Instância Global
_intel = AuraIntelligence()
