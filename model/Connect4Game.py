from typing import Optional, Tuple

from Connect4Board import Connect4Board


class Connect4Game:
    DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

    BOARD_ROWS = 6
    BOARD_COLUMNS = 7
    def __init__(self) -> None:
        self.board = Connect4Board(self.BOARD_ROWS, self.BOARD_COLUMNS )

        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.current_player: int = 1
        self.move_count: int = 0


    def is_valid_position(self, position: Tuple[int, int], piece: int) -> bool:
        row, column = position
        in_bounds = 0 <= row < self.BOARD_ROWS and 0 <= column < self.BOARD_COLUMNS
        return in_bounds and self.board.get_position(position) == piece



    def is_sequence_in_direction(
            self,
            start_position: Tuple[int, int],
            direction: Tuple[int, int],
            piece: int,
            sequence_length: int,
    ) -> bool:
        def sequence_count_in_direction(direction) -> int:
            count = 0
            for offset in range(sequence_length):
                new_position = (
                    start_position[0] + direction[0] * offset,
                    start_position[1] + direction[1] * offset,
                )
                if not self.is_valid_position(new_position, piece):
                    break
                count += 1
            return count

        # Count sequences in both the direction and its opposite
        sequence_count = sequence_count_in_direction(direction) + sequence_count_in_direction((-direction[0], -direction[1])) - 1

        return sequence_count >= sequence_length


    def is_sequence(self, position: Tuple[int, int], piece: int, sequence_length: int) -> bool:
        for direction in self.DIRECTIONS:
            if self.is_sequence_in_direction(
                    position, direction, piece, sequence_length
            ):
                return True
        return False



    def make_move(self, column: int) -> bool:
        if self.board.is_valid_move(column):
            for row in range(self.BOARD_ROWS -1, -1, -1):
                if self.board.get_position((row, column)) == 0:
                    self.board.set_position((row, column), self.current_player)
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

