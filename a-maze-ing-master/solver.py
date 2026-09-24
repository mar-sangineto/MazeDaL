# ****************************************************************************
#
#    solver.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Breadth-First Search shortest-path solver responsible
#                 for traversing reachable maze cells, reconstructing the
#                 optimal path, exporting movement directions and gathering
#                 solving performance statistics.
#
#    Created: 2026/05/19
#
# ****************************************************************************

from collections import deque
import time

from maze_structure import Maze
from parser import Parser


class MazeSolver:
    """Breadth-First or Depth-First Search maze solver."""

    def __init__(self, maze: Maze, config: Parser) -> None:
        """
        Initialize maze solver.

        Args:
            maze: Maze structure.
            config: Maze configuration parser.
        """
        assert config.entry is not None
        assert config.exit is not None

        self.maze = maze
        self.entry = config.entry
        self.exit = config.exit
        self.algorithm = config.algorithm

        self.path: (
            list[tuple[int, int]] | None
        ) = None

    def _reconstruct_path(
        self,
        parents: dict[
            tuple[int, int],
            tuple[int, int] | None,
        ],
    ) -> list[tuple[int, int]]:
        """
        Reconstruct shortest path.

        Traverses parent relationships from
        exit to entry coordinates.

        Args:
            parents: BFS parent mapping.

        Returns:
            Ordered shortest path coordinates.
        """
        path = []
        current: tuple[int, int] | None = self.exit

        while current is not None:
            path.append(current)

            current = parents[current]

        path.reverse()

        return path

    def path_to_directions(
        self,
    ) -> str:
        """
        Convert coordinate path into directions.

        Returns:
            NESW movement direction string.
        """
        if self.path is None:
            return ""

        directions = []

        for i in range(len(self.path) - 1):

            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]

            if x2 == x1 + 1:
                directions.append("E")

            elif x2 == x1 - 1:
                directions.append("W")

            elif y2 == y1 + 1:
                directions.append("S")

            elif y2 == y1 - 1:
                directions.append("N")

        return "".join(directions)

    def solve(self) -> list[tuple[int, int]]:
        """
        Solve maze using Breadth-First Search.

        Explores reachable cells level by
        level to compute the shortest path
        between entry and exit.

        Returns:
            Shortest valid maze path.
        """
        self.visited_nodes = 0
        self.solve_time = 0.0
        queue = deque([self.entry])
        visited = {self.entry}
        parents: dict[tuple[int, int], tuple[int, int] | None] = {
            self.entry: None
        }
        start = time.perf_counter()
        while queue:
            current = queue.pop() if self.algorithm == "DFS" else queue.popleft()
            self.visited_nodes += 1

            if current == self.exit:
                self.path = self._reconstruct_path(parents)
                self.solve_time = time.perf_counter() - start
                return self.path

            x, y = current
            neighbors = self.maze.reachable_neighbors(x, y)

            for neighbor in neighbors:

                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = current
                    queue.append(neighbor)
        self.path = []
        self.solve_time = time.perf_counter() - start
        return self.path
