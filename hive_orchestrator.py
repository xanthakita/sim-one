import math
import random
from enum import Enum
import numpy as np

class BeeState(Enum):
    SEARCHING = 1
    RETURNING = 2
    IN_HIVE = 3

class HiveOrchestrator:
    def __init__(self, field):
        self.field = field
        self.hive_location = self.field.place_hive()  # Place the hive on the field
        self.age = 0  # Days the hive has been alive
        self.queen = None  # The queen bee
        self.bees = []  # List of all bees in the hive
        self.nectar = 0  # Nectar collected
        self.honey = 0  # Honey produced
        self.known_flowers = []  # List to store known flower locations

    def add_bee(self, bee):
        self.bees.append(bee)

    def collect_nectar(self, amount):
        self.nectar += amount

    def produce_honey(self):
        # Convert nectar to honey (e.g., 10 nectar = 1 honey)
        honey_produced = self.nectar // 10
        self.honey += honey_produced
        self.nectar -= honey_produced * 10

    def update(self):
        # Increment hive age
        self.age += 1

        # Produce honey
        self.produce_honey()

        # Update all bees
        for bee in self.bees:
            bee.update()

        # Check if the hive should split (e.g., once a year)
        if self.age % 365 == 0 and len(self.bees) > 50:
            self.split_hive()

    def split_hive(self):
        print("The hive is splitting!")
        # Logic for hive splitting (e.g., create a new hive)

    def __str__(self):
        return (f"Hive Age: {self.age} days\n"
                f"Bees: {len(self.bees)}\n"
                f"Nectar: {self.nectar}\n"
                f"Honey: {self.honey}")

