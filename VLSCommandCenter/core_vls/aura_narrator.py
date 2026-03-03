"""
Aura AI Narrator - Fenix VLS
Responsável por gerar a narrativa de voz e logs de inteligência da Aura baseados na telemetria.
"""

import time
import random

class AuraNarrator:
    def __init__(self):
        self.last_state = {
            "drive_status": "OFFLINE",
            "coherence": 0.0,
            "integrity": 100.0,
            "active_stealth": False
        }
        self.message_queue = []
        self._boot_message()

    def _boot_message(self):
        self.log_event("Aura System Online. Conectada ao Fênix VLS Alpha.")

    def log_event(self, message):
        event = {
            "timestamp": time.strftime("%H:%M:%S"),
            "message": message,
            "priority": "normal"
        }
        self.message_queue.append(event)
        # Manter apenas as últimas 10 mensagens
        if len(self.message_queue) > 10:
            self.message_queue.pop(0)

    def monitor_telemetry(self, drive_status, coherence, integrity, active_stealth):
        """
        Analisa a telemetria e decide se a Aura deve falar algo.
        """
        
        # 1. Mudança de Status do Drive
        if drive_status == "ONLINE" and self.last_state["drive_status"] != "ONLINE":
            self.log_event("Drive Inercial Quântico ativado. Vetores de empuxo estabilizados.")
        elif drive_status == "OFFLINE" and self.last_state["drive_status"] != "OFFLINE":
            self.log_event("Drive em Standby. Coerência neural dissipada.")

        # 2. Coerência Neural (Foco)
        if coherence >= 0.9 and self.last_state["coherence"] < 0.9:
            self.log_event("Nível de foco crítico alcançado. Integração neural em 90%.")
        elif coherence < 0.3 and self.last_state["coherence"] >= 0.3:
            self.log_event("Alerta: Coerência neural baixa. Risco de desestabilização de voo.")

        # 3. Stealth / Airframe
        if active_stealth and not self.last_state["active_stealth"]:
            self.log_event("Campo de Alta Frequência engajado. Assinatura de radar minimizada.")
        elif not active_stealth and self.last_state["active_stealth"]:
            self.log_event("Retornando ao estado base. Furtividade desativada.")

        # 4. Integridade
        if integrity < 50.0 and self.last_state["integrity"] >= 50.0:
            self.log_event("AVISO: Integridade estrutural abaixo de 50%. Recomendo ejeção imediata.")

        # Atualiza o último estado conhecido
        self.last_state = {
            "drive_status": drive_status,
            "coherence": coherence,
            "integrity": integrity,
            "active_stealth": active_stealth
        }

    def get_latest_messages(self):
        """Retorna as mensagens pendentes e limpa a fila (ou retorna as últimas X)"""
        return self.message_queue

# Instância Global
_aura = AuraNarrator()
