import unittest

from Connect4Game import Connect4Game


class TestConnect4(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Connect4Game()

    def test_check_sequence_vertical(self) -> None:
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.assertTrue(self.game.has_sequence_of_length((4, 0), 1, 4))  # Vertical sequence for player 1

    def test_check_sequence_horizontal(self) -> None:
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 1, 1, 1, 1],
        ]
        self.assertTrue(self.game.has_sequence_of_length((5, 6), 1, 4))  # Horizontal sequence for player 1

    def test_check_sequence_diagonal(self) -> None:
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
            [0, 0, 2, 1, 0, 0, 0],
            [2, 2, 1, 1, 0, 0, 0],
        ]
        self.assertTrue(self.game.has_sequence_of_length((5, 0), 2, 3))  # Diagonal sequence for player 2

    def test_check_sequence_broken(self) -> None:
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 1, 0, 1, 1, 0, 0],
        ]
        self.assertFalse(self.game.has_sequence_of_length((5, 1), 1, 4))  # Broken sequence for player 1

    def test_check_sequence_at_edge(self) -> None:
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
        ]
        self.assertTrue(self.game.has_sequence_of_length((5, 0), 1, 4))  # Sequence at edge for player 1

    def test_check_sequence_out_of_board(self) -> None:
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
        ]
        self.assertFalse(self.game.has_sequence_of_length((5, 0), 1, 4))  # Out of board sequence for player 1

if __name__ == '__main__':
    unittest.main()
