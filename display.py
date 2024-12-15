import pygame
from datetime import datetime, timedelta

class Display:
    def __init__(self, field, time_multiplier=1.0):
        self.field = field
        self.cell_size = 9
        self.width = 1024  # Fixed window size
        self.height = 768
        self.screen = None
        self.base_multiplier = 60
        self.time_multiplier = float(time_multiplier) * self.base_multiplier
        self.start_time = datetime.now()
        self.sim_start_time = datetime.now()
        self.last_update = datetime.now()

        # Add camera position and movement speed
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 10
        self.zoom_level = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Bee Hive Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def update_time(self):
        """Update simulation time based on real time and multiplier"""
        current_time = datetime.now()
        real_elapsed = (current_time - self.start_time).total_seconds()
        sim_elapsed_seconds = real_elapsed * self.time_multiplier
        self.sim_time = self.sim_start_time + timedelta(seconds=sim_elapsed_seconds)

    def draw_timestamp(self):
        """Draw timestamp information on the screen"""
        current_rate = self.time_multiplier / self.base_multiplier

        real_time_str = f"Real Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        sim_time_str = f"Sim Time: {self.sim_time.strftime('%Y-%m-%d %H:%M:%S')}"
        rate_str = f"Simulation Rate: {current_rate:.1f}x"

        real_time_surface = self.font.render(real_time_str, True, (255, 255, 255))
        sim_time_surface = self.font.render(sim_time_str, True, (255, 255, 255))
        rate_surface = self.font.render(rate_str, True, (255, 255, 255))

        self.screen.blit(real_time_surface, (10, 10))
        self.screen.blit(sim_time_surface, (10, 40))
        self.screen.blit(rate_surface, (10, 70))

    def draw_stats(self):
        """Draw simulation statistics in the top center of the screen"""
        stats = [f"Bees: {len(self.field.hive.bees)}"]

        # Only add queen stats if she's alive
        if self.field.hive.queen:
            stats.extend([
                f"Queen's Nectar: {self.field.hive.queen.nectar_collected}/{self.field.hive.queen.nectar_needed}",
                f"Eggs Laid: {self.field.hive.queen.eggs_laid}",
                f"Queen State: {self.field.hive.queen.state.name}"
            ])
        else:
            stats.append("Queen has died! 👑")
            
        print("Stats being drawn:", stats)  # Debug print

        # Calculate total width of stats display
        max_width = 0
        stat_surfaces = []
        for stat in stats:
            surface = self.font.render(stat, True, (255, 255, 255))
            stat_surfaces.append(surface)
            max_width = max(max_width, surface.get_width())

        # Draw stats centered at top
        start_x = (self.width - max_width) // 2
        for i, surface in enumerate(stat_surfaces):
            self.screen.blit(surface, (start_x, 10 + (30 * i)))


    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Camera movement with arrow keys or WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.camera_x -= self.camera_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.camera_x += self.camera_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.camera_y -= self.camera_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.camera_y += self.camera_speed

        # Zoom controls with + and - keys
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.zoom_level = min(self.zoom_level + 0.02, self.max_zoom)
        if keys[pygame.K_MINUS]:
            self.zoom_level = max(self.zoom_level - 0.02, self.min_zoom)

        # Reset view with R key
        if keys[pygame.K_r]:
            self.camera_x = 0
            self.camera_y = 0
            self.zoom_level = 1.0

        # Ensure camera doesn't go too far out of bounds
        max_x = self.field.size * self.cell_size * self.zoom_level - self.width
        max_y = self.field.size * self.cell_size * self.zoom_level - self.height
        self.camera_x = max(min(self.camera_x, max_x), 0)
        self.camera_y = max(min(self.camera_y, max_y), 0)

    def world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates"""
        screen_x = int(x * self.cell_size * self.zoom_level - self.camera_x)
        screen_y = int(y * self.cell_size * self.zoom_level - self.camera_y)
        return screen_x, screen_y

    def draw_field(self):
        self.screen.fill((0, 0, 0))  # Black background

        # Calculate visible area
        cell_size_zoomed = int(self.cell_size * self.zoom_level)
        start_x = max(0, int(self.camera_x / cell_size_zoomed))
        start_y = max(0, int(self.camera_y / cell_size_zoomed))
        end_x = min(self.field.size, start_x + self.width // cell_size_zoomed + 2)
        end_y = min(self.field.size, start_y + self.height // cell_size_zoomed + 2)

        # Draw the field and resources
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                cell = self.field.grid[x][y]
                if cell is not None:
                    if cell == "hive":
                        color = (255, 255, 0)  # Yellow for hive
                    elif cell == "flower":
                        color = (0, 255, 0)  # Green for flowers

                    screen_x, screen_y = self.world_to_screen(x, y)
                    pygame.draw.rect(self.screen, color, 
                                (screen_x, screen_y, 
                                    cell_size_zoomed, cell_size_zoomed))

        # Draw queen's path and queen only if she exists
        if self.field.hive.queen:
            # Draw queen's path
            if self.field.hive.queen.path:
                for pos in self.field.hive.queen.path:
                    screen_x, screen_y = self.world_to_screen(pos[0], pos[1])
                    pygame.draw.rect(self.screen, (0, 100, 0),  # Light green
                                (screen_x, screen_y, 
                                    max(1, cell_size_zoomed // 3), 
                                    max(1, cell_size_zoomed // 3)))

            # Draw queen
            queen_x, queen_y = self.world_to_screen(
                self.field.hive.queen.x, 
                self.field.hive.queen.y
            )

            # Debug print to verify queen's position
            print(f"Drawing queen at world coords: ({self.field.hive.queen.x}, {self.field.hive.queen.y})")
            print(f"Screen coords: ({queen_x}, {queen_y})")

            # Draw queen (larger than other bees)
            pygame.draw.rect(self.screen, (255, 215, 0),  # Golden yellow
                            (queen_x, queen_y, 
                            cell_size_zoomed, cell_size_zoomed))
            # Draw black crown
            pygame.draw.rect(self.screen, (0, 0, 0),
                            (queen_x + cell_size_zoomed//3, 
                            queen_y + cell_size_zoomed//3,
                            cell_size_zoomed//3, 
                            cell_size_zoomed//3))

        # Draw stats and other UI elements
        self.draw_stats()
        self.update_time()
        self.draw_timestamp()

        # Draw navigation help text
        help_text = self.font.render("Arrow Keys/WASD to move, +/- to zoom, R to reset view", 
                                    True, (255, 255, 255))
        self.screen.blit(help_text, (10, self.height - 40))

        pygame.display.flip()

    def run(self):
        print("Initializing display...")
        self.init_pygame()
        print("Display initialized successfully")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle camera movement and zoom
            self.handle_input()

            # Update queen bee
            if self.field.hive.queen:
                self.field.hive.queen.update()

            self.draw_field()
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()