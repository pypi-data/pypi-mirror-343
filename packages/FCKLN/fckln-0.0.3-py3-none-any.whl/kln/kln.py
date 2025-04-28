"""
KLN (Kullback-Leibler Nonlinearities)
-------------------------------------
Flexible Conditional Modeling Package.

Provides:
- FlexibleConditional: A module for learning structured conditional dependencies 
  that can interpolate between linear and nonlinear mappings.
"""

import torch
import torch.nn as nn

class FlexibleConditional(nn.Module):
    """
    FlexibleConditional module for modeling structured conditional dependencies.

    Parameters:
    ----------
    input_dim : int
        The dimensionality of the concatenated inputs (i and j).
    hidden_dim : int
        The size of the hidden layer for the nonlinear path.
    output_dim : int
        The dimensionality of the output (k).
    """
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(FlexibleConditional, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)
        self.nonlinear = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
        self.alpha = nn.Parameter(torch.tensor(0.5))

    def forward(self, i, j):
        """
        Forward pass for FlexibleConditional.

        Parameters:
        ----------
        i : torch.Tensor
            Tensor of shape (batch_size, i_dim)
        j : torch.Tensor
            Tensor of shape (batch_size, j_dim)

        Returns:
        -------
        torch.Tensor
            Output tensor of shape (batch_size, output_dim)
        """
        x = torch.cat([i, j], dim=-1)
        linear_out = self.linear(x)
        nonlinear_out = self.nonlinear(x)
        alpha = torch.sigmoid(self.alpha)
        output = alpha * linear_out + (1 - alpha) * nonlinear_out
        return output

# Optional utility function (just if you want an easy interface)
def create_flexible_model(input_dim, hidden_dim=64, output_dim=1):
    """
    Utility function to quickly create a FlexibleConditional model.

    Parameters:
    ----------
    input_dim : int
    hidden_dim : int
    output_dim : int

    Returns:
    -------
    FlexibleConditional
    """
    return FlexibleConditional(input_dim, hidden_dim, output_dim)
