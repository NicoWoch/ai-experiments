import torch
from torch import Tensor, nn, optim
from torch.nn import functional as F
import os


class LinearQNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: list[int], output_size: int):
        super().__init__()
        assert len(hidden_size) >= 1
        
        self.input_layer = nn.Linear(input_size, hidden_size[0])
        self.layers = [
            nn.Linear(hidden_size[i], hidden_size[i + 1])
            for i in range(len(hidden_size) - 1)
        ]
        self.output_layer = nn.Linear(hidden_size[-1], output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.input_layer(x))
        
        for layer in self.layers:
            x = F.relu(layer(x))
        
        x = self.output_layer(x)
        return x

    def save(self, file_path: str = "model.pth") -> None:
        parent_dir = os.path.dirname(file_path)
        
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        torch.save(self.state_dict(), file_path)


class QTrainer:
    def __init__(self, model: nn.Module, lr: float, gamma: float):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def train_step(
        self, states: Tensor, actions: Tensor,
        rewards: Tensor, next_states: Tensor, dones: Tensor
    ):
        pred = self.model(states)

        target = pred.detach().clone()
        for idx in range(len(dones)):
            q_new = rewards[idx]

            if not dones[idx]:
                with torch.no_grad():
                    q_new = rewards[idx] + self.gamma * torch.max(self.model(next_states[idx]))

            target[idx][torch.argmax(actions[idx]).item()] = q_new

        self.optimizer.zero_grad()

        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()


