from Connect4Game import Connect4Game


def play_game() -> None:
    game = Connect4Game()
    while not game.game_over:
        # Print the current game state
        game.board.print_board()
        print(f"Player {1 if game.current_player == 1 else 2}'s turn.")
        move = -1
        while move not in game.board.get_valid_moves():
            move = int(input("Enter a column (0-6): "))
        game.make_move(move)
    game.board.print_board()
    if game.winner is not None:
        print(f"Player {1 if game.winner == 1 else 2} wins!")
    else:
        print("The game is a draw.")


# Call the function to play a game
if __name__ == "__main__":
    play_game()
