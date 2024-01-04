from .agent import Agent
from .wolf import Wolf
from .deer import Deer
from .agent_group import AgentGroup
from .deer_herd import Herd
from .cell import Cell, Terrain
from .params import Params
import random
import noise

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
        # generate water using Perlin noise
        water_grid = self.generate_water(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                if water_grid[x][y] == 1:
                    self.grid[x][y].terrain = Terrain.Water

        self.reset()


    def generate_water(self, width, height):
            water_grid = [[0 for _ in range(height)] for _ in range(width)]
            scale = 10  # Adjust the scale to control the water pattern
            octaves = 1 # Adjust the number of octaves to control the level of detail
            persistence = 0.4  # Adjust the persistence to control the roughness
            threshold = 0.22  # Adjust the threshold to control the amount of water

            for x in range(width):
                for y in range(height):
                    nx = x / width * scale
                    ny = y / height * scale
                    noise_value = noise.pnoise2(nx, ny, octaves=octaves, persistence=persistence)
                    if noise_value > threshold:
                        water_grid[x][y] = 1

            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    if (
                        water_grid[x-1][y] == 1 and
                        water_grid[x+1][y] == 1 and
                        water_grid[x][y-1] == 1 and
                        water_grid[x][y+1] == 1
                    ):
                        water_grid[x][y] = 1
                    elif (
                        water_grid[x-1][y] == 0 and
                        water_grid[x+1][y] == 0 and
                        water_grid[x][y-1] == 0 and
                        water_grid[x][y+1] == 0
                    ):
                        water_grid[x][y] = 0

            return water_grid

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
        return [deer for herd in self.agent_groups[Herd.kind] for deer in herd.deers]
