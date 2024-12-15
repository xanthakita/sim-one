import random

class Field:
    def __init__(self, size=208):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.flowers = {}  # Dictionary to track flower positions and their nectar
        self.populate_flowers(50)  # Populate the field with 50 flowers

    def populate_flowers(self, count):
        for _ in range(count):
            while True:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                # Check if the cell is empty
                if self.grid[x][y] is None:
                    self.grid[x][y] = "flower"  # Mark the cell as a flower
                    self.flowers[(x, y)] = 10  # Each flower starts with 10 nectar
                    break

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

    def add_new_flower(self):
        """Add a single new flower to a random empty location"""
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[x][y] is None:
                self.grid[x][y] = "flower"
                self.flowers[(x, y)] = 10  # New flower with 10 nectar
                print(f"New flower bloomed at ({x}, {y})")
                break

    def collect_nectar_from_flower(self, x, y):
        """Attempt to collect nectar from a flower, returns amount collected"""
        if (x, y) in self.flowers and self.flowers[(x, y)] > 0:
            self.flowers[(x, y)] -= 1
            print(f"Nectar collected from flower at ({x}, {y}). Remaining: {self.flowers[(x, y)]}")

            # If flower is depleted, remove it and add a new one
            if self.flowers[(x, y)] == 0:
                # Store the current position of any bee that might be there
                bee_position = None
                if hasattr(self, 'hive') and self.hive.queen:
                    bee_position = (self.hive.queen.x, self.hive.queen.y)

                # Only remove the flower if the bee isn't on it
                if bee_position != (x, y):
                    self.grid[x][y] = None
                    del self.flowers[(x, y)]
                    print(f"Flower at ({x}, {y}) has been depleted")
                    self.add_new_flower()
                else:
                    print(f"Waiting for bee to move before removing depleted flower at ({x}, {y})")
            return 1
        return 0

    def get_flower_nectar(self, x, y):
        """Get the current nectar amount for a flower"""
        return self.flowers.get((x, y), 0)

    def is_valid_position(self, x, y):
        """Check if a position is within the field boundaries"""
        return 0 <= x < self.size and 0 <= y < self.size

    def get_cell(self, x, y):
        """Safely get the contents of a cell"""
        if self.is_valid_position(x, y):
            return self.grid[x][y]
        return None