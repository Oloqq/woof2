import pygame
from collections import namedtuple
from .params import WINDOW_SIZE, Params
from math import ceil, floor

View = namedtuple("View", "left top right bottom cell_size")

class Camera:
    def __init__(self, x, y, zoom):
        self.x: float = x
        self.y: float = y
        self.zoom: float = zoom

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(self.x - 10, -100)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += 10
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(self.y - 10, -100)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += 10
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.zoom = min(Params.zoom_max, self.zoom + 0.1)
        if keys[pygame.K_MINUS]:
            self.zoom = max(Params.zoom_min, self.zoom - 0.1)

    def visible_cells(self, original_size: int) -> View:
        scaled_cell_size = original_size * self.zoom
        cells_on_screen = (ceil(WINDOW_SIZE[0] / scaled_cell_size), ceil(WINDOW_SIZE[1] / scaled_cell_size))
        left_bound = floor(self.x / scaled_cell_size)
        top_bound  = floor(self.y / scaled_cell_size)
        right_bound = left_bound + cells_on_screen[0]
        bottom_bound = top_bound + cells_on_screen[1]
        return View(left_bound, top_bound, right_bound, bottom_bound, scaled_cell_size)