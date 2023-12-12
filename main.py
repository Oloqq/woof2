import pygame

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Grid and camera settings
GRID_SIZE = 40
camera_x, camera_y = 0, 0
zoom_level = 1
running = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_grid():
    # Create a surface for the grid (world)
    grid_surface = pygame.Surface((WIDTH, HEIGHT))
    grid_surface.fill(WHITE)

    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(grid_surface, BLACK, rect, 1)

    return grid_surface

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

def main():
    clock = pygame.time.Clock()

    while running:
        process_events()



        grid_surface = draw_grid()
        scaled_surface = pygame.transform.scale(grid_surface, (int(WIDTH * zoom_level), int(HEIGHT * zoom_level)))
        window.fill(WHITE)
        window.blit(scaled_surface, (-camera_x, -camera_y)) # Apply camera translation

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()