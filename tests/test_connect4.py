import unittest

from model.connect4 import Connect4


class TestConnect4(unittest.TestCase):
    def test_create_board(self) -> None:
        game = Connect4()
        self.assertEqual(len(game.board), 6)
        self.assertEqual(len(game.board[0]), 7)
        self.assertEqual(sum(sum(row) for row in game.board), 0)

    def test_valid_move(self) -> None:
        game = Connect4()
        self.assertTrue(game.is_valid_move(0))
        game.make_move(0)
        self.assertTrue(game.is_valid_move(0))
        for _ in range(5):
            game.make_move(0)
        self.assertFalse(game.is_valid_move(0))

    def test_game_over(self) -> None:
        game = Connect4()
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

    def test_check_direction(self) -> None:
        game = Connect4()
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 2, 0, 0, 0, 0, 0],
            [1, 2, 2, 0, 2, 1, 0],
            [1, 1, 2, 0, 1, 1, 0],
            [2, 2, 1, 1, 2, 1, 0],
        ]
        self.assertTrue(game.is_winner(1, 0, 1))  # Vertical win for player 1
        self.assertFalse(game.is_winner(1, 0, 2))  # No win for player 2


if __name__ == "__main__":
    unittest.main()
