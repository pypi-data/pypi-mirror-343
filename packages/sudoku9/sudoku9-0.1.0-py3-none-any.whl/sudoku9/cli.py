import argparse
from rich import print
import sys
from PyQt6.QtWidgets import QApplication
import qdarktheme

from .gui import SudokuGUI
from .solver import SudokuSolver
from .generator import SudokuGenerator
from .utils import print_board

def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver & Generator CLI")
    subparsers = parser.add_subparsers(dest="command")

    # === NEW SUBCOMMAND ===
    new_parser = subparsers.add_parser("new", help="Generate a Sudoku puzzle of given difficulty")
    new_parser.add_argument(
        "difficulty",
        choices=["easy", "medium", "hard"],
        nargs="?",
        default="medium",
        help="Difficulty level (default: medium)"
    )

    # === SOLVE SUBCOMMAND ===
    solve_parser = subparsers.add_parser("solve", help="Solve a Sudoku puzzle")
    solve_parser.add_argument(
        "string",
        nargs="?",
        help="Sudoku puzzle as comma-separated 9 rows (default input method)"
    )
    solve_parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to a file containing the puzzle (9 lines, 1 per row)"
    )

    # === PLAY SUBCOMMAND ===
    play_parser = subparsers.add_parser("play", help="Play Sudoku in GUI")
    play_parser.add_argument(
        "difficulty",
        choices=["easy", "medium", "hard"],
        nargs="?",
        default="medium",
        help="Difficulty level for the game (default: medium)"
    )

    args = parser.parse_args()

    # === SOLVE ===
    if args.command == "solve":
        if args.file and args.string:
            print("[bold red]Error:[/bold red] Provide only one input method: either file or string.")
            return

        if args.file:
            try:
                with open(args.file, "r") as f:
                    raw_rows = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"[bold red]Error:[/bold red] File '{args.file}' not found.")
                return
        elif args.string:
            raw_rows = [row.strip() for row in args.string.split(",") if row.strip()]
        else:
            print("[bold red]Error:[/bold red] No input provided. Use a puzzle string or pass `-f` for a file.")
            return

        if len(raw_rows) != 9 or any(len(row) != 9 for row in raw_rows):
            print(f"[bold red]Error:[/bold red] Expected 9 rows of 9 characters each, got:\n{raw_rows}")
            return

        board = [list(row) for row in raw_rows]

        try:
            solver = SudokuSolver(board)
            solved = solver.solve()

            print_board(solved, title="Solved Sudoku", style="bold magenta")

            print("\n[bold yellow]Solved Puzzle (for other use):[/bold yellow]")
            print(",".join("".join(row) for row in solved))
        except Exception as e:
            print(f"[bold red]Error:[/bold red] {e}")

    # === NEW ===
    elif args.command == "new":
        generator = SudokuGenerator(difficulty=args.difficulty)
        puzzle = generator.get_puzzle()
        print_board(puzzle, title=f"Generated Sudoku ({args.difficulty.title()})", style="bold green")

        print("\n[bold yellow]Raw Puzzle (for input use):[/bold yellow]")
        print(",".join("".join(row) for row in puzzle))

    # === PLAY ===
    elif args.command == "play":
        generator = SudokuGenerator(difficulty=args.difficulty)
        puzzle = generator.get_puzzle()

        app = QApplication(sys.argv)
        app.setStyleSheet(qdarktheme.load_stylesheet("light"))
        window = SudokuGUI(puzzle, difficulty=args.difficulty)
        window.show()
        sys.exit(app.exec())

    else:
        parser.print_help()
