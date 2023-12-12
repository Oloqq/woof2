class Agent:
    kind: str = "abstract"

    def __init__(self, simulation, x: int, y: int):
        from .wolf_simulation import Simulation
        self.sim: Simulation = simulation
        self.x = x
        self.y = y

    def step(self):
        self.x += 1

    def move(self, dx, dy):
        self.x = (self.x + dx) % self.sim.width
        self.y = (self.y + dy) % self.sim.height
