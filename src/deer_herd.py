from __future__ import annotations
from .deer import Deer
from .params import Params
from .agent_group import AgentGroup
from .cell import Terrain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation
import random

class Herd(AgentGroup):
    kind: str = "herd of deer"

    def __init__(self, sim: Simulation, x, y):
        super().__init__(sim, Params.deer_herd_size, Params.deer_herd_territory_length, x, y)

        self.deers: list[Deer] = []

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

    def step(self):
        self.move_agents(self.random_move(), self.random_move())

    def move_agents(self, dx, dy):
        for deer in self.deers:
            if dx > 0 and deer.x <= self.xmin or dx < 0 and deer.x >= self.xmax:
                deer.move(dx, 0)
            else:
                deer.move(self.random_move(), 0)

            if dy > 0 and deer.y <= self.ymin or dy < 0 and deer.y >= self.ymax:
                deer.move(0, dy)
            else:
                deer.move(0, self.random_move())
        self.x = int(sum(deer.x for deer in self.deers) / len(self.deers))
        self.y = int(sum(deer.y for deer in self.deers) / len(self.deers))


    def kill_deer(self, deer: Deer):
        if deer in self.deers:
            self.deers.remove(deer)
        if len(self.deers) == 0:
            self.sim.agent_groups[self.kind].remove(self)
            self.sim.groups_positions.append([self.x, self.y])




