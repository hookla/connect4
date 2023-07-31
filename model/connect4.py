from typing import List, Optional


def create_board() -> List[List[int]]:
    # The board has 6 rows and 7 columns
    return [[0 for _ in range(7)] for _ in range(6)]


class Connect4:
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    BOARD_ROWS = 6
    BOARD_COLUMNS = 7

    def __init__(self) -> None:
        self.board: List[List[int]] = create_board()
        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.current_player: int = 1
        self.move_count: int = 0

    def print_board(self) -> None:
        print(
            "\n".join(
                [" ".join([str(cell) for cell in row]) for row in self.board]
            )
        )

    def is_valid_move(self, column: int) -> bool:
        # A move is valid if the top row of a column is not occupied
        return self.board[0][column] == 0

    def get_valid_moves(self) -> List[int]:
        return [c for c in range(7) if self.is_valid_move(c)]

    def make_move(self, column: int) -> bool:
        if self.is_valid_move(column):
            for row in range(5, -1, -1):
                if self.board[row][column] == 0:
                    self.board[row][column] = self.current_player
                    break
            self.move_count += 1
            if self.move_count >= 7 and self.is_winner(
                row, column, self.current_player
            ):
                self.game_over = True
                self.winner = self.current_player
            else:
                # Switch to the other player
                self.current_player *= -1
            return True
        return False

    def is_winner(self, row: int, column: int, piece: int) -> bool:
        for delta_row, delta_column in self.DIRECTIONS:
            for offset in range(4):
                new_row = row - delta_row * offset
                new_column = column - delta_column * offset
                if self.check_direction(
                    new_row, new_column, delta_row, delta_column, piece
                ):
                    return True
        return False

    def check_direction(
        self,
        row: int,
        column: int,
        delta_row: int,
        delta_column: int,
        piece: int,
    ) -> bool:
        for offset in range(4):
            new_row, new_column = (
                row + delta_row * offset,
                column + delta_column * offset,
            )
            if (
                not (
                    0 <= new_row < self.BOARD_ROWS
                    and 0 <= new_column < self.BOARD_COLUMNS
                )
                or self.board[new_row][new_column] != piece
            ):
                return False
        return True

    def get_state(self) -> List[int]:
        # Flatten the board into a 1D list and return it
        return [cell for row in self.board for cell in row]
