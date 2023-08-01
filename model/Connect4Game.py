from typing import Optional, Tuple

from Connect4Board import Connect4Board


class Connect4Game:
    DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

    BOARD_ROWS = 6
    BOARD_COLUMNS = 7
    MAX_MOVES = BOARD_ROWS * BOARD_COLUMNS
    def __init__(self) -> None:
        self.board = Connect4Board(self.BOARD_ROWS, self.BOARD_COLUMNS )
        self.draw: bool = False
        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.current_player: int = 1
        self.move_count: int = 0


    def is_valid_position(self, position: Tuple[int, int], piece: int) -> bool:
        row, column = position
        in_bounds = 0 <= row < self.BOARD_ROWS and 0 <= column < self.BOARD_COLUMNS
        return in_bounds and self.board.get_position(position) == piece



    def sequence_count_in_both_directions(
            self,
            start_position: Tuple[int, int],
            direction: Tuple[int, int],
            piece: int,
            max_desired_sequence_length: int,
    ) -> int:
        def sequence_count_in_direction(direction) -> int:
            count = 0
            for offset in range(max_desired_sequence_length):
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

        return sequence_count


    def is_sequence(self, position: Tuple[int, int], piece: int, max_desired_sequence_length: int) -> int:
        max_sequence_count = 0
        for direction in self.DIRECTIONS:
            sequence_count = self.sequence_count_in_both_directions(
                    position, direction, piece, max_desired_sequence_length
            )
            if sequence_count > max_sequence_count:
                max_sequence_count = sequence_count
            if max_sequence_count >= max_desired_sequence_length:
                return max_desired_sequence_length
        return max_sequence_count

    def reward(self, longest_sequence: int, column: int) -> int:
        reward = 0
        if longest_sequence == 4:
            reward += 1000 + (self.MAX_MOVES - self.move_count) # Bonus for winning quickly
        elif longest_sequence == 3:
            reward += 200
        elif longest_sequence == 2:
            reward += 100

        if column == 3:
            reward +=50
        return reward



    def make_move(self, column: int) -> Tuple[bool, int]:
        longest_sequence = 0
        if self.board.is_valid_move(column):
            for row in range(self.BOARD_ROWS -1, -1, -1):
                if self.board.get_position((row, column)) == 0:
                    self.board.set_position((row, column), self.current_player)
                    break
            self.move_count += 1

            longest_sequence = self.is_sequence( (row, column), self.current_player, 4 )
            if longest_sequence == 4:
                self.game_over = True
                self.winner = self.current_player
            if self.move_count == self.MAX_MOVES:
                self.game_over = True
                self.draw = True
                self.winner = None

            # Switch to the other player
            self.current_player *= -1
            return (True, self.reward(longest_sequence, column))
        return (False, 0)

