import pygame
from .wolf_simulation import Simulation, Terrain
from .params import Params, WINDOW_SIZE
from .wolves_pack import Pack
from .deer_herd import Herd
from .camera import Camera

GRASS_COLOR = (46, 186, 48)
WATER_COLOR = (46, 114, 186)
GRID_COLOR = (0, 0, 0)
CELL_SIZE_PX = 10
DEER_COLOR = (186, 118, 46)
WOLF_COLOR = (100, 100, 100)
HUNGRY_WOLF_COLOR = (122, 42, 42)

def draw_ground(simulation: Simulation, camera: Camera) -> pygame.Surface:
    surface = pygame.Surface(WINDOW_SIZE)
    surface.fill(GRID_COLOR)

    view = camera.visible_cells(CELL_SIZE_PX)

    for ix, x in enumerate(range(view.left, min(simulation.width, view.right))):
        for iy, y in enumerate(range(view.top, min(simulation.height, view.bottom))):
            rect = pygame.Rect(ix * view.cell_size, iy * view.cell_size, view.cell_size, view.cell_size)
            match simulation.grid[x][y].terrain:
                case Terrain.Grass:
                    pygame.draw.rect(surface, GRASS_COLOR, rect)
                case Terrain.Water:
                    pygame.draw.rect(surface, WATER_COLOR, rect)
    return surface

def draw_agents(simulation: Simulation, camera: Camera) -> pygame.Surface:
    assert simulation.agent_groups.keys() == set([Herd.kind, Pack.kind])

    surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    view = camera.visible_cells(CELL_SIZE_PX)

    for agent in simulation.get_deers():
        rect = pygame.Rect((agent.x - view.left) * view.cell_size, (agent.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
        pygame.draw.rect(surface, (DEER_COLOR), rect)

    for agent in simulation.get_wolves():
        rect = pygame.Rect((agent.x - view.left) * view.cell_size, (agent.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
        if (agent.endurance >= Params.wolf_hunger_threshold):
            pygame.draw.rect(surface, (WOLF_COLOR), rect)
        else:
            pygame.draw.rect(surface, (HUNGRY_WOLF_COLOR), rect)


    # this is used to see to coordinates of herds and packs
    # for pack in simulation.agent_groups[Pack.kind]:
    #     rect = pygame.Rect((pack.x - view.left) * view.cell_size, (pack.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
    #     pygame.draw.rect(surface, (255, 0, 0), rect)

    # for herd in simulation.agent_groups[Herd.kind]:
    #     rect = pygame.Rect((herd.x - view.left) * view.cell_size, (herd.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
    #     pygame.draw.rect(surface, (255, 255, 0), rect)

    return surface
