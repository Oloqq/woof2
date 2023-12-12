from .agent import Agent

class Simulation:
    def __init__(self, world_size):
        self.width = world_size[0]
        self.height = world_size[1]
        self.agents: list[Agent] = []
        self.scent = [[0 for _ in range(self.height)] for _ in range(self.width)]

    def step(self):
        for agent in self.agents:
            agent.step()