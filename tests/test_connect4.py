import unittest

from model.connect4 import Connect4


class TestConnect4(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Connect4()

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

    def test_check_sequence(self) -> None:
        game = Connect4()
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 2, 0, 0, 0, 0, 0],
            [1, 2, 2, 2, 2, 1, 0],
            [1, 1, 2, 0, 1, 1, 0],
            [2, 2, 1, 1, 2, 1, 0],
        ]
        self.assertTrue(game.is_sequence(1, 0, 1, 4))  # Vertical sequence of 4 for player 1
        self.assertTrue(game.is_sequence(3, 5, 1, 3))  # Horizontal sequence of 3 for player 1
        self.assertTrue(game.is_sequence(3, 4, 2, 4))  # No vertical sequence of 4 for player 2
        self.assertTrue(game.is_sequence(3, 4, 2, 3))  # No horizontal sequence of 3 for player 2
        self.assertTrue(game.is_sequence(3, 4, 2, 2))  # Horizontal sequence of 2 for player 2

def test_check_sequence_vertical(self) -> None:
    self.game.board = [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    self.assertTrue(self.game.is_sequence(4, 0, 1, 4))  # Vertical sequence for player 1


if __name__ == "__main__":
    unittest.main()
