import numpy as np
import torch

from Connect4Game import Connect4Game
from DQNAgent import DQNAgent  # assuming you have such a class

state_size = Connect4Game.BOARD_ROWS * Connect4Game.BOARD_COLUMNS  # Assuming your state is a 1D version of the board
action_size = Connect4Game.BOARD_COLUMNS  # 7 possible actions, one for each column

def play_game() -> None:
    game = Connect4Game()

    checkpoint = torch.load(f'xxx-10000.weights')
    agent = DQNAgent(state_size, action_size)
    agent.model.load_state_dict(checkpoint['model_state_dict'])
    agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    agent.model.eval()  # Set model to evaluation mode

    while not game.game_over:
        game.board.print_board()

        if game.current_player == 1:  # Human player
            print("Player 1's turn.")
            move = -1
            while move not in game.board.get_valid_moves():
                move = int(input("Enter a column (0-6): "))
        else:  # AI player
            print("Player 2's turn.")
            state = np.array(game.board.get_state())  # Get the current state
            move = agent.act(state, game)  # Let the agent choose a move

        game.make_move(move)

    game.board.print_board()

    if game.winner is not None:
        print(f"Player {1 if game.winner == 1 else 2} wins!")
    else:
        print("The game is a draw.")

# Call the function to play a game
if __name__ == "__main__":
    play_game()

