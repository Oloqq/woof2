from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .wolf_simulation import Simulation
from .agent import Agent

class Wolf(Agent):
    kind: str = "wolf"

    def __init__(self, simulation: Simulation, x: int, y: int):
        super().__init__(simulation, x, y)
        self.speed = 1

    def step(self):
        from .deer import Deer
        if len(self.sim.agents[Deer.kind]) <= 0:
            print("no deer, wolf sad")
            return

        nearest_deer_i, nearest_deer = min(enumerate(self.sim.agents[Deer.kind]),
            key=lambda i_deer: abs(self.x - i_deer[1].x) + abs(self.y - i_deer[1].y),
            )
        dx = dy = 0
        if nearest_deer.x > self.x:
            dx = 1
        elif nearest_deer.x < self.x:
            dx = -1
        if nearest_deer.y > self.y:
            dy = 1
        elif nearest_deer.y < self.y:
            dy = -1

        # Proposed new position
        new_x = (self.x + dx * self.speed) % self.sim.width
        new_y = (self.y + dy * self.speed) % self.sim.height

        # Check if the new position is already occupied by another wolf
        cell_mate = self.sim.get_cell_content(new_x, new_y)
        if not cell_mate:
            self.move(dx * self.speed, dy * self.speed)
        elif cell_mate.kind == "deer":
            self.sim.deathnote.append(cell_mate)
            self.move(dx * self.speed, dy * self.speed)
