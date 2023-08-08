from typing import Optional, Tuple

from Connect4Board import Connect4Board


class Connect4Game:
    DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]
    SEQUENCE_LENGTH_TO_WIN = 4

    def __init__(self) -> None:
        self.board = Connect4Board()
        self.draw: bool = False
        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.current_player: int = 1
        self.move_count: int = 0



    def can_win_next_move(self, player):
        # Check for each column if making a move there results in a win
        for column in range(self.board.BOARD_COLUMNS):
            row = self.board.first_empty_row_per_column[column]
            if row != -1:  # If the column is not full
                self.board.set_position((row, column), player)
                longest_sequence = self.has_sequence_of_length((row, column), player, self.SEQUENCE_LENGTH_TO_WIN)
                self.board.set_position((row, column), 0)  # Reset the position to its previous state
                if longest_sequence == self.SEQUENCE_LENGTH_TO_WIN:
                    return True
        return False



    def sequence_count_in_both_directions(self, start_position: Tuple[int, int], direction: Tuple[int, int],
                                          piece: int, max_desired_sequence_length: int) -> int:
        def sequence_count_in_direction(direction: Tuple[int, int]) -> int:
            if direction == (-1, 0):
                return

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



    def has_sequence_of_length(self, position: Tuple[int, int], piece: int, desired_length: int) -> int:
        for direction in self.DIRECTIONS:
            sequence_count = self.sequence_count_in_both_directions(position, direction, piece, desired_length)
            if sequence_count >= desired_length:
                return desired_length
        return 0  # Return 0 if no sequence of the desired length is found


    def make_move(self, column: int) ->  float:
        can_win_this_move = self.can_win_next_move(self.current_player)
        row = self.board.make_move(column, self.current_player)
        self.move_count += 1

        if self.move_count == Connect4Board.MAX_MOVES:
            self.game_over = True
            self.draw = True
            self.winner = None
            return self.reward(column, False, False)
        else:
            longest_sequence = self.has_sequence_of_length((row, column), self.current_player, 4)
            if longest_sequence == self.SEQUENCE_LENGTH_TO_WIN:
                self.game_over = True
                self.winner = self.current_player
                return self.reward(column, False, False)

        opponent_potential_win = self.can_win_next_move(self.other_player())
        reward = self.reward(column, can_win_this_move, opponent_potential_win)

        self.current_player = self.other_player()

        return reward

    def other_player(self):
        return self.current_player * -1

    def reward(self, column: int, could_have_won: bool, opponent_potential_win: bool) -> float:
        reward = 0.0

        if self.game_over:
            if self.winner == self.current_player:
                reward += 1  # Win
        else:
            if could_have_won:
                reward += -1
            elif opponent_potential_win:
                reward += -1  # Discouraging not blocking opponent's potential win
            elif column == 3:
                reward += 0.2  # Encouraging playing in the center
            else:
                # Calculate created_potential_win only if the previous conditions aren't met.
                created_potential_win = self.can_win_next_move(self.current_player)
                if created_potential_win:
                    reward += 0.3  # Encouraging creating a winning opportunity

        return reward