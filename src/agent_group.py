from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation

class AgentGroup:
    kind: str = "abstract"

    def __init__(self, sim, size: int, territory_length: int, x: int, y: int):
        self.sim: Simulation = sim
        self.size = size
        self.xmin = x - territory_length // 2
        self.xmax = self.xmin + territory_length
        self.ymin = y - territory_length // 2
        self.ymax = self.ymin + territory_length

    def move(self, dx, dy):
        self.x = (self.x + dx) % self.sim.width
        self.y = (self.y + dy) % self.sim.height