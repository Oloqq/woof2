from .agent import Agent
from .wolf_simulation import Simulation
import random

class Deer(Agent):
    kind: str = "deer"

    def __init__(self, simulation: Simulation, x: int, y: int):
        super().__init__(simulation, x, y)

    def step(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.move(dx, dy)
