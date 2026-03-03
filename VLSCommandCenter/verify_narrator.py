
from core_vls.aura_narrator import AuraNarrator
import time

def test_narrator_logic():
    narrator = AuraNarrator()
    print("Testing initial boot message...")
    messages = narrator.get_latest_messages()
    assert len(messages) > 0
    print(f"Boot message: {messages[0]['message']}")

    print("\nSimulating Drive Online...")
    narrator.monitor_telemetry("ONLINE", 0.5, 100.0, False)
    messages = narrator.get_latest_messages()
    assert any("Drive Inercial Quântico ativado" in m['message'] for m in messages)
    print("Drive Online message detected.")

    print("\nSimulating Low Coherence...")
    narrator.monitor_telemetry("ONLINE", 0.1, 100.0, False)
    messages = narrator.get_latest_messages()
    assert any("Alerta: Coerência neural baixa" in m['message'] for m in messages)
    print("Low coherence alert detected.")

    print("\nSimulating High Integrity Loss...")
    narrator.monitor_telemetry("ONLINE", 0.5, 40.0, False)
    messages = narrator.get_latest_messages()
    assert any("Integridade estrutural abaixo de 50%" in m['message'] for m in messages)
    print("Integrity alert detected.")

    print("\nAll logical checks passed!")

if __name__ == "__main__":
    try:
        test_narrator_logic()
    except Exception as e:
        print(f"Test failed: {e}")
