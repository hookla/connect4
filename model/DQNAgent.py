import random
from collections import deque
from typing import Tuple, List

import torch
import torch.nn as nn
import torch.optim as optim

from DQN import DQN


class DQNAgent:
    def __init__(self, state_size: int, action_size: int, device: torch.device):
        self.state_size = state_size
        self.action_size = action_size
        self.device = device
        self.memory = deque(maxlen=20000)
        self.gamma: float = 0.95
        self.epsilon: float = 1.0
        self.epsilon_min: float = 0.1
        self.epsilon_decay: float = 0.99999
        self.learning_rate: float = 0.001
        self.model: nn.Module = DQN(self.state_size, self.action_size)
        self.model.to(self.device)
        self.optimizer: optim.Optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion: nn.Module = nn.MSELoss()


    def remember(self, state: torch.Tensor, action: int, reward: torch.Tensor, next_state: torch.Tensor, done: bool):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: torch.Tensor, game) -> int:
        if torch.rand(1).item() <= self.epsilon:
            valid_moves = torch.tensor(game.board.get_valid_moves())
            return valid_moves[torch.randint(0, len(valid_moves), (1,))].item()
        else:
            state_tensor = state.to(self.device).unsqueeze(0)  # Adds a batch dimension
            act_values = self.model(state_tensor).squeeze().detach()  # Removes batch dimension
            valid_moves = game.board.get_valid_moves()
            valid_act_values = act_values[valid_moves]
            return valid_moves[torch.argmax(valid_act_values).item()]

    def replay(self, batch_size: int) -> float:
        if len(self.memory) < batch_size:
            return 0
        minibatch: List[Tuple[torch.Tensor, int, torch.Tensor, torch.Tensor, bool]] = random.sample(self.memory, batch_size)

        # 1. Extract batches
        states, actions, rewards, next_states, dones = zip(*minibatch)
        states = torch.stack(states).to(self.device)
        actions = torch.tensor(actions, dtype=torch.long).to(self.device)  # Long tensor for indexing
        rewards = torch.tensor(rewards, dtype=torch.float).to(self.device)
        next_states = torch.stack(next_states).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float).to(self.device)

        # 2. Compute Q-values and target Q-values
        current_q_values = self.model(states).gather(1, actions.unsqueeze(-1)).squeeze(-1)
        next_q_values = self.model(next_states).max(1)[0]
        targets = rewards + (1 - dones) * self.gamma * next_q_values

        # 3. Compute the loss and backpropagate
        self.optimizer.zero_grad()
        loss = self.criterion(current_q_values, targets.detach())
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        self.optimizer.step()

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        average_loss = loss.item() / batch_size
        return average_loss


