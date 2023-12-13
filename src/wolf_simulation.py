from .agent import Agent
from .wolf import Wolf
from .deer import Deer
from .cell import Cell, Terrain
from .params import Params

class Simulation:
    def __init__(self, world_size):
        self.width = world_size[0]
        self.height = world_size[1]
        self.agents: dict[str, list[Agent]] = {
            Deer.kind: [],
            Wolf.kind: [],
        }
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
        self.agents[Deer.kind].extend([
            Deer(self, 1, 1),
            Deer(self, 8, 8),
            Deer(self, 1, 2),
            ])
        self.agents[Wolf.kind].extend([
            Wolf(self, 10, 1),
            ])

    def step(self):
        assert self.agents.keys() == set([Wolf.kind, Deer.kind])

        for deer in self.agents[Deer.kind]:
            deer.step()

        for wolf in self.agents[Wolf.kind]:
            wolf.step()

        for agent_to_kill in self.deathnote:
            self.agents[agent_to_kill.kind].remove(agent_to_kill)
        self.deathnote = []

    def get_cell_content(self, x, y) -> Agent|None:
        for _, agents in self.agents.items():
            for agent in agents:
                if agent.x == x and agent.y == y:
                    return agent
        return None