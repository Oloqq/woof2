from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation
from .agent import Agent
from .params import Params
import random

class Wolf(Agent):
    kind: str = "wolf"

    def __init__(self, simulation: Simulation, x: int, y: int):
        super().__init__(simulation, x, y)
        self.speed = 1
        self.endurance = random.randint(Params.wolf_hunger_threshold, Params.wolf_max_endurance)

    def step(self, dx, dy):
        cell_content = self.sim.get_cell_content(self.x + dx, self.y + dy)
        if cell_content is not None and cell_content.kind == Wolf.kind:
            return False
        return self.move(dx, dy)
