from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Adds the Fenix VLS root folder to Python Path so we can import the core logic
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.quantum_drive import QuantumInertialDrive
from core.airframe import AirframeStructure
from .aura_narrator import _aura
from .hardware_layer import _hal
from .aura_intelligence import _intel

# In-memory singletons to maintain flight state across requests
_drive = QuantumInertialDrive()
_frame = AirframeStructure()

def dashboard(request):
    """
    Renders the Sovereign Command Dashboard.
    """
    return render(request, 'index.html')

def get_telemetry(request):
    """
    Returns the real-time state of the Quantum Drive and the Airframe.
    """
    drive_report = _drive.report_status()
    frame_report = _frame.get_telemetry()
    
    # 1. Update Intelligence Simulation
    _intel.update_simulation(
        thrust_kn=drive_report['thrust'],
        g_force=0.0, # Placeholder
        coherence=drive_report['coherence'] / 100.0
    )
    intel_report = _intel.get_intelligence_report()
    anomalies = _intel.detect_anomalies(frame_report['integrity'], drive_report['coherence'] / 100.0)

    # 2. Aura monitors the signals
    _aura.monitor_telemetry(
        drive_status=drive_report['status'],
        coherence=drive_report['coherence'] / 100.0,
        integrity=frame_report['integrity'],
        active_stealth=frame_report['active_stealth']
    )
    
    # AI identifies anomalies and Aura logs them
    for anomaly in anomalies:
        _aura.log_event(f"ANOMALY: {anomaly['message']}")
    
    data = {
        'drive': drive_report,
        'airframe': frame_report,
        'aura_messages': _aura.get_latest_messages(),
        'hardware': _hal.get_hardware_status(),
        'intelligence': intel_report
    }
    return JsonResponse(data)

@csrf_exempt
def set_focus(request):
    """
    API endpoint to adjust intent/focus vector.
    Expects JSON: {"focus": 0.90}
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            focus_level = float(body.get('focus', 0.0))
            # thrust vector is tied to neural coherence
            _drive.stabilize_vacuum(thrust_vector=15.0 * focus_level, neural_coherence=focus_level)
            
            # Trigger Hardware/PWM signals
            _hal.set_engine_thrust(focus_level)
            
            return JsonResponse({'status': 'focus updated', 'drive': _drive.report_status()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def set_frequency(request):
    """
    API endpoint to set airframe frequency (e.g. "violet_fire").
    Expects JSON: {"frequency": "violet_fire"}
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            freq = body.get('frequency', 'base_state')
            _frame.apply_state_vector(freq)
            
            # Trigger Hardware indicative signals
            _hal.toggle_stealth_field(active=(freq == "high_freq_field"))
            
            return JsonResponse({'status': 'frequency updated', 'airframe': _frame.get_telemetry()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
