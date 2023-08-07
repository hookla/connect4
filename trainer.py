import torch
from colorama import Fore, Style

import wandb
from Connect4Game import Connect4Game
from DQNAgent import DQNAgent


def generate_markdown_table(actions):
    # Define header
    # Define header
    header = f"{Fore.CYAN}{'Player':<10}{'Move':<15}{'Action':<10}{'Reward':<10}{Style.RESET_ALL}\n"
    header += "-" * 45  # This is for the line separator

    # Print the header
    print(header)

    for idx, action in enumerate(actions):
        # Agent 1 (Red) and Agent 2 (Yellow)
        agent_disc = f"{Fore.RED}● {Style.RESET_ALL}" if action[0] == 1 else f"{Fore.YELLOW}● {Style.RESET_ALL}"
        line = f"{agent_disc:<10}{str(idx):<15}{str(action[1]):<10}{str(action[2]):<10}"
        print(line)


def play_game(e):
    game = Connect4Game()
    state = torch.FloatTensor(game.board.get_state())
    agent1_win_count = 0
    game_reward = 0
    actions = []
    while not game.game_over:
        for agent_number, agent in enumerate(agents, start=1):
            action = agent.act(state, game)
            reward = game.make_move(action)
            next_state = torch.FloatTensor(game.board.get_state())
            actions.append((agent_number,action,reward))

            if agent_number == 1:
                game_reward += reward.item() if isinstance(reward, torch.Tensor) else reward  # Convert tensor to scalar if needed
                agent.remember(state, action, reward, next_state, game.game_over)

            if game.game_over:
                if game.winner == 1:
                    agent1_win_count = 1
                if agent_number == 2:
                    agent1.remember(state, action, -reward, next_state, game.game_over)
                break
            state = next_state

    average_loss = 0
    for _ in range(10):
        average_loss += agent.replay(BATCH_SIZE)
    average_loss = average_loss / 10

    wandb.log({"game_reward": game_reward, "agent1_win_count": agent1_win_count, "average_loss": average_loss, "agent1.epsilon": agent1.epsilon})

    if e%1000 == 0:
        game.board.print_board()
        print(generate_markdown_table(actions))
        print(f"episode {e}, winner {game.winner}, loss {average_loss}, reward {game_reward}, agent1.epsilon {agent1.epsilon}")

    if e%50000 == 0 and e > 1:
        # Save the model and optimizer
        print(f"saving model episode {e}")
        torch.save({
            'model_state_dict': agent1.model.state_dict(),
            'optimizer_state_dict': agent1.optimizer.state_dict(),
        }, f'xxx-{e}.weights')


# Training loop
EPISODES = 500000000
BATCH_SIZE = 4096

state_size = Connect4Game.BOARD_ROWS * Connect4Game.BOARD_COLUMNS  # Assuming your state is a 1D version of the board
action_size = Connect4Game.BOARD_COLUMNS  # 7 possible actions, one for each column
#agent2 = RandomAgent()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"cuda available : {torch.cuda.is_available()} ")


pretrained_agent_weights_path = "xxx-495000.weights"
pretrained_agent_weights = torch.load(pretrained_agent_weights_path)
agent1 = DQNAgent(state_size, action_size, device)
agent1.model.load_state_dict(pretrained_agent_weights['model_state_dict'])
agent1.optimizer.load_state_dict(pretrained_agent_weights['optimizer_state_dict'])
print(f'loaded pre trained agent  {pretrained_agent_weights_path} checkpoint into agent1')

agent2 = DQNAgent(state_size, action_size, device)
agent2.model.load_state_dict(pretrained_agent_weights['model_state_dict'])
agent2.optimizer.load_state_dict(pretrained_agent_weights['optimizer_state_dict'])
print(f'loaded pre trained agent  {pretrained_agent_weights_path} checkpoint into agent2')



agents = [agent1, agent2]

wandb.init(
    # set the wandb project where this run will be logged
    project="connect4",
)

for e in range(EPISODES):
    play_game(e)

