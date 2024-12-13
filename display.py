import pygame
import random
from field import Field

class Display:
    def __init__(self, field):
        """
        Initialize the display with the field.
        """
        self.field = field
        self.cell_size = 9  # Each square foot will be 9x9 pixels
        self.width = self.field.size * self.cell_size
        self.height = self.field.size * self.cell_size
        self.screen = None

    def init_pygame(self):
        """
        Initialize Pygame and create the display window.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Resource Simulation")
        self.clock = pygame.time.Clock()

    def draw_field(self):
        """
        Draw the field and resources on the screen.
        """
        self.screen.fill((0, 0, 0))  # Black background

        for x in range(self.field.size):
            for y in range(self.field.size):
                resource = self.field.grid[x][y]
                if resource is not None:
                    # Random color for flowers
                    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                    pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        pygame.display.flip()  # Update the display

    def run(self):
        """
        Main loop to run the display.
        """
        self.init_pygame()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_field()
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()

if __name__ == "__main__":
    # Example usage
    field = Field()
    display = Display(field)
    display.run()