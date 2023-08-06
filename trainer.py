import torch
import torch

import wandb
from Connect4Game import Connect4Game
from DQNAgent import DQNAgent


def play_game(e):
    # if e > 1 and e%100000 == 1:
    #     checkpoint = torch.load(f'xxx-{e-1}.weights')
    #     agent2 = DQNAgent(state_size, action_size)
    #     agent2.model.load_state_dict(checkpoint['model_state_dict'])
    #     agent2.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    #     print(f'loaded episode {e-1} checkpoint into agent2')
    game = Connect4Game()
    state = torch.tensor(game.board.get_state(), dtype=torch.float).to_device(device)
    agent1_win_count = 0
    game_reward = 0  # Reset cumulative rewards at the start of each episode
    actions = []
    while not game.game_over:
        for agent_number, agent in enumerate(agents, start=1):
            action = agent.act(state, game)
            reward = game.make_move(action)  # Assuming make_move now returns a reward
            next_state = torch.tensor(game.board.board, dtype=torch.float).reshape(-1).to_device(device)
            actions.append((action,reward))
            # Accumulate rewards
            if agent_number == 1:
                game_reward += reward
                agent.remember(state, action, reward, next_state, game.game_over)

            if game.game_over:
                if game.winner == 1:
                    agent1_win_count = 1
                if agent_number == 2:
                    agent1.remember(state, action, -reward, next_state, game.game_over)
                break
            state = next_state

    # Save rewards and calculate running averages

    average_loss = agent1.replay(BATCH_SIZE)  # Training the agent after each game
    wandb.log({"game_reward": game_reward, "agent1_win_count": agent1_win_count, "average_loss": average_loss, "agent1.epsilon": agent1.epsilon})
    if e%100 == 0:
        game.board.print_board()
        print(actions)
        print(f"episode {e}, winner {game.winner}, loss {average_loss}, reward {game_reward}, agent1.epsilon {agent1.epsilon}")

    # if e%5000 == 0 and 1==0:
    #     # Save the model and optimizer
    #     print(f"saving model episode {e}")
    #     torch.save({
    #         'model_state_dict': agent1.model.state_dict(),
    #         'optimizer_state_dict': agent1.optimizer.state_dict(),
    #     }, f'xxx-{e}.weights')


# Training loop
EPISODES = 500000
BATCH_SIZE = 32

state_size = Connect4Game.BOARD_ROWS * Connect4Game.BOARD_COLUMNS  # Assuming your state is a 1D version of the board
action_size = Connect4Game.BOARD_COLUMNS  # 7 possible actions, one for each column
#agent2 = RandomAgent()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
(f"cuda available : {torch.cuda.is_available()} ")


pretrained_agent_weights_path = "xxx-495000.weights"
pretrained_agent_weights = torch.load(pretrained_agent_weights_path)
agent1 = DQNAgent(state_size, action_size).to_device(device)
agent1.model.load_state_dict(pretrained_agent_weights['model_state_dict'])
agent1.optimizer.load_state_dict(pretrained_agent_weights['optimizer_state_dict'])
print(f'loaded pre trained agent  {pretrained_agent_weights_path} checkpoint into agent1')

agent2 = DQNAgent(state_size, action_size).to_device(device)
agent2.model.load_state_dict(pretrained_agent_weights['model_state_dict'])
agent2.optimizer.load_state_dict(pretrained_agent_weights['optimizer_state_dict'])
print(f'loaded pre trained agent  {pretrained_agent_weights_path} checkpoint into agent2')



agents = [agent1, agent2]

wandb.init(
    # set the wandb project where this run will be logged
    project="connect4",
)

print
#with Pool(processes=3) as pool:
#    results = pool.map(play_game, range(EPISODES))

for e in range(EPISODES):
    play_game(e)

