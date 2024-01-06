from queue import PriorityQueue
from .cell import Terrain

class PathFinder:
    def __init__(self, sim):
        self.sim = sim

    def find_path(self, start, goal) -> list[tuple[int, int]]:
        # Define a priority queue to store the nodes to be explored
        open_set = PriorityQueue()
        open_set.put((0, start))

        # Define a dictionary to store the parent node of each visited node
        parent = {}
        parent[start] = None

        # Define a dictionary to store the cost of reaching each node from the start node
        g_score = {}
        g_score[start] = 0

        # Define a dictionary to store the estimated total cost of reaching the goal node from each node
        f_score = {}
        f_score[start] = self.calculate_distance(start, goal)

        while not open_set.empty():
            current = open_set.get()[1]

            if current == goal:
                # Reconstruct the path from the goal node to the start node
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path

            neighbors = self.get_neighbors(current[0], current[1])
            for neighbor in neighbors:
                neighbor_cost = g_score[current] + 1  # Assuming each step has a cost of 1

                if neighbor not in g_score or neighbor_cost < g_score[neighbor]:
                    g_score[neighbor] = neighbor_cost
                    f_score[neighbor] = neighbor_cost + self.calculate_distance(neighbor, goal)
                    parent[neighbor] = current
                    open_set.put((f_score[neighbor], neighbor))

        return []  # No path found

    def get_neighbors(self, x, y) -> list[tuple[int, int]]:
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Possible movement directions (right, left, up, down)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny):
                neighbors.append((nx, ny))

        return neighbors

    def is_valid_position(self, x, y) -> bool:
        if self.sim.grid[x][y].terrain == Terrain.Water:
            return False
        return True

    def calculate_distance(self, start, goal) -> float:
        return ((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2) ** 0.5