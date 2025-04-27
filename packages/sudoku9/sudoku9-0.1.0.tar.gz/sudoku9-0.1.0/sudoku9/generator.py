import random
from .solver import SudokuSolver

class SudokuGenerator:
    def __init__(self, difficulty="medium", removal_attempts=None):
        """Initialize Sudoku Generator with difficulty level."""
        self.difficulty = difficulty
        self.removal_attempts = removal_attempts if removal_attempts is not None else self._get_default_attempts()
        self.base_grid = self._create_full_grid()
        self.puzzle = self._remove_numbers()

    def _get_default_attempts(self):
        """Return default removal attempts based on difficulty level."""
        ranges = {
            "easy": (30, 40),
            "medium": (40, 50),
            "hard": (50, 60)
        }
        low, high = ranges.get(self.difficulty, (40, 50))
        return random.randint(low, high)

    def _create_full_grid(self):
        """Generate a completed Sudoku grid using backtracking."""
        board = [['.'] * 9 for _ in range(9)]
        self._fill_grid(board)
        return board

    def _fill_grid(self, board):
        """Fills the Sudoku grid using backtracking."""
        numbers = list(map(str, range(1, 10)))
        random.shuffle(numbers)  # Ensures different boards each time

        def solve():
            empty = self._find_empty(board)
            if not empty:
                return True  # Solved

            row, col = empty
            for num in numbers:
                if self._is_valid_move(board, num, row, col):
                    board[row][col] = num
                    if solve():
                        return True
                    board[row][col] = '.'  # Backtrack

            return False

        solve()

    
    def _remove_numbers(self):
        """Remove numbers from the grid to create a puzzle."""
        puzzle = [row[:] for row in self.base_grid]
        attempts = self.removal_attempts  # Use configurable attempts

        while attempts > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if puzzle[row][col] != '.':
                temp = puzzle[row][col]
                puzzle[row][col] = '.'

                try:
                    test_solver = SudokuSolver([row[:] for row in puzzle])
                    test_solver.solve()  # Will raise if unsolvable
                except ValueError:
                    puzzle[row][col] = temp  # Restore if unsolvable
                else:
                    attempts -= 1

        return puzzle

    def _find_empty(self, board):
        """Find an empty cell in the board."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    return i, j
        return None

    def _is_valid_move(self, board, num, row, col):
        """Check if placing `num` at (row, col) is valid."""
        grid_start_row, grid_start_col = (row // 3) * 3, (col // 3) * 3

        return (
            num not in board[row] and
            num not in (board[r][col] for r in range(9)) and
            num not in (
                board[r][c]
                for r in range(grid_start_row, grid_start_row + 3)
                for c in range(grid_start_col, grid_start_col + 3)
            )
        )

    def get_puzzle(self):
        """Return the puzzle as a list of strings."""
        return ["".join(row) for row in self.puzzle]
