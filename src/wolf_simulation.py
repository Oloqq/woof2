from .agent import Agent
from .wolf import Wolf
from .deer import Deer
from .agent_group import AgentGroup
from .deer_herd import Herd
from .cell import Cell, Terrain
from .params import Params
import random

class Simulation:
    def __init__(self, world_size):
        self.width = world_size[0]
        self.height = world_size[1]
        pos = [
            [1 + Params.deer_herd_territory_length * (i + 0.5), 1 + Params.deer_herd_territory_length * (j + 0.5)]
            for i in range((world_size[0] - 2) // Params.deer_herd_territory_length)
            for j in range((world_size[1] - 2) // Params.deer_herd_territory_length)
        ]
        self.deer_herd_positions = [[int(p[0]), int(p[1])] for p in pos]
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
        for _ in range(Params.min_herd_num):
            herd_pos = random.choice(self.deer_herd_positions)
            self.deer_herd_positions.remove(herd_pos)
            self.agent_groups[Herd.kind].extend([
                Herd(self, herd_pos[0], herd_pos[1]),
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

        for _ in range(Params.min_herd_num - len(self.agent_groups[Herd.kind])):
            herd_pos = random.choice(self.deer_herd_positions)
            self.deer_herd_positions.remove(herd_pos)
            self.agent_groups[Herd.kind].extend([
                Herd(self, herd_pos[0], herd_pos[1]),
                ])

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
