# gui.py

from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLineEdit, QPushButton, QHBoxLayout,
    QVBoxLayout, QLabel, QMessageBox, QSizePolicy, QComboBox
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import QTimer, QElapsedTimer, Qt, QSize, pyqtSlot, QEvent
import random
from .solver import SudokuSolver
from .generator import SudokuGenerator

MAX_HINTS = 5

class SudokuGUI(QWidget):
    def __init__(self, puzzle, difficulty="medium"):
        super().__init__()
        self.difficulty = difficulty
        self.set_window_title()
        self.board = puzzle
        self.original_board = [row[:] for row in puzzle]
        self.hint_count = 0

        self.timer = QElapsedTimer()
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_time)

        self.cells = [[None] * 9 for _ in range(9)]
        self.grid = QGridLayout()
        self.time_label = QLabel()
        self.hint_button = QPushButton()
        self.validate_button = QPushButton()
        self.difficulty_dropdown = QComboBox()

        self.build_ui()

        self.timer.start()
        self.ui_timer.start(100)

        self.installEventFilter(self)
        self.resize(650, 800)  # Make layout visible on startup
        self.center_on_screen()

    def set_window_title(self):
        self.setWindowTitle(f"Sudoku - {self.difficulty.capitalize()}")

    def center_on_screen(self):
        screen_geometry = self.screen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Top bar with Exit, New Game, Difficulty ---
        top_bar_layout = QHBoxLayout()

        self.difficulty_dropdown.addItems(["easy", "medium", "hard"])
        self.difficulty_dropdown.setCurrentText(self.difficulty)
        self.difficulty_dropdown.currentTextChanged.connect(self.change_difficulty)
        self.difficulty_dropdown.setMinimumWidth(100)  # 👈 Fix width
        self.difficulty_dropdown.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        reset_button = QPushButton("Reset")
        new_game_button = QPushButton("New Game")
        exit_button = QPushButton("Exit")
        reset_button.clicked.connect(self.reset_board)
        new_game_button.clicked.connect(self.start_new_game)
        exit_button.clicked.connect(self.close)

        top_bar_layout.addWidget(QLabel("Difficulty:"))
        top_bar_layout.addWidget(self.difficulty_dropdown)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(reset_button)
        top_bar_layout.addWidget(new_game_button)
        top_bar_layout.addWidget(exit_button)

        main_layout.addLayout(top_bar_layout)

        # --- Time Label ---
        self.time_label.setText("Time: 0 sec")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.time_label)

        # --- Sudoku Grid ---
        self.grid.setSpacing(1)  # 👈 Add spacing between both rows & columns
        for r in range(9):
            for c in range(9):
                cell = QLineEdit()
                cell.setMaxLength(1)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

                base_color = "#f2f2f2" if ((r // 3 + c // 3) % 2 == 0) else "#ffffff"
                cell.setStyleSheet(
                    f"""
                    background-color: {base_color};
                    border: 1px solid #999;
                    margin: 0px;
                    """
                )

                if self.board[r][c] != '.':
                    cell.setText(self.board[r][c])
                    cell.setReadOnly(True)
                    cell.setStyleSheet(cell.styleSheet() + "color: black; font-weight: bold;")
                else:
                    cell.setValidator(QIntValidator(1, 9))
                    cell.textChanged.connect(self.check_validate_ready)

                self.grid.addWidget(cell, r, c)
                self.cells[r][c] = cell

        main_layout.addLayout(self.grid)

        # --- Buttons ---
        self.hint_button.setText(f"Get Hint ({MAX_HINTS - self.hint_count} left)")
        self.hint_button.clicked.connect(self.get_hint)

        self.validate_button.setText("Validate")
        self.validate_button.clicked.connect(self.validate_solution)
        self.validate_button.setEnabled(False)

        main_layout.addWidget(self.hint_button)
        main_layout.addWidget(self.validate_button)

        self.setLayout(main_layout)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            QTimer.singleShot(0, self.resize_cells)
        return super().eventFilter(obj, event)

    def resize_cells(self):
        available_width = self.width() - 40
        available_height = self.height() - 250  # leave room for top/bottom UI
        grid_size = min(available_width, available_height)
        cell_size = grid_size // 9
        font_size = max(10, int(cell_size * 0.6))

        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                cell.setFixedSize(QSize(cell_size, cell_size))
                cell.setFont(QFont("Arial", font_size))

    def update_time(self):
        ms = self.timer.elapsed()
        h, rem = divmod(ms, 3600000)
        m, rem = divmod(rem, 60000)
        s, rem = divmod(rem, 1000)
        self.time_label.setText(f"Time: {h} hr, {m} min, {s} sec, {rem} ms")
        self.check_validate_ready()

    def get_current_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.cells[r][c].text().strip()
                val = val if val in {'1','2','3','4','5','6','7','8','9'} else '.'
                row.append(val)
            board.append(row)
        return board

    def get_hint(self):
        if self.hint_count >= MAX_HINTS:
            QMessageBox.information(self, "No More Hints", "You have used all available hints.")
            return

        current_board = self.get_current_board()
        try:
            solver = SudokuSolver(current_board)
            if not solver.is_valid():
                QMessageBox.warning(self, "Invalid Board", "Board has rule violations.")
                return
            solved = solver.solve()
        except Exception as e:
            QMessageBox.warning(self, "Unsolvable", f"Current board is not solvable.\n\n{e}")
            return
        
        empty_cells = [(r, c) for r in range(9) for c in range(9) if self.board[r][c] == '.' and self.cells[r][c].text() == '']
        if not empty_cells:
            QMessageBox.information(self, "Complete", "Board is already complete!")
            return

        r, c = random.choice(empty_cells)  # Pick one at random
        self.cells[r][c].setText(solved[r][c])
        self.hint_count += 1
        self.hint_button.setText(f"Get Hint ({MAX_HINTS - self.hint_count} left)")

    @pyqtSlot()
    def check_validate_ready(self):
        board = self.get_current_board()
        filled = all(val != '.' for row in board for val in row)
        self.validate_button.setEnabled(filled)

    def validate_solution(self):
        board = self.get_current_board()
        try:
            solver = SudokuSolver(board)
            if solver.is_valid():
                self.ui_timer.stop()
                ms = self.timer.elapsed()
                h, rem = divmod(ms, 3600000)
                m, rem = divmod(rem, 60000)
                s, rem = divmod(rem, 1000)

                reply = QMessageBox.question(
                    self,
                    "Congratulations!",
                    f"Puzzle is correct!\nTime: {h} hr, {m} min, {s} sec, {rem} ms\n\nDo you want to play again?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.start_new_game()
                else:
                    self.close()
            else:
                QMessageBox.warning(self, "Incorrect", "The solution is not a valid Sudoku.")
        except Exception as ex:
            QMessageBox.warning(self, "Error", f"An error occurred: {ex}")

    def start_new_game(self):
        self.difficulty = self.difficulty_dropdown.currentText()
        generator = SudokuGenerator(difficulty=self.difficulty)
        new_puzzle = generator.get_puzzle()

        self.board = new_puzzle
        self.original_board = [row[:] for row in new_puzzle]
        self.hint_count = 0
        self.timer.restart()
        self.hint_button.setText(f"Get Hint ({MAX_HINTS} left)")
        self.validate_button.setEnabled(False)

        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                val = new_puzzle[r][c]
                cell.blockSignals(True)

                base_color = "#f2f2f2" if ((r // 3 + c // 3) % 2 == 0) else "#ffffff"
                style = f"background-color: {base_color}; border: 1px solid #999;"

                if val != '.':
                    cell.setText(val)
                    cell.setReadOnly(True)
                    cell.setStyleSheet(style + "color: black; font-weight: bold;")
                else:
                    cell.setText('')
                    cell.setReadOnly(False)
                    cell.setValidator(QIntValidator(1, 9))
                    cell.setStyleSheet(style)

                cell.blockSignals(False)

        self.ui_timer.start(100)
        self.resize_cells()


    def reset_board(self):
        self.board = [row[:] for row in self.original_board]
        # self.hint_count = 0
        self.timer.restart()
        self.hint_button.setText(f"Get Hint ({MAX_HINTS - self.hint_count} left)")
        self.validate_button.setEnabled(False)

        for r in range(9):
            for c in range(9):
                cell = self.cells[r][c]
                val = self.board[r][c]
                cell.blockSignals(True)

                base_color = "#f2f2f2" if ((r // 3 + c // 3) % 2 == 0) else "#ffffff"
                style = f"background-color: {base_color}; border: 1px solid #999;"

                if val != '.':
                    cell.setText(val)
                    cell.setReadOnly(True)
                    cell.setStyleSheet(style + "color: black; font-weight: bold;")
                else:
                    cell.setText('')
                    cell.setReadOnly(False)
                    cell.setValidator(QIntValidator(1, 9))
                    cell.setStyleSheet(style)

                cell.blockSignals(False)

        self.ui_timer.start(100)
        self.resize_cells()


    def change_difficulty(self, value):
        self.difficulty = value
        self.set_window_title()
        self.start_new_game()


