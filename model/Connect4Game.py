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



    def can_win_next_move(self, player):
        # Check for each column if making a move there results in a win
        for column in range(self.BOARD_COLUMNS):
            for row in range(self.BOARD_ROWS - 1, -1, -1):
                if self.board.get_position((row, column)) == 0:
                    self.board.set_position((row, column), player)
                    longest_sequence = self.has_sequence_of_length((row, column), player, 4)
                    self.board.set_position((row, column), 0)  # Reset the position to its previous state
                    if longest_sequence == 4:
                        return True
        return False


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
                if not self.board.is_valid_position(new_position) or self.board.get_position(new_position) != piece:
                    break
                count += 1
            return count

        # Count sequences in both the direction and its opposite
        sequence_count = sequence_count_in_direction(direction) + sequence_count_in_direction((-direction[0], -direction[1])) - 1

        return sequence_count


    def has_sequence_of_length(self, position: Tuple[int, int], piece: int, max_desired_sequence_length: int) -> int:
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



    def make_move(self, column: int) ->  float:
        longest_sequence = 0
        row = self.board.make_move(column, self.current_player)
        self.move_count += 1


        if self.move_count == self.MAX_MOVES:
            self.game_over = True
            self.draw = True
            self.winner = None
        else:
            longest_sequence = self.has_sequence_of_length((row, column), self.current_player, 4)
            if longest_sequence == 4:
                self.game_over = True
                self.winner = self.current_player

        # Switch to the other player
        opponent = self.current_player * -1
        opponent_potential_win = self.can_win_next_move(opponent)
        reward = self.reward(longest_sequence, column, opponent_potential_win)

        self.current_player = opponent
        return reward



    def reward(self, longest_sequence: int, column: int, opponent_potential_win: bool) -> float:
        reward = 0.0
        if self.game_over:
            pass
            if self.winner == self.current_player:
                 reward += 1  # Win

        else:
            if opponent_potential_win:
                reward -= 1  # Discouraging not blocking opponent's potential win
            elif column == 3:
                reward += 0.2  # Encouraging playing in the center
        return reward

    def reward2(self, position: Tuple[int, int], column: int) -> float:
        reward = 0.0

        if self.game_over:
            if self.winner == self.current_player:
                reward += 1  # Win
        else:
            # Calculate opponent_potential_win first.
            opponent_potential_win = self.can_win_next_move(self.current_player * -1)
            if opponent_potential_win:
                reward -= 1  # Discouraging not blocking opponent's potential win
            elif column == 3:
                reward += 0.2  # Encouraging playing in the center
            else:
                # Calculate created_potential_win only if the previous conditions aren't met.
                created_potential_win = self.can_win_next_move(self.current_player)
                if created_potential_win:
                    reward += 0.3  # Encouraging creating a winning opportunity

        return reward