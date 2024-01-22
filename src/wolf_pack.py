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
        self.safe_spot: tuple[int, int] = None

        wolves_density = Params.pack_size / (Params.pack_territory_length ** 2)

        safe_spots = []

        for i in range(self.xmin, self.xmax + 1):
            if (len(self.wolves)) >= Params.pack_size:
                break
            for j in range(self.ymin, self.ymax + 1):
                if (len(self.wolves)) >= Params.pack_size:
                    break
                if random.random() <= wolves_density + 0.1:
                    if i < len(sim.grid) and j < len(sim.grid[i]) and sim.grid[i][j].terrain != Terrain.Water:
                        self.wolves.append(Wolf(sim, i, j, self))
                        safe_spots.append((i, j))

        self.safe_spot = random.choice(safe_spots)

    def step(self):
        self.state = "chill"
        for wolf in self.wolves:
            wolf.endurance -= 5
            if wolf.endurance <= Params.wolf_hunger_threshold:
                self.state = "hunt"
            if wolf.endurance <= 0:
                self.kill_wolf(wolf)

        self.move_pack()

        # eat the deer if there is one
        for wolf in self.wolves:
            cell_content = self.sim.get_cell_content(wolf.x, wolf.y)
            if cell_content is not None and cell_content.kind == Deer.kind:
                if self.state == "hunt":
                    self.sim.deathnote.append(cell_content)
                    for wolf_eating in self.wolves:
                        wolf_eating.endurance = Params.wolf_max_endurance
                    self.nearest_herd = None
                    self.previous_herd = None
                    self.path = []
                break

    def kill_wolf(self, wolf: Wolf):
        if wolf in self.wolves:
            self.wolves.remove(wolf)
        if (len(self.wolves) == 0):
            self.sim.agent_groups[self.kind].remove(self)
            self.sim.groups_positions.append([self.x, self.y])

    def random_move(self):
        return random.choice([-1, 0, 1])

    def move_pack_randomly(self):
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

    def move_pack(self):
        if self.state == "chill":
            # print(f'pack {self.id} is chilling')
            if len(self.path) > 0:
                # print(f'pack {self.id} is moving to safe spot')
                self.move(self.path[0][0] - self.x, self.path[0][1] - self.y)
                self.path.pop(0)
                self.move_wolves()
                return
            # if they are on the edge of their territory - so multiple packs are not chilling next to each other on territory borders
            if self.path_finder.calculate_distance((self.x, self.y), self.safe_spot) > 50:
                self.path = self.path_finder.find_path((self.x, self.y), self.safe_spot)
            else:
                # print(f'pack {self.id} is close to the safe spot: {self.x, self.y}, {self.safe_spot}')
                self.move_pack_randomly()
            return

        # hunting
        if self.nearest_herd is None:
            # print(f'pack {self.id} is looking for a herd')
            self.nearest_herd = self.find_nearest_herd()
            if self.nearest_herd:
                # print(f'pack {self.id} found a herd')
                self.path = self.path_finder.find_path((self.x, self.y), (self.nearest_herd.x, self.nearest_herd.y))
            elif self.previous_herd and any(wolf.endurance < 2000 for wolf in self.wolves):
                # print(f'pack {self.id} is going back to the previous herd')
                # no nearest herd, but there is a previous herd and wolves are hungry, so switch back to it
                self.nearest_herd = self.previous_herd
                self.path = self.path_finder.find_path((self.x, self.y), (self.previous_herd.x, self.previous_herd.y))
            else:
                # print(f'no deer to hunt on, pack {self.id} is going back to the safe spot')
                self.path = self.path_finder.find_path((self.x, self.y), self.safe_spot)
                self.move(self.path[0][0] - self.x, self.path[0][1] - self.y)
                self.move_wolves()
                return

        # we have a path to nearest herd
        if len(self.path) > 0:
            # print(f'pack {self.id} is moving to the herd')
            distance = self.path_finder.calculate_distance((self.x, self.y), (self.nearest_herd.x, self.nearest_herd.y))
            steps = Params.sprint_speed if distance <= Params.sprint_distance else 1
            # when distance less than 25, move by Params.sprint_speed instead of 1
            for _ in range(steps):
                if len(self.path) == 0:
                    break

                self.move(self.path[0][0] - self.x, self.path[0][1] - self.y)

                # adding this so the wolves are not following the wrong previous path to deers
                if self.nearest_herd and self.path_finder.calculate_distance((self.x, self.y), (self.nearest_herd.x, self.nearest_herd.y)) > distance:
                #     # print(f'recalculating the path in next step')
                    self.nearest_herd = None

                # # check if the wolves are on their territory - if not check if another pack is following the prey - if there is one, the pack should give up on hunting
                # if self.sim.grid[self.x][self.y].scent_pack != self.id and len([pack for pack in self.sim.agent_groups[self.kind] if pack.nearest_herd == self.nearest_herd]) > 1:
                # #     # print(f'pack {self.id} is giving up on hunting, another herd is hunting the same prey')
                #     self.nearest_herd = None
                #     self.previous_herd = None
                #     break

                self.path.pop(0)
                self.move_wolves()
        else:
            self.move_pack_randomly()
            self.previous_herd = self.nearest_herd
            self.nearest_herd = None


    def move_wolves(self):
        for wolf in self.wolves:
            path_to_follow = self.path_finder.find_path((wolf.x, wolf.y), (self.x, self.y))
            if len(path_to_follow) > 1:
                wolf.step(path_to_follow[1][0] - wolf.x, path_to_follow[1][1] - wolf.y)
                if random.random() < 0.5:
                    wolf.step(self.random_move(), self.random_move())

    def find_nearest_herd(self) -> Herd:
        nearest_herd = None
        min_distance = float('inf')
        for herd in self.sim.agent_groups[Herd.kind]:
            # check if herd in the same territory - if not wolves will attack only if they are really hungry
            herd_territory = self.sim.grid[herd.x][herd.y].scent_pack
            if herd_territory != self.id and not any(wolf.endurance < 2000 for wolf in self.wolves):
                continue

            distance = self.path_finder.calculate_distance((self.x, self.y), (herd.x, herd.y))
            if distance < min_distance:
                min_distance = distance
                nearest_herd = herd
        return nearest_herd
