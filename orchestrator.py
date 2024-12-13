import os
import time

class OverlordOrchestrator:
    def __init__(self, default_multiplier=1.0):
        """
        Initialize the orchestrator with a default time multiplier.
        The multiplier adjusts the speed of the simulation.
        """
        self.time_multiplier = float(os.getenv("TIME_MULTIPLIER", default_multiplier))
        self.simulated_seconds_per_real_second = 3600 / 60  # 1 simulated hour = 1 real-time minute

    def calculate_real_time_per_simulated_second(self):
        """
        Calculate the real-time duration of one simulated second based on the multiplier.
        """
        return 1 / (self.simulated_seconds_per_real_second * self.time_multiplier)

    def run_simulation(self, total_simulated_seconds):
        """
        Run the simulation for a given number of simulated seconds.
        """
        real_time_per_simulated_second = self.calculate_real_time_per_simulated_second()
        print(f"Simulation running with time multiplier: {self.time_multiplier}")
        print(f"1 simulated second = {real_time_per_simulated_second:.4f} real seconds")

        for simulated_second in range(total_simulated_seconds):
            # Simulate the passage of time
            print(f"Simulated Time: {simulated_second // 3600}h:{(simulated_second % 3600) // 60}m:{simulated_second % 60}s")
            time.sleep(real_time_per_simulated_second)

        print("Simulation complete!")

if __name__ == "__main__":
    orchestrator = OverlordOrchestrator()
    orchestrator.run_simulation(total_simulated_seconds=24 * 3600)