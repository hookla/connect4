import numpy as np

from Connect4Game import Connect4Game
from RuleBasedAgent import RuleBasedAgent

board_template = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])

def test_agent_winning_move():
    game = Connect4Game()
    game.board.set_board_state(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0],
        [1, -1, -1, -1, 1, -1, 1],
        [-1, 1, 1, 1, -1, 1, -1],
    ]))
    agent = RuleBasedAgent(game)
    move = agent.choose_move()
    assert move == 3, f"Expected move 3, got {move}"

def test_agent_blocking_opponent_win():
    game2 = Connect4Game()
    game2.board.set_board_state(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, 0, 0, 0, 0],
        [1, -1, -1, 1, 1, -1, 1],
        [-1, 1, 1, 1, -1, 1, -1],
    ]))
    agent2 = RuleBasedAgent(game2)
    move2 = agent2.choose_move()
    assert move2 == 3, f"Expected move 3, got {move2}"

def test_agent_prefers_center_column():
    game3 = Connect4Game()
    game3.board.set_board_state(np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, -1, -1, 0, 1, -1, 1],
        [-1, 1, 1, 1, -1, 1, -1],
    ]))
    agent3 = RuleBasedAgent(game3)
    move3 = agent3.choose_move()
    assert move3 == 3, f"Expected move 3, got {move3}"

def test_agent_random_move_when_center_full():
    game4 = Connect4Game()
    game4.board.set_board_state(np.array([
        [1, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, -1, 0, 0, 0],
        [-1, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, -1, 0, 0, 0],
        [-1, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, -1, 0, 0, 0],
    ]))
    agent4 = RuleBasedAgent(game4)
    move4 = agent4.choose_move()
    assert move4 in game4.board.get_valid_moves(), f"Expected one of {game4.board.get_valid_moves()}, got {move4}"


def test_agent_blocks_threat():
    game = Connect4Game()

    scenario_board = np.array([
        [0, 2, 0, 2, 1, 0, 1],
        [0, 1, 0, 1, 2, 0, 2],
        [1, 2, 0, 2, 2, 1, 2],
        [2, 1, 0, 1, 1, 1, 2],
        [1, 1, 2, 2, 1, 2, 1],
        [2, 1, 2, 1, 1, 2, 2],
    ])
    scenario_board[scenario_board == 2] = -1
    game.board.set_board_state(scenario_board)

    agent = RuleBasedAgent(game)
    game.current_player = -1
    move = agent.choose_move()
    expected = 2
    print(game.board.visualize())

    assert move == expected, f"Expected move {expected}, got {move}"


def test_agent_blocks_compound_threat():
    game = Connect4Game()

    scenario_board = np.array([
        [3, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 2, 0, 0, 0],
        [3, 0, 0, 1, 1, 0, 0],
    ])
    scenario_board[scenario_board == 2] = -1
    game.board.set_board_state(scenario_board)

    agent = RuleBasedAgent(game)
    game.current_player = -1
    move = agent.choose_move()
    expected = [2,5]
    print(game.board.visualize())

    assert move in expected, f"Expected move {expected}, got {move}"