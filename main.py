from field import Field
from hive_orchestrator import HiveOrchestrator, QueenBee
from display import Display
import os

def main():
    # Initialize the field
    field = Field()

    # Initialize the hive orchestrator
    hive = HiveOrchestrator(field)

    # Add the queen bee
    queen = QueenBee(hive)
    hive.add_bee(queen)
    hive.queen = queen

    # Run the simulation
    display = Display(field, os.getenv("TIME_MULTIPLIER", 1.0))
    while True:
        hive.update()
        display.draw_field()

if __name__ == "__main__":
    main()