import pygame
import sys

# Initialize pygame
pygame.init()

# Constants for the window size
WIDTH, HEIGHT = 800, 600

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Grid settings
GRID_SIZE = 40  # Size of each grid cell
camera_x, camera_y = 0, 0  # Initial camera position
zoom_level = 1  # Initial zoom level

def draw_grid():
    window.fill(WHITE)
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            rect = pygame.Rect(x - camera_x, y - camera_y, GRID_SIZE * zoom_level, GRID_SIZE * zoom_level)
            pygame.draw.rect(window, BLACK, rect, 1)

def main():
    global camera_x, camera_y, zoom_level

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera_x -= GRID_SIZE
                elif event.key == pygame.K_RIGHT:
                    camera_x += GRID_SIZE
                elif event.key == pygame.K_UP:
                    camera_y -= GRID_SIZE
                elif event.key == pygame.K_DOWN:
                    camera_y += GRID_SIZE
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    zoom_level += 0.1
                elif event.key == pygame.K_MINUS:
                    zoom_level = max(0.1, zoom_level - 0.1)

        draw_grid()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

main()
