from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation

from .agent import Agent
import random

class Deer(Agent):
    kind: str = "deer"

    def __init__(self, simulation: Simulation, x: int, y: int):
        super().__init__(simulation, x, y)

    def step(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.move(dx, dy)
