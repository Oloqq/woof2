from __future__ import annotations
from .deer import Deer
from .params import Params
from .agent_group import AgentGroup
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation
import random

class Herd(AgentGroup):
    kind: str = "herd of deer"

    def __init__(self, sim: Simulation, x, y):
        super().__init__(sim, Params.deer_herd_size, Params.deer_herd_territory_length, x, y)

        self.deers: list[Deer] = []

        for _ in range(Params.deer_herd_size):
            deer_x = int(round(random.uniform(self.xmin, self.xmax)))
            deer_y = int(round(random.uniform(self.ymin, self.ymax)))

            while any(deer.x == x and deer.y == y for deer in self.deers):
                deer_x = int(round(random.uniform(self.xmin, self.xmax)))
                deer_y = int(round(random.uniform(self.ymin, self.ymax)))

            self.deers.append(Deer(sim, deer_x, deer_y))

    def random_move(self):
        return random.choice([-1, 0, 1])

    def step(self):
        self.move(self.random_move(), self.random_move())

    def move(self, dx, dy):
        for deer in self.deers:
            if dx > 0 and deer.x <= self.xmin or dx < 0 and deer.x >= self.xmax:
                deer.move(dx, 0)
            else:
                deer.move(self.random_move(), 0)

            if dy > 0 and deer.y <= self.ymin or dy < 0 and deer.y >= self.ymax:
                deer.move(0, dy)
            else:
                deer.move(0, self.random_move())

    def kill_deer(self, deer: Deer):
        if deer in self.deers:
            self.deers.remove(deer)




