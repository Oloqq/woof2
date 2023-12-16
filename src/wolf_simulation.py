from .agent import Agent
from .wolf import Wolf
from .deer import Deer
from .agent_group import AgentGroup
from .deer_herd import Herd
from .cell import Cell, Terrain
from .params import Params

class Simulation:
    def __init__(self, world_size):
        self.width = world_size[0]
        self.height = world_size[1]
        self.agents: dict[str, list[Agent]] = {
            Wolf.kind: []
        }
        self.agent_groups: dict[str, list[AgentGroup]] = {
            Herd.kind : []
        }
        self.deathnote: list[Agent] = []
        self.grid: list[list[Cell]] = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

        # make the borders water
        for x in range(self.width):
            self.grid[x][0].terrain = Terrain.Water
            self.grid[x][self.height-1].terrain = Terrain.Water
        for y in range(self.height):
            self.grid[0][y].terrain = Terrain.Water
            self.grid[self.width-1][y].terrain = Terrain.Water
        # create a pattern with water to track camera movement
        for x in range(0, self.width, 10):
            for y in range(0, self.height, 10):
                self.grid[x][y].terrain = Terrain.Water
        self.reset()

    def reset(self):
        self.agent_groups[Herd.kind].extend([
            Herd(self, 10, 10),
            # Herd(self, 40, 20)
            ])
        self.agents[Wolf.kind].extend([
            Wolf(self, 25, 15),
            Wolf(self, 25, 10),
            Wolf(self, 25, 20),
            ])

    def step(self):
        for herd in self.agent_groups[Herd.kind]:
            herd.step()

        for wolf in self.agents[Wolf.kind]:
            wolf.step()

        for agent_to_kill in self.deathnote:
            for herd in self.agent_groups[Herd.kind]:
                herd.kill_deer(agent_to_kill)
        self.deathnote = []

        # if len(self.agents[Deer.kind]) < Params.keep_deer_alive:
        #     for _ in range(Params.deer_herd_size):
        #         x = random.randint(1, self.width)
        #         y = random.randint(1, self.height)
        #         self.agents[Deer.kind].append(Deer(self, x, y))

    def get_cell_content(self, x, y) -> Agent|None:
        for _, agents in self.agents.items():
            for agent in agents:
                if agent.x == x and agent.y == y:
                    return agent
        for deer in self.get_deers():
            if deer.x == x and deer.y == y:
                    return deer
        return None

    def get_deers(self) -> list[Deer]:
        return [deer for horde in self.agent_groups[Herd.kind] for deer in horde.deers]
