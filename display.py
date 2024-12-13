import pygame
import random
from field import Field
from datetime import datetime, timedelta

class Display:
    def __init__(self, field, time_multiplier=1.0):
        self.field = field
        self.cell_size = 9
        self.width = self.field.size * self.cell_size
        self.height = self.field.size * self.cell_size
        self.screen = None
        # Base multiplier is 60 (1 real second = 1 sim minute)
        # Additional time_multiplier affects this base rate
        self.base_multiplier = 60
        self.time_multiplier = float(time_multiplier) * self.base_multiplier
        self.start_time = datetime.now()
        self.sim_start_time = datetime.now()
        self.last_update = datetime.now()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Resource Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def update_time(self):
        current_time = datetime.now()
        real_elapsed = (current_time - self.start_time).total_seconds()
        sim_elapsed_seconds = real_elapsed * self.time_multiplier
        self.sim_time = self.sim_start_time + timedelta(seconds=sim_elapsed_seconds)

    def draw_timestamp(self):
        # Calculate simulation rate for display
        current_rate = self.time_multiplier / self.base_multiplier

        # Create timestamp strings
        real_time_str = f"Real Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        sim_time_str = f"Sim Time: {self.sim_time.strftime('%Y-%m-%d %H:%M:%S')}"
        rate_str = f"Simulation Rate: {current_rate:.1f}x"

        # Render the timestamps
        real_time_surface = self.font.render(real_time_str, True, (255, 255, 255))
        sim_time_surface = self.font.render(sim_time_str, True, (255, 255, 255))
        rate_surface = self.font.render(rate_str, True, (255, 255, 255))

        # Position and draw the timestamps
        self.screen.blit(real_time_surface, (10, 10))
        self.screen.blit(sim_time_surface, (10, 40))
        self.screen.blit(rate_surface, (10, 70))

    def draw_field(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Draw the field and flowers
        for x in range(self.field.size):
            for y in range(self.field.size):
                resource = self.field.grid[x][y]
                if resource is not None:
                    color = (random.randint(100, 255), 
                            random.randint(100, 255), 
                            random.randint(100, 255))
                    pygame.draw.rect(self.screen, color, 
                                   (x * self.cell_size, 
                                    y * self.cell_size, 
                                    self.cell_size, 
                                    self.cell_size))

        # Update and draw the timestamp
        self.update_time()
        self.draw_timestamp()

        pygame.display.flip()

    def run(self):
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
    field = Field()
    display = Display(field)
    display.run()