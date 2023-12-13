from enum import Enum, auto

class Terrain(Enum):
    Grass = auto(),
    Water = auto()

class Cell:
    def __init__(self):
        self.scent = 0
        self.terrain = Terrain.Grass