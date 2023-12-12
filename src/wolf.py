from .agent import Agent
from .wolf_simulation import Simulation

class Wolf(Agent):
    kind: str = "wolf"

    def __init__(self, simulation: Simulation, x: int, y: int):
        super().__init__(simulation, x, y)
        self.speed = 1

    def step(self):
        deer_positions = [
            (agent.x, agent.y) for agent in self.sim.agents if agent.kind == "deer"
        ]
        if not deer_positions:
            print("no deer, wolf sad")
            return

        nearest_deer_pos = min(deer_positions,
            key=lambda deerpos: abs(self.x - deerpos[0]) + abs(self.y - deerpos[1]),
        )
        dx = dy = 0
        if nearest_deer_pos[0] > self.x:
            dx = 1
        elif nearest_deer_pos[0] < self.x:
            dx = -1
        if nearest_deer_pos[1] > self.y:
            dy = 1
        elif nearest_deer_pos[1] < self.y:
            dy = -1

        self.move(dx * self.speed, dy * self.speed)

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
