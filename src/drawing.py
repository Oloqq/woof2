import pygame
from .wolf_simulation import Simulation, Terrain
from .params import Params, WINDOW_SIZE
from .wolf import Wolf
from .deer import Deer
from .deer_herd import Herd
from .camera import Camera

WHITE = (255, 255, 255)
GRASS_COLOR = (0, 160, 0)
WATER_COLOR = (0, 0, 160)
GRID_COLOR = (0, 0, 0)
CELL_SIZE_PX = 40

def draw_ground(simulation: Simulation, camera: Camera) -> pygame.Surface:
    surface = pygame.Surface(WINDOW_SIZE)
    surface.fill(WHITE)

    view = camera.visible_cells(CELL_SIZE_PX)

    for ix, x in enumerate(range(view.left, min(simulation.width, view.right))):
        for iy, y in enumerate(range(view.top, min(simulation.height, view.bottom))):
            rect = pygame.Rect(ix * view.cell_size, iy * view.cell_size, view.cell_size, view.cell_size)
            match simulation.grid[x][y].terrain:
                case Terrain.Grass:
                    pygame.draw.rect(surface, GRASS_COLOR, rect)
                case Terrain.Water:
                    pygame.draw.rect(surface, WATER_COLOR, rect)
            if camera.zoom > 0.6:
                pygame.draw.rect(surface, GRID_COLOR, rect, 1)
    return surface

def draw_agents(simulation: Simulation, camera: Camera) -> pygame.Surface:
    assert simulation.agents.keys() == set([Wolf.kind])
    assert simulation.agent_groups.keys() == set([Herd.kind])

    surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    view = camera.visible_cells(CELL_SIZE_PX)

    for agent in simulation.agents[Wolf.kind]:
        rect = pygame.Rect((agent.x - view.left) * view.cell_size, (agent.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
        pygame.draw.rect(surface, (100, 100, 100), rect)

    for agent in simulation.get_deers():
        rect = pygame.Rect((agent.x - view.left) * view.cell_size, (agent.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
        pygame.draw.rect(surface, (205, 133, 63), rect)

    return surface
