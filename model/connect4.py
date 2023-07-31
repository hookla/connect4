from typing import List, Optional, Tuple


class Connect4:
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    BOARD_ROWS = 6
    BOARD_COLUMNS = 7

    def create_board(self) -> List[List[int]]:
        # The board has 6 rows and 7 columns
        return [[0 for _ in range(self.BOARD_COLUMNS)] for _ in range(self.BOARD_ROWS)]



    def __init__(self) -> None:
        self.board: List[List[int]] = self.create_board()
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

    def is_sequence_in_direction(
            self,
            position: Tuple[int, int],
            direction: Tuple[int, int],
            piece: int,
            sequence_length: int,
    ) -> bool:
        # This function checks if there's a sequence of `sequence_length` pieces
        # starting from the (row, column) in the direction defined by deltas
        direction_row, direction_column = direction
        for offset in range(sequence_length):
            new_position= (
                position[0] + direction_row * offset,
                position[1] + direction_column * offset,
            )
            if (
                    not (
                            0 <= new_position[0] < self.BOARD_ROWS
                            and 0 <= new_position[1] < self.BOARD_COLUMNS
                    )
                    or self.board[new_position[0], new_position[1]] != piece
            ):
                return False
        return True

    def is_sequence(self, position: Tuple[int, int], piece: int, sequence_length: int) -> bool:
        new_position = (0,0)
        # This function checks in all directions for a sequence of `sequence_length` pieces
        for direction in self.DIRECTIONS:
            for offset in range(-sequence_length+1, 1):  # To account for both directions
                new_position = position[0] - direction[0] * offset, position[1] - direction[1] * offset
                if self.is_sequence_in_direction(
                        new_position, direction, piece, sequence_length
                ):
                    return True
        return False

    # Update your make_move method
    def make_move(self, column: int) -> bool:
        if self.is_valid_move(column):
            for row in range(5, -1, -1):
                if self.board[row][column] == 0:
                    self.board[row][column] = self.current_player
                    break
            self.move_count += 1
            if self.move_count >= 7 and self.is_sequence(
                    (row, column), self.current_player, 4  # Check for a sequence of 4
            ):
                self.game_over = True
                self.winner = self.current_player
            else:
                # Switch to the other player
                self.current_player *= -1
            return True
        return False


    def get_state(self) -> List[int]:
        # Flatten the board into a 1D list and return it
        return [cell for row in self.board for cell in row]
