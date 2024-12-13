import random

class Field:
    def __init__(self, size=208):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def place_hive(self):
        # Find a random location for the hive (2x2 grid)
        while True:
            x = random.randint(0, self.size - 2)
            y = random.randint(0, self.size - 2)
            # Check if the 2x2 area is empty
            if all(self.grid[x + dx][y + dy] is None for dx in range(2) for dy in range(2)):
                # Mark the 2x2 area as the hive
                for dx in range(2):
                    for dy in range(2):
                        self.grid[x + dx][y + dy] = "hive"
                return (x, y)  # Return the hive's top-left corner