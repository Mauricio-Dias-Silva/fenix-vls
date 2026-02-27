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
    data = {
        'drive': _drive.report_status(),
        'airframe': _frame.get_telemetry()
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
            return JsonResponse({'status': 'frequency updated', 'airframe': _frame.get_telemetry()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
