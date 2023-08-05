import numpy as np
import torch
import wandb

from Connect4Game import Connect4Game
from DQNAgent import DQNAgent
from RandomAgent import RandomAgent

# Training loop
EPISODES = 500000
BATCH_SIZE = 32

state_size = Connect4Game.BOARD_ROWS * Connect4Game.BOARD_COLUMNS  # Assuming your state is a 1D version of the board
action_size = Connect4Game.BOARD_COLUMNS  # 7 possible actions, one for each column
agent1 = DQNAgent(state_size, action_size)
agent2 = RandomAgent()

checkpoint = torch.load(f'xxx-{100000}.weights')
agent3 = DQNAgent(state_size, action_size)
agent3.model.load_state_dict(checkpoint['model_state_dict'])
agent3.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
print(f'loaded episode {100000} checkpoint into agent3')

agents = [agent1, agent3]

wandb.init(
    # set the wandb project where this run will be logged
    project="connect4",

)


for e in range(EPISODES):
    if e > 1 and e%100000 == 1:
        checkpoint = torch.load(f'xxx-{100000}.weights')
        agent2 = DQNAgent(state_size, action_size)
        agent2.model.load_state_dict(checkpoint['model_state_dict'])
        agent2.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        print(f'loaded episode {e-1} checkpoint into agent2')

    game = Connect4Game()
    state = np.array(game.board.get_state())
    agent1_win = 0
    this_game_reward = 0  # Reset cumulative rewards at the start of each episode
    while not game.game_over:
        for agent_number, agent in enumerate(agents, start=1):
            action = agent.act(state, game)
            reward = game.make_move(action)  # Assuming make_move now returns a reward
            next_state = np.array(game.board.board).reshape(-1)

            # Accumulate rewards
            if agent_number == 1:
                this_game_reward += reward
                agent.remember(state, action, reward, next_state, game.game_over)

            if game.game_over:
                if game.winner == 1:
                    agent1_win = 1
                if agent_number == 2:
                    agent1.remember(state, action, -reward, next_state, game.game_over)
                break
            state = next_state

    # Save rewards and calculate running averages

    average_loss = agent1.replay(BATCH_SIZE)  # Training the agent after each game
    wandb.log({"this_game_reward": this_game_reward, "agent1_win": agent1_win, "average_loss": average_loss, "agent1.epsilon": agent1.epsilon})

    if e%100 == 0:
        game.board.print_board()
        print(f"episode {e}, winner {game.winner}, loss {average_loss}, reward {this_game_reward}, agent1.epsilon {agent1.epsilon}")

    if e%5000 == 0:
        # Save the model and optimizer
        print(f"saving model episode {e}")
        torch.save({
            'model_state_dict': agent1.model.state_dict(),
            'optimizer_state_dict': agent1.optimizer.state_dict(),
        }, f'xxx-{e}.weights')

