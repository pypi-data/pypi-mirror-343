# sudoku9

A Sudoku solver and puzzle generator with **CLI** and **GUI** support.  
Built with `PyQt6`, `rich`, and `qdarktheme` for a beautiful user experience.

---

## ✨ Features

- 🔥 Solve Sudoku puzzles via the command-line or Python imports.
- 🎲 Generate new Sudoku puzzles with selectable difficulty (`easy`, `medium`, `hard`).
- 🖥️ Play Sudoku interactively via a GUI built with PyQt6.
- 🎨 Stylish and colorful CLI output using `rich`.

---

## 📦 Installation

Install from PyPI:

```bash
pip install sudoku9
```


## 🚀 Usage
1. CLI (Command Line)
After installation, use sudoku9 command from your terminal.

➡️ Generate a new puzzle
```bash
sudoku9 new easy
```
(If no difficulty is specified, defaults to medium.)
Output:
- A nicely formatted table view of the unsolved new Sudoku.
- The new Sudoku as a single string:
    ```
    86392...4,92..1..6.,.148.392.,..9..214.,..2147.89,.4.......,.3.5.....,5..4.1.3.,4..238...
    ```


➡️ Solve a puzzle from a string
```bash
sudoku9 solve "53..7....","6..195...",".98....6.","8...6...3","4..8.3..1","7...2...6",".6....28.","...419..5","....8..79"
```
Output:
- A nicely formatted table view of the solved Sudoku.
- The solved Sudoku as a single string:
    ```
    534678912,672195348,198342567,859761423,426853791,713924856,961537284,287419635,345286179
    ```


➡️ Solve a puzzle from a file
```bash
sudoku9 solve -f <path/to/puzzle.txt>
```
(The file should contain 9 lines, each with 9 characters.)

➡️ Play Sudoku with GUI
```bash
sudoku9 play hard
```
(Default difficulty is medium if not specified.)

2. As a Python Module
You can import and use sudoku9 programmatically in your own scripts.

➡️ Example: Solve a Sudoku puzzle
```python
from sudoku9 import SudokuSolver

# Define a Sudoku board
board = [
    "53..7....",
    "6..195...",
    ".98....6.",
    "8...6...3",
    "4..8.3..1",
    "7...2...6",
    ".6....28.",
    "...419..5",
    "....8..79",
]

solver = SudokuSolver(board)
solved_board = solver.solve()

for row in solved_board:
    print(" ".join(row))
```

➡️ Example: Generate a Sudoku puzzle
```python
from sudoku9 import SudokuGenerator

generator = SudokuGenerator(difficulty="hard")
puzzle = generator.get_puzzle()

for row in puzzle:
    print(" ".join(row))
```



## 🌟 Author
Kunal Kumar
[GitHub](https://github.com/kunalsingh2904)
