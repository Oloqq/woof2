import pygame
from .wolf_simulation import Simulation, Terrain
from .params import Params, WINDOW_SIZE
from .wolf_pack import Pack
from .deer_herd import Herd
from .camera import Camera

GRASS_COLOR = (46, 186, 48)
WATER_COLOR = (46, 114, 186)
GRID_COLOR = (0, 0, 0)
CELL_SIZE_PX = 10
DEER_COLOR = (186, 118, 46)
WOLF_COLOR = (100, 100, 100)
HUNGRY_WOLF_COLOR = (122, 42, 42)

PACK_COLORS = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128)]

def draw_tile(surface: pygame.Surface, simulation: Simulation, x: int, y: int, at: pygame.Rect, overlay: str|None):
    match simulation.grid[x][y].terrain:
        case Terrain.Grass:
            match overlay:
                case "scent":
                    color = PACK_COLORS[simulation.grid[x][y].scent_pack] if simulation.grid[x][y].scent_pack < len(PACK_COLORS) else (0, 0, 0)
                    pygame.draw.rect(surface, color, at)
                case None:
                    pygame.draw.rect(surface, GRASS_COLOR, at)
                case _:
                    raise Exception(f"unhandled overlay '{overlay}'")
        case Terrain.Water:
            pygame.draw.rect(surface, WATER_COLOR, at)

def draw_ground(simulation: Simulation, camera: Camera, overlay: str|None) -> pygame.Surface:
    surface = pygame.Surface(WINDOW_SIZE)
    surface.fill(GRID_COLOR)

    view = camera.visible_cells(CELL_SIZE_PX)

    for ix, x in enumerate(range(view.left, min(simulation.width, view.right))):
        for iy, y in enumerate(range(view.top, min(simulation.height, view.bottom))):
            rect = pygame.Rect(ix * view.cell_size, iy * view.cell_size, view.cell_size, view.cell_size)
            draw_tile(surface, simulation, x, y, rect, overlay)
    return surface

def draw_agents(simulation: Simulation, camera: Camera, overlay: str|None) -> pygame.Surface:
    assert simulation.agent_groups.keys() == set([Herd.kind, Pack.kind])

    surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    view = camera.visible_cells(CELL_SIZE_PX)

    for agent in simulation.get_deer():
        rect = pygame.Rect((agent.x - view.left) * view.cell_size, (agent.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
        pygame.draw.rect(surface, (DEER_COLOR), rect)

    for agent in simulation.get_wolves():
        rect = pygame.Rect((agent.x - view.left) * view.cell_size, (agent.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
        match overlay:
            case "scent":
                pack_color = PACK_COLORS[agent.pack.id] if agent.pack.id < len(PACK_COLORS) else WOLF_COLOR
                pygame.draw.rect(surface, pack_color, rect)
            case None:
                if (agent.endurance >= Params.wolf_hunger_threshold):
                    pygame.draw.rect(surface, (WOLF_COLOR), rect)
                else:
                    pygame.draw.rect(surface, (HUNGRY_WOLF_COLOR), rect)
            case _:
                raise Exception(f"unhandled overlay '{overlay}'")


    # this is used to see to coordinates of herds and packs
    # for pack in simulation.agent_groups[Pack.kind]:
    #     rect = pygame.Rect((pack.x - view.left) * view.cell_size, (pack.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
    #     pygame.draw.rect(surface, (255, 0, 0), rect)

    # for herd in simulation.agent_groups[Herd.kind]:
    #     rect = pygame.Rect((herd.x - view.left) * view.cell_size, (herd.y - view.top) * view.cell_size, view.cell_size, view.cell_size)
    #     pygame.draw.rect(surface, (255, 255, 0), rect)

    return surface
