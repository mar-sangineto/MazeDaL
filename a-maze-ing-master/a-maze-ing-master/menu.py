# ****************************************************************************
#
#    menu.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Interactive terminal menu for maze visualization and
#                 user interactions.
#
#    Created: 2026/05/19
#
# ****************************************************************************

import os
import time

import themes

from maze_generator import MazeGenerator
from maze_structure import Maze
from parser import Parser
from renderer import MazeRenderer
from solver import MazeSolver
from audio_manager import AudioManager


class MazeMenu:
    """Interactive maze terminal menu."""

    THEME_MUSIC: dict[str, str] = {
        "1": " ",
        "2": " ",
        "3": " ",
        "4": "songs/one_piece_overtaken.mp3",
        "5": "songs/wano_kuni.mp3",
        "6": "songs/binks_sake.mp3",
        "7": "songs/terror.mp3",
    }

    def __init__(
        self,
        maze: Maze,
        generator: MazeGenerator,
        config: Parser,
    ) -> None:
        """
        Initialize interactive maze menu.

        Args:
            maze: Maze structure.
            generator: Maze generator instance.
            config: Maze configuration parser.
        """
        self.maze = maze
        self.generator = generator
        self.config = config

        self.show_path = False

        self.path: (list[tuple[int, int]] | None) = None

        self.current_theme = themes.DEFAULT_THEME
        self.current_theme_name = "Default"
        self.audio = AudioManager()
        self.renderer = MazeRenderer(
            self.maze,
            self.config,
            self.path,
            self.current_theme,
        )

        self.path = MazeSolver(self.maze, self.config).solve()
        self.save = True

    def _clear_screen(self) -> None:
        """Clear terminal screen."""
        os.system("clear")

    def _render(self) -> None:
        """
        Render maze using current state.

        Updates renderer attributes before
        displaying the maze.
        """
        self.renderer.maze = self.maze

        if self.show_path:
            self.renderer.path = self.path

        else:
            self.renderer.path = None

        self.renderer.theme = self.current_theme
        self.renderer.render()

    def _show_menu(self) -> None:
        """
        Display available menu options.

        Shows interactive actions and current
        visualization state.
        """
        print()

        print(f"{'═'*15} Menu {'═'*15}")
        print("[1] Regenerate maze")
        if not self.show_path:
            print("[2] Toggle shortest path (Disabled)")
        else:
            print("[2] Toggle shortest path (Enabled)")
        print(f"[3] Change theme ({self.current_theme_name})")
        if self.save:
            print(f"[4] Save maze (saved to `{self.config.output_file}`)")
        else:
            print("[4] Save maze (not saved)")
        print("[5] Animate solution")
        print("[6] Show stats")
        print("[0] Exit")
        print(f"{'═'*36}")

        print()

    def _show_title(self) -> None:
        """
        Show project title and maze status.

        Displays ASCII banner and warns when
        the 42 pattern is unavailable.
        """
        print(
            "\033[1m"
            "\033[38;5;220m"
            r"""
             █████╗       ███╗   ███╗ █████╗ ███████╗███████╗
            ██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝
            ███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗
            ██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝
            ██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗
            ╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝
                """
            "\033[0m"
            )

        if not self.generator.has_42_pattern:
            print("42 pattern was not generated.\n")

    def _regenerate(self) -> None:
        """
        Generate and solve a new maze.

        Resets current visualization state and
        updates the stored solution path.
        """
        self.maze = Maze(self.config)
        self.generator = MazeGenerator(self.maze, self.config)
        self.generator.generate()
        solver = MazeSolver(self.maze, self.config)
        self.path = solver.solve()
        self.save = False

    def _toggle_path(self) -> None:
        """Show or hide shortest path."""
        self.show_path = not self.show_path

    def _change_theme(self) -> None:
        """
        Change active renderer theme.

        Updates maze colors and associated
        background music.
        """
        print(f"\n{'═'*9} Choose a Theme: {'═'*10}")
        for key, (name, _) in themes.THEMES.items():
            print(f"[{key}] {name}")

        choice = input("\nTheme: ").strip()

        if choice in themes.THEMES:
            name, theme = themes.THEMES[choice]
            self.current_theme = theme
            self.current_theme_name = name

            if choice in self.THEME_MUSIC:
                self.audio.play(self.THEME_MUSIC[choice])
            else:
                self.audio.stop()

        else:
            print("\nSelect a valid menu option (1-7).\n")
            self._pause()

    def _save_maze(self) -> None:
        """
        Save maze to output file.

        Exports hexadecimal maze encoding and
        shortest solution path.
        """
        try:
            new_file = input(
                f"Enter the name of the file to save"
                f" ({self.config.output_file}): "
                )
            if new_file:
                self.config.output_file = new_file
            solver = MazeSolver(self.maze, self.config)
            solver.solve()
            solution = solver.path_to_directions()
            self.generator.save_maze(self.maze, self.config, solution)
            self.save = True

        except Exception:
            print("\nFailed to save maze.\n")
            self.save = False
            self._pause()

    def _show_stats(self) -> None:
        """Display maze generation statistics."""
        solver = MazeSolver(self.maze, self.config)
        path = solver.solve()

        print(f"\n{'═'*15} Stats {'═'*14}\n")

        print(f"Algorithm: {self.config.algorithm}")
        print(f"Maze Size: {self.maze.width} x {self.maze.height}")
        print(f"Perfect Maze: {self.config.perfect}")
        print(f"Visited Nodes: {solver.visited_nodes}")
        print(f"Path Length: {len(path)}")
        print(f"Solve Time: {solver.solve_time:.6f}s")
        print(f"Generation Time: {self.generator.generation_time:.6f}s")
        print(f"Loops Added: {self.generator.loops_added}")
        print(f"42 Pattern: {self.generator.has_42_pattern}")
        print(f"Seed: {self.config.seed}")
        print(f"\n{'═'*36}")

    def _handle_choice(self, choice: str) -> bool:
        """
        Handle user menu selection.

        Args:
            choice: Selected menu option.

        Returns:
            False when exiting the menu.
        """
        if choice == "1":
            self._regenerate()

        elif choice == "2":
            self._toggle_path()

        elif choice == "3":
            self._change_theme()

        elif choice == "4":
            self._save_maze()

        elif choice == "5":
            self._animate_solution()

        elif choice == "6":
            self._show_stats()
            self._pause()

        elif choice == "0":
            self.audio.stop()
            print("\nMeu tesouro? Se quiserem, podem pegá-lo! Procurem-no!")
            return False

        else:
            print("\nSelect a valid menu option (0-6).\n")
            self._pause()

        return True

    def _pause(self) -> None:
        """Wait for user confirmation."""
        input("Press ENTER to continue...")

    def _animate_solution(self) -> None:
        """
        Animate shortest maze solution.

        Displays the solution path incrementally
        using the active renderer theme.
        """
        solver = MazeSolver(self.maze, self.config)
        path = solver.solve()

        if not path:
            return

        for i in range(len(path) + 1):
            self.renderer.path = path[:i]
            print("\033[H", end="")
            self._show_title()
            self.renderer.render()

            time.sleep(0.05)

        self.path = path
        self.show_path = True

    def run(self) -> None:
        """
        Start interactive terminal loop.

        Continuously renders the maze and
        handles user interactions.
        """
        while True:
            try:
                self._clear_screen()
                self._show_title()
                self._render()
                self._show_menu()

                choice = input("Option: ").strip()
                if not self._handle_choice(choice):
                    break
            except KeyboardInterrupt:
                self.audio.stop()
                print("\nMeu tesouro? "
                      "Se quiserem, podem pegá-lo! Procurem-no!")
                break
