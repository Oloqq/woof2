class Agent:
    kind: str = "abstract"

    def __init__(self, simulation, x: int, y: int):
        from .wolf_simulation import Simulation
        self.sim: Simulation = simulation
        self.x = x
        self.y = y

    def step(self):
        self.x += 1
