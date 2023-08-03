import random


class RandomAgent:
    def __init__(self):
        pass

    def act(self,state, game):
        return random.choice(game.board.get_valid_moves())
