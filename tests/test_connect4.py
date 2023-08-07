import unittest

from Connect4Game import Connect4Game


class TestConnect4(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Connect4Game()

    def test_create_board(self) -> None:
        game = Connect4Game()
        self.assertEqual(len(game.board), 6)
        self.assertEqual(len(game.board[0]), 7)
        self.assertEqual(sum(sum(row) for row in game.board), 0)

    def test_valid_move(self) -> None:
        game = Connect4Game()
        self.assertTrue(game.is_valid_move(0))
        game.make_move(0)
        self.assertTrue(game.is_valid_move(0))
        for _ in range(5):
            game.make_move(0)
        self.assertFalse(game.is_valid_move(0))

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
        game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 2, 0, 0, 0, 0, 0],
            [1, 2, 2, 2, 2, 1, 0],
            [1, 1, 2, 0, 1, 1, 0],
            [2, 2, 1, 1, 2, 1, 0],
        ]
        self.assertTrue(game.has_sequence_of_length(1, 0, 1, 4))  # Vertical sequence of 4 for player 1
        self.assertTrue(game.has_sequence_of_length(3, 5, 1, 3))  # Horizontal sequence of 3 for player 1
        self.assertTrue(game.has_sequence_of_length(3, 4, 2, 4))  # No vertical sequence of 4 for player 2
        self.assertTrue(game.has_sequence_of_length(3, 4, 2, 3))  # No horizontal sequence of 3 for player 2
        self.assertTrue(game.has_sequence_of_length(3, 4, 2, 2))  # Horizontal sequence of 2 for player 2

def test_check_sequence_vertical(self) -> None:
    self.game.board = [
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    self.assertTrue(self.game.has_sequence_of_length(4, 0, 1, 4))  # Vertical sequence for player 1


if __name__ == "__main__":
    unittest.main()
