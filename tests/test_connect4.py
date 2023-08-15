import unittest

import numpy as np

from Connect4Game import Connect4Game


class TestConnect4(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Connect4Game()

    def test_create_board(self) -> None:
        game = Connect4Game()
        self.assertEqual(game.board._board.shape[0], 6)
        self.assertEqual(game.board._board.shape[1], 7)
        self.assertTrue(np.all(game.board._board == 0))

    def test_valid_move(self) -> None:
        game = Connect4Game()
        self.assertTrue(game.board.is_valid_move(0))
        game.make_move(0)
        self.assertTrue(game.board.is_valid_move(0))
        for _ in range(5):
            game.make_move(0)
        self.assertFalse(game.board.is_valid_move(0))

    def test_game_over(self) -> None:
        game = Connect4Game()
        self.assertFalse(game.game_over)
        game.make_move(0)
        game.make_move(1)
        game.make_move(0)
        game.make_move(1)
        game.make_move(0)
        game.make_move(1)
        game.make_move(0)
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, 1)

    def test_check_sequence(self) -> None:
        game = Connect4Game()
        game.board.set_board_state(np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 2, 0, 0, 0, 0, 0],
            [1, 2, 2, 2, 2, 1, 0],
            [1, 1, 2, 0, 1, 1, 0],
            [2, 2, 1, 1, 2, 1, 0]
        ]))

        self.assertTrue(game.has_sequence_of_length((1, 0), 1, 4))  # Vertical sequence of 4 for player 1
        self.assertTrue(game.has_sequence_of_length((3, 4), 2, 4))  # No vertical sequence of 4 for player 2

if __name__ == "__main__":
    unittest.main()
