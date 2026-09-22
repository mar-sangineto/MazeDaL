# ****************************************************************************
#
#    a_maze_ing.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Main entry point for the A-Maze-ing project, responsible
#                 for parsing configuration files, generating the maze,
#                 solving the shortest path, saving the output file and
#                 launching the interactive terminal interface.
#
#    Created: 2026/04/22
#
# ****************************************************************************

import sys

from exceptions import ConfigError, MazeError
from maze_generator import MazeGenerator
from maze_structure import Maze
from menu import MazeMenu
from parser import Parser
from solver import MazeSolver


def main() -> None:
    """
    Run the maze generation program.

    Parses the configuration file, generates
    the maze, solves the shortest path and
    launches the interactive terminal menu.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config_path = sys.argv[1]
        config = Parser(config_path)

        maze = Maze(config)

        gen = MazeGenerator(maze, config)
        gen.generate()

        solver = MazeSolver(maze, config)
        solver.solve()
        solution = solver.path_to_directions()
        gen.save_maze(maze, config, solution)

        MazeMenu(maze, gen, config).run()

    except ConfigError as e:
        print(f"Config error: {e}")

    except MazeError as e:
        print(f"Maze error: {e}")

    except KeyboardInterrupt:
        print("\nQue a força esteja sempre com você!")

    except Exception as e:
        print(f"Error found: {e}")


if __name__ == "__main__":
    main()
