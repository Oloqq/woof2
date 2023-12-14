from math import floor, ceil
from tkinter.tix import CELL
from turtle import left
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

    cx, cy, scale = (camera.x, camera.y, camera.zoom)
    scaled_cell_size = CELL_SIZE_PX * scale
    cells_on_screen = (ceil(WINDOW_SIZE[0] / scaled_cell_size), ceil(WINDOW_SIZE[1] / scaled_cell_size))
    leftmost = max(0, floor(cx / scaled_cell_size))
    topmost  = max(0, floor(cy / scaled_cell_size))

    for ix, x in enumerate(range(leftmost, min(simulation.width, leftmost + cells_on_screen[0]))):
        for iy, y in enumerate(range(topmost, min(simulation.height, topmost + cells_on_screen[1]))):
            rect = pygame.Rect(ix * scaled_cell_size, iy * scaled_cell_size, scaled_cell_size, scaled_cell_size)
            match simulation.grid[x][y].terrain:
                case Terrain.Grass:
                    pygame.draw.rect(surface, GRASS_COLOR, rect)
                case Terrain.Water:
                    pygame.draw.rect(surface, WATER_COLOR, rect)
            if scale > 0.6:
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