class QueenBee:
    def __init__(self, hive):
        self.hive = hive
        self.nectar_collected = 0
        self.lifespan = 1460 * 10  # 40 years in simulation days
        self.age = 0
        self.x, self.y = hive.hive_location
        self.state = BeeState.IN_HIVE
        self.search_radius = 1
        self.search_angle = random.uniform(0, 2 * math.pi)
        self.path = []  # Store the path taken
        self.last_flower = None
        self.zigzag_offset = 0
        self.zigzag_direction = 1
        self.eggs_laid = 0
        self.nectar_needed = 10  # Nectar needed to lay eggs
        self.move_speed = 1  # How many cells to move per update
        self.forward_steps = 0
        self.steps_before_turn = 15  # Move forward this many steps before changing direction
        self.return_path = []  # Store the path to return on
        self.known_flower_locations = []  # Store locations of flowers we've found
        print(f"Queen initialized at position: ({self.x}, {self.y})")

    def update(self):
        """Main update loop for the queen"""
        self.age += 1
        if self.age > self.lifespan:
            print("The queen has died!")
            self.hive.queen = None
            return

        # Handle state transitions
        if self.state == BeeState.IN_HIVE:
            if self.nectar_collected >= self.nectar_needed:
                print(f"Queen laying eggs! Total eggs laid: {self.eggs_laid + 1}")
                print(f"Using {self.nectar_needed} nectar for eggs")
                self.nectar_collected -= self.nectar_needed
                self.eggs_laid += 1
                print(f"Remaining nectar: {self.nectar_collected}")

            # Start searching if we need more nectar
            if self.nectar_collected < self.nectar_needed:
                print("Queen leaving hive to search for nectar!")
                self.state = BeeState.SEARCHING
                self.x, self.y = self.hive.hive_location
                self.search_radius = 1
                self.search_angle = random.uniform(0, 2 * math.pi)

        # Move the queen
        self.move()

        # Check if we've reached the hive while returning
        if self.state == BeeState.RETURNING:
            if abs(self.x - self.hive.hive_location[0]) <= 1 and \
            abs(self.y - self.hive.hive_location[1]) <= 1:
                self.perform_waggle_dance()
                self.state = BeeState.IN_HIVE
                print(f"Queen returned to hive with nectar! Current total: {self.nectar_collected}")
                


    def collect_nectar(self):
        """Modified nectar collection with flower location memory"""
        if self.hive.field.grid[self.x][self.y] == "flower":
            # Collect from the flower using the field's method
            nectar_collected = self.hive.field.collect_nectar_from_flower(self.x, self.y)

            if nectar_collected:
                self.nectar_collected += nectar_collected
                self.last_flower = (self.x, self.y)
                if (self.x, self.y) not in self.known_flower_locations:
                    self.known_flower_locations.append((self.x, self.y))

                print(f"Queen collected nectar at ({self.x}, {self.y})")
                print(f"Current nectar: {self.nectar_collected}/{self.nectar_needed}")

                # Only switch to RETURNING if we've collected enough nectar
                if self.nectar_collected >= self.nectar_needed:
                    print("Queen has collected enough nectar, returning to hive!")
                    self.state = BeeState.RETURNING
                return True
        return False

    def check_surroundings(self):
        """Check for flowers in the immediate vicinity."""
        search_range = 2  # Increased search range
        for dx in range(-search_range, search_range + 1):
            for dy in range(-search_range, search_range + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < self.hive.field.size and 0 <= ny < self.hive.field.size:
                    if self.hive.field.grid[nx][ny] == "flower":
                        self.last_flower = (nx, ny)
                        self.state = BeeState.RETURNING
                        return True
        return False

    def spiral_search(self):
        """Calculate next position in spiral pattern"""
        # Increment angle and radius for spiral pattern
        self.search_angle += 0.1  # Slower angle increment for wider spiral

        # Calculate new position using parametric equations for spiral
        dx = self.search_radius * math.cos(self.search_angle)
        dy = self.search_radius * math.sin(self.search_angle)

        # Calculate new position relative to hive
        new_x = int(self.hive.hive_location[0] + dx)
        new_y = int(self.hive.hive_location[1] + dy)

        # Increment search radius periodically
        if self.search_angle >= 2 * math.pi:
            self.search_angle = 0
            self.search_radius += 1

        # Ensure within bounds
        new_x = max(0, min(new_x, self.hive.field.size - 1))
        new_y = max(0, min(new_y, self.hive.field.size - 1))

        print(f"Spiral search: new position ({new_x}, {new_y})")  # Debug print
        return new_x, new_y

    def move(self):
        """Modified move method with nectar collection"""
        old_x, old_y = self.x, self.y  # Store previous position
        
        
        if self.state == BeeState.SEARCHING:
            # First check if we know of any flowers
            if self.known_flower_locations:
                target = self.known_flower_locations[0]
                if self.hive.field.grid[target[0]][target[1]] != "flower":
                    # Flower is gone, remove it and continue searching
                    self.known_flower_locations.pop(0)
                    new_x, new_y = self.spiral_search()
                else:
                    # Move toward known flower
                    dx = target[0] - self.x
                    dy = target[1] - self.y
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance > 0:
                        self.x += int((dx/distance) * self.move_speed)
                        self.y += int((dy/distance) * self.move_speed)
            else:
                new_x, new_y = self.spiral_search()
                self.x, self.y = new_x, new_y

            # After moving, check if we're on a flower and collect nectar
            if self.hive.field.grid[self.x][self.y] == "flower":
                if self.collect_nectar():
                    print(f"Queen collected nectar at ({self.x}, {self.y})")
                    if self.nectar_collected >= self.nectar_needed:
                        print(f"Total nectar collected: {self.nectar_collected}")
                        self.state = BeeState.RETURNING

        elif self.state == BeeState.RETURNING:
            self.return_to_hive()

        # After moving, if we were on a depleted flower, now we can remove it
        if self.hive.field.grid[old_x][old_y] == "flower" and (old_x, old_y) not in self.hive.field.flowers:
            self.hive.field.grid[old_x][old_y] = None
            print(f"Removing depleted flower at ({old_x}, {old_y}) after bee moved")
        

    def zigzag_return(self):
        """Method for returning to hive in a zigzag pattern"""
        if not self.last_flower:
            return self.hive.hive_location[0], self.hive.hive_location[1]  # Return as tuple

        # Calculate direct vector to hive
        dx = self.hive.hive_location[0] - self.x
        dy = self.hive.hive_location[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < 1:
            return self.hive.hive_location[0], self.hive.hive_location[1]  # Return as tuple

        # Add zigzag pattern
        self.zigzag_offset += self.zigzag_direction * 0.5
        if abs(self.zigzag_offset) > 2:
            self.zigzag_direction *= -1

        # Normalize direction and add zigzag
        dx = dx/distance + self.zigzag_offset
        dy = dy/distance

        new_x = int(self.x + dx)
        new_y = int(self.y + dy)

        # Ensure within bounds
        new_x = max(0, min(new_x, self.hive.field.size - 1))
        new_y = max(0, min(new_y, self.hive.field.size - 1))

        return new_x, new_y

    def return_to_hive(self):
        """Return using stored path"""
        if not self.return_path:
            dx = self.hive.hive_location[0] - self.x
            dy = self.hive.hive_location[1] - self.y
        else:
            next_pos = self.return_path.pop()
            dx = next_pos[0] - self.x
            dy = next_pos[1] - self.y

        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            self.x += int((dx/distance) * self.move_speed)
            self.y += int((dy/distance) * self.move_speed)

    def perform_waggle_dance(self):
        """Share information about flower location with the hive"""
        if self.last_flower:
            print(f"Queen performing waggle dance to share flower location: {self.last_flower}")
            self.hive.known_flowers.append({
                'location': self.last_flower,
                'path': self.return_path.copy()
            })

class Larva:
    def __init__(self, hive):
        self.hive = hive
        self.age = 0
        self.development_time = 21  # 21 days to develop

    def update(self):
        self.age += 1
        if self.age >= self.development_time:
            # Decide what type of bee to become
            if len([bee for bee in self.hive.bees if isinstance(bee, WorkerBee)]) < 50:
                self.hive.add_bee(WorkerBee(self.hive))
            elif len([bee for bee in self.hive.bees if isinstance(bee, DroneBee)]) < 10:
                self.hive.add_bee(DroneBee(self.hive))
            else:
                self.hive.add_bee(QueenBee(self.hive))
            self.hive.bees.remove(self)