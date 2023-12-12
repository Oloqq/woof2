from .agent import Agent

class Wolf(Agent):
    kind: str = "wolf"

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def step(self):
        pass
