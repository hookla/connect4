import random

import Connect4Game


class RuleBasedAgent:
    def __init__(self, game: Connect4Game):
        self.game = game

    def act(self, __, ___) -> int:
        return self.choose_move()

    def choose_move(self) -> int:
        # this time it will try every possible move and choose the one that gives the best reward and log the reward for each move
        rewards = []
        valid_moves = self.game.board.get_valid_moves()
        winning_moves_current_player = self.game.get_winning_moves_if_possible(self.game.current_player)
        winning_moves_opponent = self.game.get_winning_moves_if_possible(self.game.other_player(), True)

        for move in valid_moves:
            self.game.board.make_move(move, self.game.current_player)
            rewards.append(self.game.reward(move, move if move in winning_moves_current_player else -1,  move if move in winning_moves_opponent else -1))
            self.game.board.undo_last_move()
        # logger.info(f"rewards for each move: {rewards}")

        # Find the maximum reward value
        max_reward = max(rewards)

        # Create a list of all moves with that maximum reward value
        best_moves = [move for move, reward in zip(valid_moves, rewards) if reward == max_reward]

        # Return a random choice from the best moves
        return random.choice(best_moves)

