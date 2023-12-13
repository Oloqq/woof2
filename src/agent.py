from .cell import Cell, Terrain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation

class Agent:
    kind: str = "abstract"

    def __init__(self, simulation, x: int, y: int):
        self.sim: Simulation = simulation
        self.x = x
        self.y = y

    def step(self):
        self.move(1, 0)

    def move(self, dx, dy):
        x = (self.x + dx) % self.sim.width
        y = (self.y + dy) % self.sim.height
        cell: Cell = self.sim.grid[x][y]
        if cell.terrain == Terrain.Grass:
            self.x = x
            self.y = y
