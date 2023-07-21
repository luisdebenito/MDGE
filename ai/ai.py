import torch
import torch.nn as nn
import torch.nn.functional as F


class GameAI(nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes=[]):
        super(GameAI, self).__init__()
        sizes = [input_size] + hidden_sizes + [output_size]
        self.layers = nn.ModuleList(
            [nn.Linear(sizes[i], sizes[i + 1]) for i in range(len(sizes) - 1)]
        )

    def forward(self, x):
        for layer in self.layers[:-1]:
            x = F.relu(layer(x))
        return self.layers[-1](x)
