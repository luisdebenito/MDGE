import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random

from src.ball import PlayerBall, EnemyBall
from typing import List

# the chosen algorithm is going to be Deep Q-Network (DQN)


class Transition:
    def __init__(self, state, action, reward, next_state, done):
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state
        self.done = done


class Action:
    # example: left (0, -1), up & right (1, 1), down & right (-1, 1)
    def __init__(self, rm: tuple, lm: tuple) -> None:
        self.movLeft: tuple = rm
        self.movRight: tuple = lm


class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, hidden_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class AI:
    def __init__(self):
        self.input_size = (2 * 3) + 1 + (28 * 3)
        self.output_size = 4
        self.hidden_size = 64
        self.lr = 0.001
        self.gamma = 0.99
        self.epsilon = 0.1

        self.q_network = QNetwork(self.input_size, self.output_size, self.hidden_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.lr)

        self.memory = []
        self.generation = 0

    def _get_GameAction(
        self,
        playerR: PlayerBall,
        playerL: PlayerBall,
        enemies: List[EnemyBall],
        score: int,
    ) -> Action:
        # Implement the game state into a tensor
        _myL = self._get_State_List(playerR, playerL, enemies, score)
        state = torch.tensor(
            _myL,
            dtype=torch.float,
        ).unsqueeze(0)

        # Pass the state through the QNetwork
        q_values = self.q_network(state)

        # Convert Q-values to action
        action = self._select_action(q_values)

        return action

    def _get_State_List(
        self, playerR: PlayerBall, playerL: PlayerBall, enemies: List[EnemyBall], score
    ) -> List[float]:
        _myL = [
            playerR.position.posx,
            playerR.position.posy,
            playerR.rad,
            playerL.position.posx,
            playerL.position.posy,
            playerL.rad,
            score,
        ]

        # Extract enemy information and include it in the state
        for i in range(28):
            var1 = 0
            var2 = 0
            var3 = 0
            if len(enemies) - 1 >= i and enemies[i]:
                var1 = enemies[i].position.posx
                var2 = enemies[i].position.posy
                var3 = enemies[i].speed

            _myL += [var1, var2, var3]

        return _myL

    def _select_action(self, q_values):
        # Epsilon-greedy exploration strategy
        if random.random() < self.epsilon:
            # Randomly select an action
            ac = Action(
                (random.randint(-1, 1), random.randint(-1, 1)),
                (random.randint(-1, 1), random.randint(-1, 1)),
            )
        else:
            # Choose the action with the highest Q-value
            action_idx = torch.argmax(q_values)
            ac = Action(
                (action_idx.item(), action_idx.item()),
                (action_idx.item(), action_idx.item()),
            )
        return ac

    def update_network(self):
        # Sample a mini-batch from the replay memory
        transitions = random.sample(self.memory, 32)
        batch = Transition(*zip(*transitions))

        # Convert the batch data to tensors
        state_batch = torch.tensor(batch.state, dtype=torch.float)
        action_batch = torch.tensor(batch.action, dtype=torch.long)
        reward_batch = torch.tensor(batch.reward, dtype=torch.float)
        next_state_batch = torch.tensor(batch.next_state, dtype=torch.float)
        done_batch = torch.tensor(batch.done, dtype=torch.float)

        # Normalize the state batch
        state_batch = self.q_network.normalize_state(state_batch)
        next_state_batch = self.q_network.normalize_state(next_state_batch)

        # Calculate Q-values for the current state
        q_values = self.q_network(state_batch)

        # Calculate Q-values for the next state
        next_q_values = self.q_network(next_state_batch)

        # Get the Q-values for the selected actions
        q_values = q_values.gather(1, action_batch.unsqueeze(1)).squeeze(1)

        # Calculate the target Q-values using the Bellman equation
        target_q_values = reward_batch + self.gamma * next_q_values.max(1)[0] * (
            1 - done_batch
        )

        # Calculate the loss (Mean Squared Error)
        loss = F.mse_loss(q_values, target_q_values)

        # Optimize the network
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
