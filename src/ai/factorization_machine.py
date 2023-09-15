import torch
import numpy as np
import torch.nn as nn


class FactorizationMachineModel(nn.Module):
    def __init__(self, num_feats, embed_dim, output_dim=1, reduce_sum=True, sigmoid=True, weight_decay=1e-5):
        super().__init__()
        self.fc = nn.Embedding(num_feats, output_dim)
        self.bias = nn.Parameter(torch.zeros(output_dim))
        self.offsets = np.array((0, *np.cumsum(num_feats)[: -1]), dtype=int)

        self.embedding = nn.Embedding(num_feats, embed_dim)
        self.reduce_sum = reduce_sum
        self.sigmoid = sigmoid
        self.weight_decay = weight_decay

        nn.init.xavier_uniform_(self.embedding.weight.data)

    def forward(self, x):
        x = x + x.new_tensor(self.offsets).unsqueeze(0)

        linear_term = torch.sum(self.fc(x), dim=1) + self.bias
        x_embedding = self.embedding(x)

        square_of_sum = torch.sum(x_embedding, dim=1) ** 2
        sum_of_square = torch.sum(x_embedding ** 2, dim=1)
        interaction = square_of_sum - sum_of_square

        if self.reduce_sum:
            interaction = torch.sum(interaction, dim=1, keepdim=True)
        interaction = 0.5 * interaction

        out = linear_term + interaction

        if self.sigmoid:
            return torch.sigmoid(out.squeeze(1))
        return out

    def l2_regularization_loss(self):
        l2_reg = 0.0

        for param in self.parameters():
            if param.dim() > 1:
                l2_reg += torch.norm(param, p=2) ** 2

        l2_reg *= self.weight_decay
        return l2_reg
