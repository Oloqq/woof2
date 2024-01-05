from __future__ import annotations
from .params import Params
from .agent_group import AgentGroup
from .cell import Terrain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation
import random
from .wolf import Wolf
from .deer import Deer
from .deer_herd import Herd
from .path_finder import PathFinder

class Pack(AgentGroup):
    kind: str = "pack of wolves"
    nearest_herd: Herd = None
    path: list[tuple[int, int]] = []

    def __init__(self, sim: Simulation, x, y):
        super().__init__(sim, Params.wolves_pack_size, Params.wolves_pack_territory_length, x, y)

        self.path_finder = PathFinder(sim)
        self.wolves: list[Wolf] = []

        wolves_density = Params.wolves_pack_size / (Params.wolves_pack_territory_length ** 2)
        for i in range(self.xmin, self.xmax + 1):
            if(len(self.wolves)) >= Params.wolves_pack_size:
                break
            for j in range(self.ymin, self.ymax + 1):
                if(len(self.wolves)) >= Params.wolves_pack_size:
                    break
                if random.uniform(0,1) <= wolves_density + 0.1:
                    if not sim.grid[i][j].terrain == Terrain.Water:
                        self.wolves.append(Wolf(sim, i, j))


    def step(self):
        for wolf in self.wolves:
            wolf.endurance -= 5
            if wolf.endurance <= 0:
                self.kill_wolf(wolf)

        self.move_agents()

        for wolf in self.wolves:
            cell_content = self.sim.get_cell_content(wolf.x, wolf.y)
            if cell_content is not None and cell_content.kind == Deer.kind:
                self.sim.deathnote.append(cell_content)
                for wolf_eating in self.wolves:
                    wolf_eating.endurance = 1000
                self.nearest_herd = None
                break

    def kill_wolf(self, wolf: Wolf):
        if wolf in self.wolves:
            self.wolves.remove(wolf)
        if(len(self.wolves) == 0):
            self.sim.agent_groups[self.kind].remove(self)
            self.sim.groups_positions.append([self.x, self.y])

    def move_agents(self):
        if self.nearest_herd is None:
            self.nearest_herd = self.find_nearest_herd()
            self.path = self.path_finder.find_path((self.x, self.y), (self.nearest_herd.x, self.nearest_herd.y))
            if len(self.path) != 0:
                self.path.pop(0)

        if len(self.path) > 0:
            self.move(self.path[0][0] - self.x, self.path[0][1] - self.y)
            for wolf in self.wolves:
                path_to_follow = self.path_finder.find_path((wolf.x, wolf.y), (self.x, self.y))
                if len(path_to_follow) > 1:
                    wolf.step(path_to_follow[1][0] - wolf.x, path_to_follow[1][1] - wolf.y)
            self.path.pop(0)
        else:
            self.nearest_herd = None

    def find_nearest_herd(self) -> Herd:
        nearest_herd = None
        min_distance = float('inf')
        for herd in self.sim.agent_groups[Herd.kind]:
            distance = self.path_finder.calculate_distance((self.x, self.y), (herd.x, herd.y))
            if distance < min_distance:
                min_distance = distance
                nearest_herd = herd
        return nearest_herd
