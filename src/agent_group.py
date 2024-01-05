from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation

class AgentGroup:
    kind: str = "abstract"
    xmin = property(lambda self: self.x - self.territory_length // 2)
    xmax = property(lambda self: self.xmin + self.territory_length)
    ymin = property(lambda self: self.y - self.territory_length // 2)
    ymax = property(lambda self: self.ymin + self.territory_length)

    def __init__(self, sim, size: int, territory_length: int, x: int, y: int):
        self.sim: Simulation = sim
        self.size = size
        self.territory_length = territory_length
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x = (self.x + dx) % self.sim.width
        self.y = (self.y + dy) % self.sim.height

