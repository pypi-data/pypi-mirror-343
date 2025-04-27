"""Solve the sudoku"""

import random

class SudokuSolver:
    def __init__(self, board):
        """Initialize the solver with a 9x9 board."""
        if len(board) != 9 or any(len(row) != 9 for row in board):
            raise ValueError("Invalid Board: Must be 9x9")
        
        self._original_board = board  # Store the original board
        self.board = [list(row) for row in board]  # Convert to a mutable format

        if not self._is_valid():
            raise ValueError("Invalid Sudoku Board")

    def solve(self):
        """Solve the Sudoku puzzle."""
        if self._solve_sudoku():
            return ["".join(row) for row in self.board]
        raise ValueError("No Solution Found")

    def is_valid(self):
        """Validate the board."""
        return self._is_valid()
    
    def _is_valid(self):
        """Check if the board is a valid Sudoku configuration."""
        rows, cols, grids = [set() for _ in range(9)], [set() for _ in range(9)], [set() for _ in range(9)]
        
        for r in range(9):
            for c in range(9):
                num = self.board[r][c]
                if num == ".":
                    continue
                
                grid_idx = (r // 3) * 3 + (c // 3)
                
                if num in rows[r] or num in cols[c] or num in grids[grid_idx]:
                    return False

                rows[r].add(num)
                cols[c].add(num)
                grids[grid_idx].add(num)
        
        return True

    def _solve_sudoku(self):
        """Recursive solver using backtracking."""
        empty = self._find_empty()
        if not empty:
            return True
        row, col = empty

        nums = list(map(str, range(1, 10)))
        # Comment below line of want unique solution each time
        random.shuffle(nums) #Shuffle to explore random paths

        for num in nums:
            if self._is_valid_move(num, row, col):
                self.board[row][col] = num
                if self._solve_sudoku():
                    return True
                self.board[row][col] = '.'  # Backtrack
        return False

    def _find_empty(self):
        """Find an empty cell."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '.':
                    return i, j
        return None

    def _is_valid_move(self, num, row, col):
        """Check if placing `num` at (row, col) is valid."""
        grid_start_row, grid_start_col = (row // 3) * 3, (col // 3) * 3
        
        return (
            num not in self.board[row] and
            num not in (self.board[r][col] for r in range(9)) and
            num not in (
                self.board[r][c]
                for r in range(grid_start_row, grid_start_row + 3)
                for c in range(grid_start_col, grid_start_col + 3)
            )
        )



# if __name__ == "__main__":
#     board = [
#         ".3..7....",
#         "6....5...",
#         ".98....6.",
#         "8...6...3",
#         "4..8.3..1",
#         "7...2...6",
#         ".6.....8.",
#         "........5",
#         "....8...."
#     ]
#     solver = SudokuSolver(board)
#     try:
#         solved = solver.solve()
#         for row in solved:
#             print(row)
#     except ValueError as e:
#         print(e)
