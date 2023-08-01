import random
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from Connect4Game import Connect4Game


class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, output_dim)
        )

    def forward(self, x):
        return self.network(x)

class RandomAgent:
    def __init__(self, action_size):
        self.action_size = action_size

    def act(self, state, game: Connect4Game):
        return random.choice(game.board.get_valid_moves())


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = DQN(self.state_size, self.action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, game):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(game.board.get_valid_moves())
        else:
            state_tensor = torch.tensor(np.array([state]), dtype=torch.float32)
            act_values = self.model(state_tensor).detach().numpy().flatten()
            valid_moves = game.board.get_valid_moves()
            valid_act_values = [act_values[i] for i in valid_moves]
            return valid_moves[np.argmax(valid_act_values)]

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = torch.tensor(np.array(state), dtype=torch.float32)
            next_state = torch.tensor(np.array(next_state), dtype=torch.float32)
            reward = torch.tensor(np.array(reward), dtype=torch.float32)
            if not done:
                target = reward + self.gamma * torch.max(self.model(next_state)).item()
            else:
                target = reward

            target_f = self.model(state)
            target_f = target_f.view(1, -1)  # reshape target_f
            target = target.detach().view(1, -1)  # reshape target
            target_f[0][action] = target[0]

            self.optimizer.zero_grad()
            loss = self.criterion(target_f, self.model(state).view(1, -1))
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay




# Training loop
EPISODES = 500000
BATCH_SIZE = 32

state_size = Connect4Game.BOARD_ROWS * Connect4Game.BOARD_COLUMNS  # Assuming your state is a 1D version of the board
action_size = Connect4Game.BOARD_COLUMNS  # 7 possible actions, one for each column
agent1 = DQNAgent(state_size, action_size)
agent2 = RandomAgent(action_size)
agents = [agent1, agent2]

# Load the model and optimizer
#checkpoint = torch.load('xxx.weights')
#agent1.model.load_state_dict(checkpoint['model_state_dict'])
#agent1.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
#print('loaded checkpoint')



# Initialize lists to store the rewards and running averages
rewards1, rewards2, running_avg_rewards1, running_avg_rewards2 = [], [], [], []
agent1_win_count = 0

for e in range(EPISODES):

    game = Connect4Game()
    state = np.array(game.board.get_state())
    done = False
    cumulative_reward1, cumulative_reward2 = 0, 0  # Reset cumulative rewards at the start of each episode
    while not done:
        for agent_number, agent in enumerate(agents, start=1):
            action = agent.act(state, game)
            reward = game.make_move(action)  # Assuming make_move now returns a reward
            # Accumulate rewards
            if agent_number == 1:
                cumulative_reward1 += reward
            else:
                cumulative_reward2 += reward
            done = game.game_over
            next_state = np.array(game.board.board).reshape(-1)
            if agent_number == 1:
                agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                #game.board.print_board()
                if game.winner == 1:
                    agent1_win_count +=1

                cumulative_reward1 += reward
                break
    # Save rewards and calculate running averages
    rewards1.append(cumulative_reward1)
    rewards2.append(cumulative_reward2)
    running_avg_rewards1.append(np.mean(rewards1[max(0, e-100):e+1]))  # Calculate running average over last 100 episodes
    running_avg_rewards2.append(np.mean(rewards2[max(0, e-100):e+1]))  # Calculate running average over last 100 episodes

    if e%100 == 0:
        print(f"Episode {e}/{EPISODES}")
        print(f"Average reward for Agent 1 in this episode: {cumulative_reward1}, Running average: {running_avg_rewards1[-1]}")
        print(f"Average reward for Agent 2 in this episode: {cumulative_reward2}, Running average: {running_avg_rewards2[-1]}")
        print(f"Agent 1 win count: {agent1_win_count}. average {agent1_win_count / 100 }")
        game.board.print_board()
        agent1_win_count = 0
    agent1.replay(BATCH_SIZE)  # Training the agent after each game
    #agent2.replay(BATCH_SIZE)  # Training the agent after each game





    if e%1000 == 0 and agent_number == 1:
        # Save the model and optimizer
        print("saving model")
        torch.save({
            'model_state_dict': agent.model.state_dict(),
            'optimizer_state_dict': agent.optimizer.state_dict(),
        }, 'xxx.weights')
        # Assuming rewards is a list of rewards obtained per episode
        plt.plot(rewards1)
        plt.ylabel('Reward per episode')
        plt.xlabel('Episode')
        plt.show()
