class Agent:
    kind: str = "abstract"

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def step(self):
        self.x += 1
