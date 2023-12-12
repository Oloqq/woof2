import pygame

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Grid and camera settings
camera_x, camera_y = 0, 0
zoom_level = 1
running = True
GRID = (40, 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_grid(surface: pygame.Surface):
    CELL_SIZE_PX = 40
    for x in range(GRID[0]):
        for y in range(GRID[1]):
            rect = pygame.Rect(x * CELL_SIZE_PX, y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
            pygame.draw.rect(surface, BLACK, rect, 1)
    return surface

def process_events():
    global camera_x, camera_y, zoom_level, running

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera_x -= 10
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera_x += 10
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        camera_y -= 10
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        camera_y += 10
    if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
        zoom_level = min(2, zoom_level + 0.1)
    if keys[pygame.K_MINUS]:
        zoom_level = max(0.5, zoom_level - 0.1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("run/pause")
            if event.key == pygame.K_TAB:
                print("step")

def draw_world() -> pygame.Surface:
    grid_surface = pygame.Surface((WIDTH, HEIGHT))
    grid_surface.fill(WHITE)

    draw_grid(grid_surface)
    # TODO draw agents

    return grid_surface

def main():
    clock = pygame.time.Clock()
    # simulation = Simula

    while running:
        process_events()

        # if should perform step then update the simulation

        world_surface = draw_world()
        scaled_surface = pygame.transform.scale(world_surface, (int(WIDTH * zoom_level), int(HEIGHT * zoom_level)))
        window.fill(WHITE)
        window.blit(scaled_surface, (-camera_x, -camera_y)) # Draw surface while applying camera translation

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()