import pygame
from .wolf_simulation import Simulation
from .agent import Agent
from .wolf import Wolf
from .deer import Deer

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Grid and camera settings
camera_x, camera_y = 0, 0
zoom_level = 1
running = True

simulation = Simulation((40, 20))
simulation.agents.extend([
    Agent(0, 0),
    Wolf(10, 0),
    Deer(15, 0)
    ])

# Visualization
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CELL_SIZE_PX = 40


def move_camera():
    global camera_x, camera_y, zoom_level
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

def process_events():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("run/pause")
            if event.key == pygame.K_TAB:
                simulation.step()

def draw_grid(surface: pygame.Surface, simulation: Simulation):
    for x in range(simulation.width):
        for y in range(simulation.height):
            rect = pygame.Rect(x * CELL_SIZE_PX, y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
            pygame.draw.rect(surface, BLACK, rect, 1)
    return surface

def draw_agents(surface: pygame.Surface, simulation: Simulation):
    for agent in simulation.agents:
        match agent.kind:
            case "abstract":
                rect = pygame.Rect(agent.x * CELL_SIZE_PX, agent.y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
                pygame.draw.rect(surface, (255, 0, 0), rect)
            case "wolf":
                rect = pygame.Rect(agent.x * CELL_SIZE_PX, agent.y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
                pygame.draw.rect(surface, (120, 120, 120), rect)
            case "deer":
                rect = pygame.Rect(agent.x * CELL_SIZE_PX, agent.y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
                pygame.draw.rect(surface, (255, 255, 0), rect)
            case _:
                raise NotImplementedError(f"can't display agent of kind {agent.kind}")

def draw_world(simulation) -> pygame.Surface:
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(WHITE)

    draw_grid(surface, simulation)
    draw_agents(surface, simulation)

    return surface

def draw_ui() -> pygame.Surface:
    raise NotImplementedError

def main():
    clock = pygame.time.Clock()

    while running:
        process_events()
        move_camera()

        # if should perform step then update the simulation

        world_surface = draw_world(simulation)
        scaled_surface = pygame.transform.scale(world_surface, (int(WIDTH * zoom_level), int(HEIGHT * zoom_level)))
        window.fill(WHITE)
        window.blit(scaled_surface, (-camera_x, -camera_y)) # Draw surface while applying camera translation

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()