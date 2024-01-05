from __future__ import annotations
from .deer import Deer
from .params import Params
from .path_finder import PathFinder
from .agent_group import AgentGroup
from .cell import Terrain, Cell
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation
import random

class Herd(AgentGroup):
    kind: str = "herd of deer"

    def __init__(self, sim: Simulation, x, y):
        super().__init__(sim, Params.deer_herd_size, Params.deer_herd_territory_length, x, y)
        self.deers: list[Deer] = []
        self.path_finder = PathFinder(sim)
        self.state = "chill"
        deer_density = Params.deer_herd_size / (Params.deer_herd_territory_length ** 2)
        for i in range(self.xmin, self.xmax + 1):
            if(len(self.deers)) >= Params.deer_herd_size + 5:
                break
            for j in range(self.ymin, self.ymax + 1):
                if(len(self.deers)) >= Params.deer_herd_size + 5:
                    break
                if random.uniform(0,1) <= deer_density + 0.1:
                    if not sim.grid[i][j].terrain == Terrain.Water:
                        self.deers.append(Deer(sim, i, j))


    def random_move(self):
        return random.choice([-1, 0, 1])

    def find_max_distance_cell(self, pack) -> tuple[int, int]:
        max_distance = 0
        max_distance_cell = None
        for i in range(self.xmin,self.xmax+1):
            for j in range(self.ymin,self.ymax+1):
                distance = self.path_finder.calculate_distance((i, j), (pack.x, pack.y))
                if self.sim.grid[i][j].terrain != Terrain.Water and distance > max_distance:
                    max_distance = distance
                    max_distance_cell = (i, j)
        return max_distance_cell

    def step(self):
        nearest_pack, distance = self.calculate_distance_to_wolves()
        if distance < Params.deer_herd_safety_distance:
            self.state = "run"
            direction = self.find_max_distance_cell(nearest_pack)
            if direction is not None:
                path = self.path_finder.find_path((self.x, self.y), direction)
                if path is not None and len(path) > 1:
                    self.move_agents(path[1][0] - self.x, path[1][1] - self.y)
        else:
            self.state = "chill"
            self.move_agents(self.random_move(), self.random_move())

    def move_agents(self, dx, dy):
        for deer in self.deers:
            if dx > 0 and deer.x <= self.xmin or dx < 0 and deer.x >= self.xmax:
                deer.step(dx, 0)
            else:
                deer.step(self.random_move(), 0)

            if dy > 0 and deer.y <= self.ymin or dy < 0 and deer.y >= self.ymax:
                deer.step(0, dy)
            else:
                deer.step(0, self.random_move())

        if self.state == "chill":
            dx = -1 if self.x - int(sum(deer.x for deer in self.deers) / len(self.deers)) > 0 else 1 if self.x - int(sum(deer.x for deer in self.deers) / len(self.deers)) < 0 else 0
            dy = -1 if self.y - int(sum(deer.y for deer in self.deers) / len(self.deers)) > 0 else 1 if self.y - int(sum(deer.y for deer in self.deers) / len(self.deers)) < 0 else 0
            self.move(dx, dy)
        else:
            self.move(dx, dy)


    def kill_deer(self, deer: Deer):
        if deer in self.deers:
            self.deers.remove(deer)
        if len(self.deers) == 0:
            self.sim.agent_groups[self.kind].remove(self)
            self.sim.groups_positions.append([self.x, self.y])

    def calculate_distance_to_wolves(self):
        nearest_pack = None
        min_distance = float('inf')
        for pack in self.sim.agent_groups["pack of wolves"]:
            distance = self.path_finder.calculate_distance((self.x, self.y), (pack.x, pack.y))
            if distance < min_distance:
                min_distance = distance
                nearest_pack = pack
        return nearest_pack, min_distance




