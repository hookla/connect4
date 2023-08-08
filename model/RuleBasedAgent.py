import random

import Connect4Game

class OptimizedConnect4Agent:
    def __init__(self, game: Connect4Game):
        self.game = game

    def choose_move(self) -> int:
        valid_moves = self.game.board.get_valid_moves()

        # Check for a winning move for the agent
        for move in valid_moves:
            if self.is_winning_move(move, self.game.current_player):
                return move

        # Check for a blocking move to prevent opponent's win
        for move in valid_moves:
            if self.is_winning_move(move, self.game.other_player()):
                return move

        # Prefer the center column if available
        if 3 in valid_moves:
            return 3

        # Otherwise, choose a random move
        return random.choice(valid_moves)

    def is_winning_move(self, column: int, player: int) -> bool:
        row = self.game.board.first_empty_row_per_column[column]
        if row == -1:  # Column is full
            return False

        # Temporarily set the position
        self.game.board.set_position((row, column), player)

        # Check if this move results in a win
        win = self.game.has_sequence_of_length((row, column), player, Connect4Game.Connect4Game.SEQUENCE_LENGTH_TO_WIN )

        # Undo the move
        self.game.board.set_position((row, column), 0)

        return win

