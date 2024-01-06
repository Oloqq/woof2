from enum import Enum, auto

class Terrain(Enum):
    Grass = auto(),
    Water = auto()

class Cell:
    def __init__(self):
        self.scent_strength = 1
        self.scent_pack = -1
        self.terrain = Terrain.Grass