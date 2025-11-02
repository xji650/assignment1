import pygame
import random

from typing import Any

from hlogedu.search.common import ClassParameter
from hlogedu.search.problem import Problem, action, DDRange, Heuristic
from hlogedu.search.visualizer import SolutionVisualizer

# Visualization (you do not have to modify this!)
##############################################################################


class NQueensVisualizer(SolutionVisualizer):
    """Pygame-based visualizer for the N-Queens problem."""

    def draw_state(self, state: Any) -> None:
        """Draw a board with queens placed according to the given state."""
        n = self.problem.n_queens
        cell_size = self.get_cell_size()

        # Clear screen
        self.screen.fill((255, 255, 255))

        # Draw chessboard
        for row in range(n):
            for col in range(n):
                rect = pygame.Rect(
                    col * cell_size, row * cell_size, cell_size, cell_size
                )
                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, rect)

        # Draw queens
        for col, row in enumerate(state):
            center = (
                col * cell_size + cell_size // 2,
                row * cell_size + cell_size // 2,
            )
            radius = cell_size // 3
            pygame.draw.circle(self.screen, (200, 0, 0), center, radius)

        pygame.display.flip()

    def animate_transition(self, state: Any, action: Any, new_state: Any) -> None:
        """Smoothly animate the transition from one state to another."""
        n = self.problem.n_queens
        cell_size = self.get_cell_size()
        delay = self.get_delay()

        # figure out which queens moved
        moved = [
            (col, state[col], new_state[col])
            for col in range(n)
            if state[col] != new_state[col]
        ]

        if not moved:
            return  # nothing changed

        # number of steps in animation
        steps = 10

        for step in range(steps + 1):
            # interpolate state
            intermediate = list(state)
            for col, old_row, new_row in moved:
                interp_row = old_row + (new_row - old_row) * (step / steps)
                intermediate[col] = interp_row

            # draw interpolated state
            self.draw_interpolated_state(intermediate)
            pygame.time.delay(delay // max(1, steps))

        # final draw (ensure exact new state)
        self.draw_state(new_state)

    def draw_interpolated_state(self, state) -> None:
        """Draw state where row positions can be floats (for animation)."""
        n = self.problem.n_queens
        cell_size = self.get_cell_size()

        # Draw board
        self.screen.fill((255, 255, 255))
        for row in range(n):
            for col in range(n):
                rect = pygame.Rect(
                    col * cell_size, row * cell_size, cell_size, cell_size
                )
                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, rect)

        # Draw queens (supports float rows)
        for col, row in enumerate(state):
            center = (
                col * cell_size + cell_size // 2,
                int(row * cell_size + cell_size // 2),
            )
            radius = cell_size // 3
            pygame.draw.circle(self.screen, (200, 0, 0), center, radius)

        pygame.display.flip()


# Problem
##############################################################################


class NQueensIterativeRepair(Problem):
    """N-Queens problem

    This problem consists in placing n non-attacking queens on an
    nxn chessboard.

    This implementations starts with an nxn chessboard that already
    contains N queens on it, and tries to solve the problem by iteratively
    moving the queens to different possitions
    """

    NAME = "NQueensIR"
    VISUALIZER = NQueensVisualizer
    PARAMS = [
        ClassParameter(name="n_queens", type=int, default="8", help="Number of queens."),
        ClassParameter(name="seed", type=int, default="123456", help="Random seed."),
    ]

    def __init__(self, n_queens: int = 8, seed: int = 123456):
        super().__init__()
        self.n_queens = n_queens
        self.seed = seed
        self.b_size = max(4, self.n_queens)
        random.seed(self.seed)

    def get_start_states(self):
        """Generate random initial configuration with N queens on the board."""
        return [tuple(random.randint(0, self.b_size - 1) for _ in range(self.b_size))]

    def is_goal_state(self, state):
        """A state is a goal if no queens attack each other."""
        if not isinstance(state, (tuple, list)):
            return False
            
        if len(state) != self.b_size:
            return False
        
        n = len(state)
        
        for col1 in range(n):
            row1 = state[col1]
            for col2 in range(col1 + 1, n):
                row2 = state[col2]
                
                # Check if queens attack each other
                # Same row
                if row1 == row2:
                    return False
                
                # Same diagonal
                if abs(row1 - row2) == abs(col1 - col2):
                    return False
        
        return True
    
    def is_valid_state(self, state):
        """A state is valid if all queens are within the board boundaries."""
        if not isinstance(state, (tuple, list)):
            return False
            
        if len(state) != self.b_size:
            return False
            
        return all(0 <= row < self.b_size for row in state)

    # Actions go here...
    @action(DDRange(0, 'b_size'), DDRange(0, 'b_size'), cost=1)
    def move_queen(self, state, queen_col, new_row):
        """Move the queen in column `queen_col` to `new_row`."""

        if queen_col >= len(state) or new_row >= self.b_size:
            return None

        old_row = state[queen_col]
        
        # Can't move to the same position
        if old_row == new_row:
            return None
        
        new_state = list(state)
        new_state[queen_col] = new_row
        new_state = tuple(new_state)

        return new_state


# Heuristic
##############################################################################


@NQueensIterativeRepair.heuristic
class RepairHeuristic(Heuristic):
    """
    Heuristic: Minimal number of moves to achieve unique rows.
    """

    def compute(self, state):
        """Compute minimum moves needed to achieve unique rows."""
        if not isinstance(state, (tuple, list)):
            return float('inf')
        
        n = len(state)
        
        # Sort current rows
        sorted_rows = sorted(state)
        
        # Count how many queens are NOT in their target position
        # Target positions are 0, 1, 2, ..., n-1 (sorted)
        moves_needed = sum(1 for i in range(n) if sorted_rows[i] != i)
        
        return moves_needed
