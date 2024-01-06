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

pack_id = 0


class Pack(AgentGroup):
    kind: str = "pack of wolves"

    def __init__(self, sim: Simulation, x, y):
        super().__init__(sim, Params.pack_size, Params.pack_territory_length, x, y)

        global pack_id
        self.id = pack_id
        pack_id += 1

        self.path_finder = PathFinder(sim)
        self.wolves: list[Wolf] = []
        self.nearest_herd: Herd = None
        self.previous_herd: Herd = None
        self.path: list[tuple[int, int]] = []
        self.state: str = "chill"

        wolves_density = Params.pack_size / (Params.pack_territory_length ** 2)
        for i in range(self.xmin, self.xmax + 1):
            if (len(self.wolves)) >= Params.pack_size:
                break
            for j in range(self.ymin, self.ymax + 1):
                if (len(self.wolves)) >= Params.pack_size:
                    break
                if random.random() <= wolves_density + 0.1:
                    if not sim.grid[i][j].terrain == Terrain.Water:
                        self.wolves.append(Wolf(sim, i, j, self))

    def step(self):
        self.state = "chill"
        for wolf in self.wolves:
            wolf.endurance -= 5
            if wolf.endurance <= Params.wolf_hunger_threshold:
                self.state = "hunt"
            elif wolf.endurance <= 0:
                self.kill_wolf(wolf)

        self.move_agents()

        for wolf in self.wolves:
            cell_content = self.sim.get_cell_content(wolf.x, wolf.y)
            if cell_content is not None and cell_content.kind == Deer.kind:
                if self.state == "hunt":
                    self.sim.deathnote.append(cell_content)
                for wolf_eating in self.wolves:
                    wolf_eating.endurance = Params.wolf_max_endurance
                self.nearest_herd = None
                break

    def kill_wolf(self, wolf: Wolf):
        if wolf in self.wolves:
            self.wolves.remove(wolf)
        if (len(self.wolves) == 0):
            self.sim.agent_groups[self.kind].remove(self)
            self.sim.groups_positions.append([self.x, self.y])

    def random_move(self):
        return random.choice([-1, 0, 1])

    def move_agents_randomly(self):
        for wolf in self.wolves:
            if wolf.x < self.xmin:
                wolf.step(1, 0)
            elif wolf.x > self.xmax:
                wolf.step(-1, 0)
            else:
                wolf.step(self.random_move(), 0)

            if wolf.y < self.ymin:
                wolf.step(0, 1)
            elif wolf.y > self.ymax:
                wolf.step(0, -1)
            else:
                wolf.step(0, self.random_move())

    def move_agents(self):
        if (self.state == "chill"):
            self.previous_herd = None
            self.move_agents_randomly()
            return

        if self.nearest_herd is None:
            self.nearest_herd = self.find_nearest_herd()
            if self.nearest_herd:
                self.path = self.path_finder.find_path((self.x, self.y), (self.nearest_herd.x, self.nearest_herd.y))
            elif self.previous_herd:
                # no nearest herd, but there is a previous herd, so switch back to it
                self.nearest_herd = self.previous_herd
                self.path = self.path_finder.find_path((self.x, self.y), (self.previous_herd.x, self.previous_herd.y))
            if len(self.path) != 0:
                self.path.pop(0)

        if len(self.path) > 0:

            distance = self.path_finder.calculate_distance((self.x, self.y), (self.nearest_herd.x, self.nearest_herd.y))
            steps = Params.sprint_speed if distance <= 25 else 1
            # when distance less than 25, move by Params.sprint_speed instead of 1
            for _ in range(steps):
                if len(self.path) == 0:
                    break

                self.move(self.path[0][0] - self.x, self.path[0][1] - self.y)
                for wolf in self.wolves:
                    path_to_follow = self.path_finder.find_path((wolf.x, wolf.y), (self.x, self.y))
                    if len(path_to_follow) > 1:
                        # TODO if wolf does not move, we may need to find a path for him
                        wolf.step(path_to_follow[1][0] - wolf.x, path_to_follow[1][1] - wolf.y)
                        if random.random() < 0.5:
                            wolf.step(self.random_move(), self.random_move())
                self.path.pop(0)
        else:
            # TODO: find new path for wolves
            self.move_agents_randomly()
            self.previous_herd = self.nearest_herd
            self.nearest_herd = None

    def find_nearest_herd(self) -> Herd:
        nearest_herd = None
        min_distance = float('inf')
        for herd in self.sim.agent_groups[Herd.kind]:
            # check if herd in the same territory
            herd_territory = self.sim.grid[herd.x][herd.y].scent_pack
            if herd_territory != self.id:
                continue

            distance = self.path_finder.calculate_distance((self.x, self.y), (herd.x, herd.y))
            if distance < min_distance:
                min_distance = distance
                nearest_herd = herd
        return nearest_herd
