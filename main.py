import numpy as np
import torch

from model.Connect4Board import Connect4Board
from model.Connect4Game import Connect4Game
from model.RuleBasedAgent import RuleBasedAgent

state_size = Connect4Board.BOARD_ROWS * Connect4Board.BOARD_COLUMNS  # Assuming your state is a 1D version of the board
action_size = Connect4Board.BOARD_COLUMNS  # 7 possible actions, one for each column

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"cuda available : {torch.cuda.is_available()} ")

player1_win_count = 0
player2_win_count = 0
draw_count = 0


def get_user_move():
    while True:
        user_input = input("Enter a column (1-7) or 'q' to quit: ").strip()

        # Allow the user to quit
        if user_input.lower() == 'q':
            print("Thanks for playing!")
            return None

        # Validate the input
        try:
            move = int(user_input) - 1
            if 0 <= move <= 6:
                return move
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7 or 'q' to quit.")

# Test the function
# move_enhanced = get_user_move_enhanced()
# move_enhanced


def jumbotron(message):
    # Calculate the padding length based on the message length
    padding_length = len(message) + 10  # 10 accounts for extra spaces and characters around the message
    border = '═' * padding_length

    # Print the message with the dynamic padding
    print(f'╔{border}╗')
    print(f'║ *** {message} ***  ║')
    print(f'╚{border}╝')



def play_game() -> None:
    global player1_win_count, player2_win_count, draw_count  # Specify that we're using the global variables

    jumbotron("NEW GAME")

    game = Connect4Game()

    # checkpoint = torch.load(f'model/xxx-10000.weights')
    # agent = DQNAgent(state_size, action_size, device)
    # agent.model.load_state_dict(checkpoint['model_state_dict'])
    # agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    # agent.model.eval()  # Set model to evaluation mode

    agent = RuleBasedAgent(game)
    agent2 = RuleBasedAgent(game)

    while not game.game_over:
        # print(game.board.visualize())
        state = np.array(game.board.get_state())  # Get the current state

        if game.current_player == 1:  # Human player
            #while move not in game.board.get_valid_moves():
                #move = get_user_move()
            move = agent2.act(state, game)  # Let the agent choose a move
        else:  # AI player
            move = agent.act(state, game)  # Let the agent choose a move
        reward = game.make_move(move)
        # print({f"player {game.other_player()} played column {move+1}.  reward for player {game.other_player()} : {reward}"})


    print(game.board.visualize())

    if game.winner is not None:
        if game.winner == 1:
            jumbotron("Player 1 wins!")
            player1_win_count += 1
        else:
            jumbotron("Player 2 wins!")
            player2_win_count += 1


    else:
        print("The game is a draw.")
        draw_count += 1

    print(f"Win counts: Player 1: {player1_win_count}, Player 2: {player2_win_count}, Draws: {draw_count}")





# Call the function to play a game
if __name__ == "__main__":
    while True:(
        play_game())

