from .agent import Agent
from .wolf import Wolf
from .deer import Deer
from .agent_group import AgentGroup
from .deer_herd import Herd
from .wolf_pack import Pack
from .cell import Cell, Terrain
from .params import Params
import random
import noise
import numpy as np

class Simulation:
    def __init__(self, world_size):
        self.width = world_size[0]
        self.height = world_size[1]
        self.agent_groups: dict[str, list[AgentGroup]] = {
            Herd.kind : [],
            Pack.kind : []
        }
        self.deathnote: list[Agent] = []

        self.init_map()

        self.reset()

    def init_map(self):
        self.grid: list[list[Cell]] = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

        # make the borders water
        for x in range(self.width):
            self.grid[x][0].terrain = Terrain.Water
            self.grid[x][self.height-1].terrain = Terrain.Water
        for y in range(self.height):
            self.grid[0][y].terrain = Terrain.Water
            self.grid[self.width-1][y].terrain = Terrain.Water

        # generate lakes
        water_grid = self.generate_lakes(self.width, self.height)

        def owner_of_tile(x, y) -> int:
            pack_centers = np.array(Params.pack_territory_centers)
            distances = np.sqrt(np.sum(np.power(pack_centers - np.array([x, y]), 2), axis = 1))
            owner_pack_id = np.argmin(distances)
            return owner_pack_id

        # apply lakes, init scent
        for x in range(self.width):
            for y in range(self.height):
                if water_grid[x][y] == 1:
                    self.grid[x][y].terrain = Terrain.Water
                self.grid[x][y].scent_pack = owner_of_tile(x, y)

    def generate_lakes(self, width, height):
            water_grid = [[0 for _ in range(height)] for _ in range(width)]
            scale = 6.9
            octaves = 3
            persistence = 0.1
            threshold = 0.25

            for x in range(width):
                for y in range(height):
                    nx = x / width * scale
                    ny = y / height * scale
                    noise_value = noise.pnoise2(nx, ny, octaves=octaves, persistence=persistence)
                    if noise_value > threshold:
                        water_grid[x][y] = 1

            return water_grid

    def reset(self):
        self.groups_positions = [
            [int(1 + Params.herd_territory_size * (i + 0.5)), int(1 + Params.herd_territory_size * (j + 0.5))]
            for i in range((self.width - 2) // Params.herd_territory_size)
            for j in range((self.height - 2) // Params.herd_territory_size)
        ]

        # generate wolves
        for _ in range(len(Params.pack_territory_centers)):
            pack_pos = random.choice(self.groups_positions)
            self.groups_positions.remove(pack_pos)
            # Check if the position is not water
            while self.grid[pack_pos[0]][pack_pos[1]].terrain == Terrain.Water:
                pack_pos = random.choice(self.groups_positions)
                self.groups_positions.remove(pack_pos)
            self.agent_groups[Pack.kind].extend([
                Pack(self, pack_pos[0], pack_pos[1]),
            ])

        for _ in range(Params.min_herd_num):
            herd_pos = random.choice(self.groups_positions)
            self.groups_positions.remove(herd_pos)
            # it can cause the simulation to crash when there is no more space for agents
            while(self.grid[herd_pos[0]][herd_pos[1]].terrain == Terrain.Water):
                herd_pos = random.choice(self.groups_positions)
                self.groups_positions.remove(herd_pos)
            self.agent_groups[Herd.kind].extend([
                Herd(self, herd_pos[0], herd_pos[1]),
                ])

    def step(self):
        for pack in self.agent_groups[Pack.kind]:
            pack.step()

        for herd in self.agent_groups[Herd.kind]:
            herd.step()

        for agent_to_kill in self.deathnote:
            for herd in self.agent_groups[Herd.kind]:
                herd.kill_deer(agent_to_kill)
        self.deathnote = []

        for _ in range(Params.min_herd_num - len(self.agent_groups[Herd.kind])):
            herd_pos = random.choice(self.groups_positions)
            self.groups_positions.remove(herd_pos)
            self.agent_groups[Herd.kind].extend([
                Herd(self, herd_pos[0], herd_pos[1]),
                ])

    def get_cell_content(self, x, y) -> Agent|None:
        for deer in self.get_deer():
            if deer.x == x and deer.y == y:
                    return deer
        for wolf in self.get_wolves():
            if wolf.x == x and wolf.y == y:
                    return wolf
        return None

    def get_deer(self) -> list[Deer]:
        return [deer for herd in self.agent_groups[Herd.kind] for deer in herd.deers]

    def get_wolves(self) -> list[Wolf]:
        return [wolf for pack in self.agent_groups[Pack.kind] for wolf in pack.wolves]
