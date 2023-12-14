import pygame
from .wolf_simulation import Simulation, Terrain
from .wolf import Wolf
from .deer import Deer
from .deer_herd import Herd

WHITE = (255, 255, 255)
GRASS_COLOR = (0, 160, 0)
WATER_COLOR = (0, 0, 160)
GRID_COLOR = (0, 0, 0)
CELL_SIZE_PX = 20

def draw_ground(simulation: Simulation) -> pygame.Surface:
    surface = pygame.Surface((simulation.width * CELL_SIZE_PX, simulation.height * CELL_SIZE_PX))
    surface.fill(WHITE)
    for x in range(simulation.width):
        for y in range(simulation.height):
            rect = pygame.Rect(x * CELL_SIZE_PX, y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
            match simulation.grid[x][y].terrain:
                case Terrain.Grass:
                    pygame.draw.rect(surface, GRASS_COLOR, rect)
                case Terrain.Water:
                    pygame.draw.rect(surface, WATER_COLOR, rect)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)
    return surface

def draw_agents(simulation: Simulation) -> pygame.Surface:
    surface = pygame.Surface((simulation.width * CELL_SIZE_PX, simulation.height * CELL_SIZE_PX), pygame.SRCALPHA)
    assert simulation.agents.keys() == set([Wolf.kind])
    assert simulation.agent_groups.keys() == set([Herd.kind])
    for agent in simulation.agents[Wolf.kind]:
        rect = pygame.Rect(agent.x * CELL_SIZE_PX, agent.y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
        pygame.draw.rect(surface, (100, 100, 100), rect)

    for deer in simulation.get_deers():
        rect = pygame.Rect(deer.x * CELL_SIZE_PX, deer.y * CELL_SIZE_PX, CELL_SIZE_PX, CELL_SIZE_PX)
        pygame.draw.rect(surface, (205, 133, 63), rect)

    return surface
