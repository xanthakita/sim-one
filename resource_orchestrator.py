import random
from field import Field

class Resource:
    def __init__(self, name, value_collected, number_of_collections):
        """
        Initialize a resource with its properties.
        """
        self.name = name
        self.value_collected = value_collected
        self.number_of_collections = number_of_collections

    def collect(self):
        """
        Simulate collecting from the resource.
        Decrease the number of collections left and return the value collected.
        """
        if self.number_of_collections > 0:
            self.number_of_collections -= 1
            return self.value_collected
        else:
            return 0  # Resource is depleted

    def is_depleted(self):
        """
        Check if the resource is depleted.
        """
        return self.number_of_collections <= 0

    def __str__(self):
        """
        String representation of the resource.
        """
        return f"{self.name} (Value: {self.value_collected}, Remaining: {self.number_of_collections})"

class ResourceOrchestrator:
    def __init__(self, field, resource_type, count):
        """
        Initialize the orchestrator with a field, resource type, and count.
        :param field: The Field object where resources will be placed.
        :param resource_type: A tuple defining the resource (name, value_collected, number_of_collections).
        :param count: The number of resources to place in the field.
        """
        self.field = field
        self.resource_type = resource_type
        self.count = count
        self.resources = []

    def spread_resources(self):
        """
        Randomly spread resources across the field.
        """
        name, value_collected, number_of_collections = self.resource_type
        for _ in range(self.count):
            while True:
                x = random.randint(0, self.field.size - 1)
                y = random.randint(0, self.field.size - 1)
                if self.field.grid[x][y] is None:  # Only place resource in an empty cell
                    resource = Resource(name, value_collected, number_of_collections)
                    self.field.grid[x][y] = resource
                    self.resources.append((x, y, resource))
                    break

    def display_resources(self):
        """
        Display all resources and their locations.
        """
        for x, y, resource in self.resources:
            print(f"Resource at ({x}, {y}): {resource}")