"""
Fenix VLS - Broadcaster Zero-Point
Envia pulsos de telemetria a cada 0.5s para o PythonJet via JWT.
"""

import threading
import time
import json
import logging
import requests
import os

logger = logging.getLogger("VLSBroadcaster")

PYTHONJET_URL = os.environ.get("PYTHONJET_VLS_ENDPOINT", "http://localhost:8001/api/vls/telemetry-sync/")
VLS_SECRET_TOKEN = os.environ.get("VLS_SECRET_TOKEN", "fenix-vls-secret-alpha-token")
BROADCAST_INTERVAL = 0.5  # seconds

def start_broadcaster(drive_instance, frame_instance):
    """
    Inicia o thread daemon de broadcasting de telemetria.
    Esta função deve ser chamada pelo apps.py do Django no método ready().
    """
    def broadcast_loop():
        logger.info(f"VLS Broadcaster started. Transmitting to: {PYTHONJET_URL}")
        while True:
            try:
                telemetry = {
                    "drive": drive_instance.report_status(),
                    "airframe": frame_instance.get_telemetry(),
                    "source": "fenix-vls-alpha",
                }

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {VLS_SECRET_TOKEN}",
                }

                r = requests.post(PYTHONJET_URL, data=json.dumps(telemetry), headers=headers, timeout=2)

                if r.status_code == 200:
                    logger.debug("Telemetry pulse acknowledged.")
                else:
                    logger.warning(f"PythonJet returned {r.status_code}: {r.text[:100]}")

            except requests.exceptions.ConnectionError:
                # PythonJet offline - OK, o VLS continua voando sozinho
                logger.debug("PythonJet offline. VLS operating autonomously.")
            except Exception as e:
                logger.error(f"Broadcaster error: {e}")

            time.sleep(BROADCAST_INTERVAL)

    t = threading.Thread(target=broadcast_loop, daemon=True)
    t.start()
    logger.info("VLS Broadcaster thread launched.")
