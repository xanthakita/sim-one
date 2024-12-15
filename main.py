from field import Field
from hive_orchestrator import HiveOrchestrator, QueenBee
from display import Display
import os

def main():
    # Initialize the field
    field = Field()

    # Initialize the hive orchestrator
    hive = HiveOrchestrator(field)
    field.hive = hive  # Add reference to hive in field


    # Add the queen bee
    queen = QueenBee(hive)
    hive.add_bee(queen)
    hive.queen = queen
    print(f"Queen added to hive at: ({queen.x}, {queen.y})")  # Add debug print

    # Initialize the display
    display = Display(field, os.getenv("TIME_MULTIPLIER", 1.0))

    # Start the display loop (this will handle the initialization)
    display.run()  # This method contains the main game loop

if __name__ == "__main__":
    main()
    
