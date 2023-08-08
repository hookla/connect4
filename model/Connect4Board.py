from typing import List, Tuple

import colorama
import torch

colorama.init(autoreset=True)



class InvalidMoveError(Exception):
    pass

class Connect4Board:

    BOARD_ROWS = 6
    BOARD_COLUMNS = 7
    MAX_MOVES = BOARD_ROWS * BOARD_COLUMNS
    EMPTY_CELL = 0

    def __init__(self) -> None:
        self.board: List[List[int]] = [[0 for _ in range(self.BOARD_COLUMNS)] for _ in range(self.BOARD_ROWS)]
        self.first_empty_row_per_column = [self.BOARD_ROWS - 1 for _ in range(self.BOARD_COLUMNS)]

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        return 0 <= position[0] < self.BOARD_ROWS and 0 <= position[1] < self.BOARD_COLUMNS

    def is_valid_move(self, column: int) -> bool:
        if self.first_empty_row_per_column[column] >= 0:
            return True
        else:
            return False

    def make_move(self, column: int, piece: int) -> int:
        if not self.is_valid_move(column):
            raise InvalidMoveError(f"column {column} is not a valid move.")

        row = self.first_empty_row_per_column[column]
        self.board[row][column] = piece
        self.first_empty_row_per_column[column] -= 1
        return row

    def set_board_state(self, state: List[List[int]]) -> None:
        if len(state) != self.BOARD_ROWS or any(len(row) != self.BOARD_COLUMNS for row in state):
            raise ValueError(f'Invalid state, expected a list with {self.BOARD_ROWS} rows and {self.BOARD_COLUMNS} columns')
        self.board = [list(row) for row in state]


    def get_position(self, position: Tuple[int, int]) -> int:
        return self.board[position[0]][position[1]]

    def set_position(self, position: Tuple[int, int], player: int) -> None:
        self.board[position[0]][position[1]] = player

    def print_board(self) -> None:


        disk_player1:str = colorama.Fore.RED + "●"
        disk_player2:str = colorama.Fore.YELLOW + "●"
        disk_empty:str = colorama.Fore.WHITE + "●"

        def get_disk(player: int) -> str:
            if player == 1:
                return disk_player1
            elif player == -1:
                return disk_player2
            else:
                return disk_empty

        board_representation = "┏━━━━━━━━━━━━━━━┓\n"

        for row in self.board:
            row_representation = "┃ "
            for cell in row:
                disk = get_disk(cell)
                row_representation += disk + " "
            row_representation += "┃\n"
            board_representation += row_representation

        board_representation += "┗━━━━━━━━━━━━━━━┛\n"
        column_numbers = "  " + " ".join(str(i) for i in range(len(self.board[0]))) + "\n"
        board_representation += column_numbers

        print(board_representation)

    def get_valid_moves(self) -> List[int]:
        return [c for c in range(7) if self.is_valid_move(c)]

    def get_state(self) -> torch.Tensor:
        return torch.tensor(self.board, dtype=torch.float).reshape(-1)

