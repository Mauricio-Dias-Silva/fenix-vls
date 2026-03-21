import math

class ChronosEngine:
    """
    Cosmic and Planetary Timeline Engine.
    Maps 13.8 billion years of expansion/evolution to physical resonance constants.
    """
    
    ERAS = {
        "big_bang": {
            "name": "Singularity & Inflation",
            "age": "13.8 Ga",
            "resonance_factor": 10**26, # Inflation factor
            "constraints": {"entropy": 0.0, "temperature": float('inf')},
            "desc": "Exponential expansion from quantum fluctuations."
        },
        "hadean": {
            "name": "Primordial Fire",
            "age": "4.5 Ga",
            "resonance_factor": 2.5,
            "constraints": {"entropy": 0.3, "temperature": 2000.0},
            "desc": "Formation of Earth and Moon. Molten crust."
        },
        "archean": {
            "name": "Microbial Dawn",
            "age": "4.0 Ga",
            "resonance_factor": 1.8,
            "constraints": {"entropy": 0.5, "temperature": 80.0},
            "desc": "First single-celled organisms. Anaerobic world."
        },
        "paleozoic": {
            "name": "Cambrian Explosion",
            "age": "541 Ma",
            "resonance_factor": 3.2,
            "constraints": {"entropy": 0.8, "temperature": 25.0},
            "desc": "Rapid diversification of multicellular life."
        },
        "mesozoic": {
            "name": "Age of Giants",
            "age": "252 Ma",
            "resonance_factor": 4.5, # High power era
            "constraints": {"entropy": 0.9, "temperature": 30.0},
            "desc": "Dominance of Dinosaurs and first mammals."
        },
        "cenozoic": {
            "name": "Era of the Mind",
            "age": "66 Ma - Present",
            "resonance_factor": 1.0, # Baseline for modern human
            "constraints": {"entropy": 1.0, "temperature": 15.0},
            "desc": "Diversification of mammals and evolution of intelligence."
        }
    }

    def get_era_context(self, era_id):
        return self.ERAS.get(era_id, self.ERAS["cenozoic"])

    def calculate_evolutionary_torque(self, era_id, base_torque):
        context = self.get_era_context(era_id)
        # Power magnitude increases with biological 'drive' of the era
        return base_torque * context["resonance_factor"]

    def calculate_entropy_wave(self, t_coordinates):
        """
        Entropy-Time Wave Equation.
        Simulates the degradation or resonance of energy over temporal coordinates.
        """
        resonance = math.sin(t_coordinates * 0.1) * math.exp(-0.01 * t_coordinates)
        return round(abs(resonance), 4)

    def time_accelerated_healing(self, standard_days, era_id):
        """
        Warp Healing Protocol.
        Uses the high-resonance environment of past eras to accelerate current biological repair.
        """
        context = self.get_era_context(era_id)
        # Acceleration is proportional to the resonance factor
        accelerated_days = standard_days / context["resonance_factor"]
        return round(accelerated_days, 2)

if __name__ == "__main__":
    engine = ChronosEngine()
    print("--- CHRONOS: TIME-ACCELERATED HEALING ---")
    
    # Case: Regenerating a nerve (Standard: 300 days)
    standard_nerved_days = 300
    fast_healing = engine.time_accelerated_healing(standard_nerved_days, "mesozoic")
    
    print(f" > Condição: Reparo Neural Profundo")
    print(f" > Tempo Padrão: {standard_nerved_days} dias")
    print(f" > Tempo Aura (Era Mesozoica): {fast_healing} dias")
    print(f" > Ganho Temporal: {round((1 - fast_healing/standard_nerved_days)*100, 2)}%")

    print("\n--- CHRONOS EXPLORATION ---")
    engine = ChronosEngine()
    print("Simulando Ressonância da Era Mesozoica:")
    context = engine.get_era_context("mesozoic")
    print(f"Era: {context['name']} - Fator: {context['resonance_factor']}")
    print(f"Torque resultante (Base 50): {engine.calculate_evolutionary_torque('mesozoic', 50.0)}")
    
    print("\nCalculando Onda de Entropia Temporal (t=42):")
    print(f"Resonância: {engine.calculate_entropy_wave(42)}")
