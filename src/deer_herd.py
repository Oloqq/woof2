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
    path: list[tuple[int, int]] = []

    def __init__(self, sim: Simulation, x, y):
        super().__init__(sim, Params.herd_size, Params.herd_territory_size, x, y)
        self.deers: list[Deer] = []
        self.path_finder = PathFinder(sim)
        self.state = "chill"
        deer_density = Params.herd_size / (Params.herd_territory_size ** 2)
        for i in range(self.xmin, self.xmax + 1):
            if(len(self.deers)) >= Params.herd_size + 5:
                break
            for j in range(self.ymin, self.ymax + 1):
                if(len(self.deers)) >= Params.herd_size + 5:
                    break
                if random.random() <= deer_density + 0.1:
                    if not sim.grid[i][j].terrain == Terrain.Water:
                        self.deers.append(Deer(sim, i, j))


    def random_move(self):
        return random.choice([-1, 0, 1])

    def find_max_distance_cell(self, pack) -> tuple[int, int]:
        max_distance = 0
        max_distance_cell = None
        for i in range(max(1, self.xmin), min(self.xmax + 1, self.sim.width - 1)):
            for j in range(max(1, self.ymin), min(self.ymax + 1, self.sim.height - 1)):
                distance = self.path_finder.calculate_distance((i, j), (pack.x, pack.y))
                if self.sim.grid[i][j].terrain != Terrain.Water and distance > max_distance:
                    max_distance = distance
                    max_distance_cell = (i, j)
        return max_distance_cell

    def step(self):
        nearest_pack, distance = self.calculate_distance_to_wolves()
        if distance < Params.deer_max_tolerated_distance_from_wolves:
            self.state = "run"
        else:
            self.state = "chill"

        self.move_agents(nearest_pack)

    def move_agents(self, pack):
        if(self.state == "chill"):
            for deer in self.deers:
                if deer.x < self.xmin:
                    deer.step(1, 0)
                elif deer.x > self.xmax:
                    deer.step(-1, 0)
                else:
                    deer.step(self.random_move(), 0)

                if deer.y < self.ymin:
                    deer.step(0, 1)
                elif deer.y > self.ymax:
                    deer.step(0, -1)
                else:
                    deer.step(0, self.random_move())

            x = int(sum(deer.x for deer in self.deers) / len(self.deers))
            y = int(sum(deer.y for deer in self.deers) / len(self.deers))

            self.move(x - self.x, y - self.y)

        else:
            if len(self.path) == 0:
                dx = -1 if pack.x - self.x > 0 else 1 if pack.x - self.x < 0 else 0
                dy = -1 if pack.y - self.y > 0 else 1 if pack.y - self.y < 0 else 0
                herd_moved = self.move(dx, dy)
                if not herd_moved:
                    max_distance_cell = self.find_max_distance_cell(pack)
                    self.path = self.path_finder.find_path((self.x, self.y), max_distance_cell)
                    if len(self.path) > 1:
                        self.path.pop(0)
                        self.move(self.path[0][0] - self.x, self.path[0][1] - self.y)
            else:
                self.move(self.path[0][0] - self.x, self.path[0][1] - self.y)
                dx = self.path[0][0] - self.x
                dy = self.path[0][1] - self.y
                self.path.pop(0)

            for deer in self.deers:
                deer_moved = deer.step(dx, dy)
                deer.step(self.random_move(), self.random_move())
                if not deer_moved:
                    path_to_follow = self.path_finder.find_path((deer.x, deer.y), (self.x, self.y))
                    if path_to_follow is not None and len(path_to_follow) > 0:
                        path_to_follow.pop(0)
                        deer.path = path_to_follow


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




