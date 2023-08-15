from typing import Tuple

import colorama
import numpy as np
import torch

colorama.init(autoreset=True)


class InvalidMoveError(Exception):
    pass

class Connect4Board:

    BOARD_ROWS = 6
    BOARD_COLUMNS = 7
    MAX_MOVES = BOARD_ROWS * BOARD_COLUMNS
    EMPTY_CELL = 0

    move_history = []

    def __init__(self) -> None:
        self._board = np.zeros((self.BOARD_ROWS, self.BOARD_COLUMNS), dtype=int)
        self._first_empty_row_per_column = np.full(self.BOARD_COLUMNS, self.BOARD_ROWS - 1)


    def is_valid_move(self, column: int) -> bool:
        if self._first_empty_row_per_column[column] >= 0:
            return True
        else:
            return False

    def get_valid_moves(self) -> np.ndarray:
        return np.where(self._first_empty_row_per_column != -1)[0]

    def is_full(self) -> bool:
        return self.move_count == self.MAX_MOVES

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        return 0 <= position[0] < self.BOARD_ROWS and 0 <= position[1] < self.BOARD_COLUMNS

    def make_move(self, column: int, piece: int) -> int:
        if not self.is_valid_move(column):
            raise InvalidMoveError(f"column {column} is not a valid move.")

        row = self._first_empty_row_per_column[column]
        self._board[row, column] = piece
        self._first_empty_row_per_column[column] -= 1
        self.move_history.append(column)
        return row

    def undo_last_move(self) -> None:
        column = self.move_history.pop()
        row = self._first_empty_row_per_column[column] + 1
        self._board[row, column] = self.EMPTY_CELL
        self._first_empty_row_per_column[column] += 1

    def get_first_empty_row(self, column: int) -> int:
        return self._first_empty_row_per_column[column]

    def set_first_empty_row_per_column(self) -> None:
        """Update the first_empty_row_per_column array to reflect the current board state."""
        for col in range(self.BOARD_COLUMNS):
            for row in range(self.BOARD_ROWS-1, -1, -1):  # Start from the bottom and move upwards
                if self._board[row, col] == 0:
                    self._first_empty_row_per_column[col] = row
                    break
            else:
                # This will execute if the inner loop completes without hitting 'break'
                # meaning the column is full
                self._first_empty_row_per_column[col] = -1

    def set_board_state(self, state: np.ndarray) -> None:
        if state.shape != (self.BOARD_ROWS, self.BOARD_COLUMNS):
            raise ValueError(f'Invalid state, expected an array with {self.BOARD_ROWS} rows and {self.BOARD_COLUMNS} columns')

        self._board = state
        self.set_first_empty_row_per_column()
   
    def get_position(self, position: Tuple[int, int]) -> int:
        return self._board[position]


    def visualize(self):
        # Convert numbers to characters
        disk_player1 = colorama.Fore.RED + "●"
        disk_player2 = colorama.Fore.YELLOW + "●"
        disk_empty = colorama.Fore.WHITE + "○"  # Using an empty circle for vacant spots
        border = colorama.Fore.WHITE + "│"

        visual_board = np.where(self._board == 1, disk_player1, np.where(self._board == -1, disk_player2, disk_empty))

        # Convert the 2D array to the desired string format
        output = []
        output.append(colorama.Fore.WHITE +"┌─────────────┐\n")

        for row in visual_board:
            output_row = border.join(cell for cell in row) + border + '\n'  # Adding a separator at the end of each row
            output.append(border+output_row)

        output.append(colorama.Fore.WHITE +"└─────────────┘\n")
        return ''.join(output)

    def get_state(self) -> torch.Tensor:
        return torch.tensor(self._board, dtype=torch.float).reshape(-1)

