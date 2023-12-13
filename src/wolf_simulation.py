from .agent import Agent
from enum import Enum, auto

class Terrain(Enum):
    Grass = auto(),
    Water = auto()

class Cell:
    def __init__(self):
        self.scent = 0
        self.terrain = Terrain.Grass

class Simulation:
    def __init__(self, world_size):
        self.width = world_size[0]
        self.height = world_size[1]
        self.agents: list[Agent] = []
        self.deathnote: list[Agent] = []
        self.grid: list[list[Cell]] = [[Cell() for _ in range(self.height)] for _ in range(self.width)]
        for x in range(self.width):
            self.grid[x][0].terrain = Terrain.Water
            self.grid[x][self.height-1].terrain = Terrain.Water
        for y in range(self.height):
            self.grid[0][y].terrain = Terrain.Water
            self.grid[self.width-1][y].terrain = Terrain.Water
        self.reset()

    def reset(self):
        # local imports to avoid circular depenedncy
        from .wolf import Wolf
        from .deer import Deer

        self.agents.extend([
            # Agent(self, 0, 0),
            Wolf(self, 10, 0),
            Deer(self, 0, 0),
            Deer(self, 9, 9),
            Deer(self, 0, 2),
            ])

    def step(self):
        for agent in self.agents:
            agent.step()
        for agent_to_kill in self.deathnote:
            self.agents.remove(agent_to_kill)
        self.deathnote = []

    def get_cell_content(self, x, y) -> Agent|None:
        for agent in self.agents:
            if agent.x == x and agent.y == y:
                return agent
        return None