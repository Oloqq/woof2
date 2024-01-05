from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation
from .agent import Agent

class Deer(Agent):
    kind: str = "deer"
    path: list[tuple[int, int]] = []

    def __init__(self, simulation: Simulation, x: int, y: int):
        super().__init__(simulation, x, y)

    def step(self, dx, dy):
        if len(self.path) > 0 and self.sim.get_cell_content(self.path[0][0], self.path[0][1]) is None:
            step = self.path.pop(0)
            return self.move(step[0] - self.x, step[1] - self.y)
        elif self.sim.get_cell_content(self.x + dx, self.y + dy) is None:
            return self.move(dx, dy)
        return False
