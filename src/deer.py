from .agent import Agent

class Deer(Agent):
    kind: str = "deer"

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def step(self):
        pass
