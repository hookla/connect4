from typing import List, Tuple

import colorama
import torch

colorama.init(autoreset=True)

class Connect4Board:


    def __init__(self, board_rows: int, board_columns: int) -> None:
        self.board: List[List[int]] = [[0 for _ in range(board_columns)] for _ in range(board_rows)]
        self.board_rows = board_rows
        self.board_columns = board_columns


    def set_board_state(self, state: List[List[int]]) -> None:
        if len(state) != self.board_rows or any(len(row) != self.board_columns for row in state):
            raise ValueError(f'Invalid state, expected a list with {self.board_rows} rows and {self.board_columns} columns')
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


    def is_valid_move(self, column: int) -> bool:
        # A move is valid if the top row of a column is not occupied
        return self.board[0][column] == 0

    def get_valid_moves(self) -> List[int]:
        return [c for c in range(7) if self.is_valid_move(c)]

    def get_state(self) -> torch.Tensor:
        return torch.tensor(self.board, dtype=torch.float).reshape(-1)

