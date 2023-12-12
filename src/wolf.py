from .agent import Agent
from .wolf_simulation import Simulation

class Wolf(Agent):
    kind: str = "wolf"

    def __init__(self, simulation: Simulation, x: int, y: int):
        super().__init__(simulation, x, y)

    def step(self):
        pass
