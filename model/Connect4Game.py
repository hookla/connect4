from enum import Enum
from typing import Optional, Tuple, List

from .Connect4Board import Connect4Board


class Direction(Enum):
    VERTICAL = (1, 0)
    HORIZONTAL = (0, 1)
    DIAGONAL_UP = (1, 1)
    DIAGONAL_DOWN = (1, -1)


class Connect4Game:

    DIRECTIONS = [Direction.VERTICAL.value, Direction.HORIZONTAL.value, Direction.DIAGONAL_UP.value, Direction.DIAGONAL_DOWN.value]

    SEQUENCE_LENGTH_TO_WIN = 4

    def __init__(self) -> None:
        self.board = Connect4Board()
        self.draw: bool = False
        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.current_player: int = 1
        self.move_count: int = 0
        self.winning_moves_player_1 = []
        self.winning_moves_player_2 = []
        self.last_move_player_1: int = -1
        self.last_move_player_2: int = -1

    def other_player(self):
        return self.current_player * -1

    def get_winning_moves_if_possible(self, player, stop_at_first=False) -> List[int]:
        winning_moves = []

        # Check for each column if making a move there results in a win
        for column in self.board.get_valid_moves():
            row = self.board.get_first_empty_row(column)
            self.board.make_move(column, player)
            if self.has_sequence_of_length((row, column), player, self.SEQUENCE_LENGTH_TO_WIN):
                winning_moves.append(column)
                if stop_at_first:
                    self.board.undo_last_move()
                    break
            self.board.undo_last_move()

        winning_moves.append(-1)
        return winning_moves

    def sequence_count_in_both_directions(self, start_position: Tuple[int, int], direction: Direction,
                                          piece: int, max_desired_sequence_length: int) -> int:
        def sequence_count_in_direction(direction: Direction) -> int:
            if direction == (-1, 0):
                return 0
            if direction == (1, 0) and start_position[0] > 6 - max_desired_sequence_length:
                return 0
            if direction == (1, 1) and start_position not in [(5, 4), (5, 5), (5, 6), (4, 4), (4, 5), (3, 6)]:
                return 0
            if direction == (1, -1) and start_position not in [(5, 0), (5, 1), (5, 2), (4, 0), (4, 1), (3, 0)]:
                return 0
            count = 0
            for offset in range(1, max_desired_sequence_length):  # Updated range
                new_position = (
                    start_position[0] + direction[0] * offset,
                    start_position[1] + direction[1] * offset,
                )

                if not self.board.is_valid_position(new_position) or self.board.get_position(new_position) != piece:
                    break
                count += 1
            return count

        # Count sequences in the initial direction
        sequence_count = sequence_count_in_direction(direction)

        # If the sequence count from the initial direction is not the desired length, check the opposite direction
        if sequence_count < max_desired_sequence_length -1:
            sequence_count += sequence_count_in_direction((-direction[0], -direction[1]))

        return sequence_count +1

    def has_sequence_of_length(self, position: Tuple[int, int], piece: int, desired_length: int) -> bool:
        for direction in self.DIRECTIONS:
            sequence_count = self.sequence_count_in_both_directions(position, direction, piece, desired_length)
            if sequence_count >= desired_length:
                return True
        return False  # Return 0 if no sequence of the desired length is found

    def make_move(self, column: int) -> float:
        winning_move_current_player = self.get_winning_moves_if_possible(self.current_player)

        _ = self.board.make_move(column, self.current_player)

        if self.current_player == 1:
            self.last_move_player_1 = column
        else:
            self.last_move_player_2 = column

        self.move_count += 1

        if column in winning_move_current_player:
            self.game_over = True
            self.winner = self.current_player
            return self.reward(column, True, False)
        elif self.move_count == Connect4Board.MAX_MOVES:
            self.game_over = True
            self.draw = True
            self.winner = None
            return self.reward(column, False, False)

        winning_move_opponent = self.get_winning_moves_if_possible(self.other_player(), True)[0]
        reward = self.reward(column, winning_move_current_player[0], winning_move_opponent)

        self.current_player = self.other_player()

        return reward

    def reward(self, column: int, winning_move_current_player: int, winning_move_opponent: int) -> float:
        reward = 0.0

        if winning_move_current_player == column:
            reward += 1  # Win
        elif winning_move_opponent != -1 and winning_move_opponent == column:
                reward += 0.6  # encourage blocking opponent's potential win
        elif self.opponent_can_make_compound_threat():
                reward -= 1  # Discourage letting opponent create a compound threat
        elif column == 3:
                reward += 0.2  # Encouraging playing in the center
        else:
                # Calculate created_potential_win only if the previous conditions aren't met.
                if True if self.get_winning_moves_if_possible(self.current_player)[0] != -1 else False:
                    reward += 0.3  # Encouraging creating a threat
                if True if self.get_winning_moves_if_possible(self.other_player())[0] != -1 else False:
                    reward -= 0.3  # Discourage letting opponent create a threat

        return reward

    def opponent_can_make_compound_threat(self):
        for column in self.board.get_valid_moves():
            self.board.make_move(column, self.other_player())
            threat_moves = self.get_winning_moves_if_possible(self.other_player())
            if len(threat_moves)>2:
                self.board.undo_last_move()
                return True
            self.board.undo_last_move()
        return False
