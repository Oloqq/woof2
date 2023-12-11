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

def main():
    global camera_x, camera_y, zoom_level

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera_x -= 10
                elif event.key == pygame.K_RIGHT:
                    camera_x += 10
                elif event.key == pygame.K_UP:
                    camera_y -= 10
                elif event.key == pygame.K_DOWN:
                    camera_y += 10
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    zoom_level = min(2, zoom_level + 0.1)
                elif event.key == pygame.K_MINUS:
                    zoom_level = max(0.5, zoom_level - 0.1)

        # Draw the grid
        grid_surface = draw_grid()

        # Scale the grid surface
        scaled_surface = pygame.transform.scale(grid_surface, (int(WIDTH * zoom_level), int(HEIGHT * zoom_level)))

        # Clear the window
        window.fill(WHITE)

        # Blit the scaled surface onto the window at the adjusted camera position
        window.blit(scaled_surface, (-camera_x, -camera_y))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()