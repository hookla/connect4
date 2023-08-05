import random
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from DQN import DQN


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.99999
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
            #print(valid_act_values)
            return valid_moves[np.argmax(valid_act_values)]


    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        #start_replay = time.time()

        minibatch = random.sample(self.memory, batch_size)
        total_loss = 0  # Initialize the total_loss to 0
        #average_loss = 0
        for state, action, reward, next_state, done in minibatch:
            state = torch.tensor(np.array(state), dtype=torch.float32)
            next_state = torch.tensor(np.array(next_state), dtype=torch.float32)
            reward = torch.tensor(np.array(reward), dtype=torch.float32)
            if not done:
                target = reward + self.gamma * torch.max(self.model(next_state)).item()
            else:
                target = reward

            current_q_values = self.model(state)
            target_q_values = current_q_values.view(1, -1)  # reshape target_f
            target = target.detach().view(1, -1)  # reshape target
            target_q_values[0][action] = target[0]
            self.optimizer.zero_grad()
            loss = self.criterion(target_q_values, self.model(state).view(1, -1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            total_loss += loss.item()  # Add the loss of this sample to the total_loss

        #average_loss = total_loss / batch_size  # Calculate the average loss

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        return average_loss


