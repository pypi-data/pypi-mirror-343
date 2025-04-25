import torch
from torch.optim import Optimizer

class HomM(Optimizer):
    def __init__(self, params, lr=0.1, a=-0.5, k1=1.0, k2=1.0, beta=0.9):
        """
        Homogeneous Momentum Optimizer

        Args:
            params (iterable): model parameters
            lr (float): learning rate
            a (float): exponent on the norm (usually negative)
            k1, k2 (float): gradient scaling coefficients
            eps (float): velocity coupling factor
        """
        defaults = dict(lr=lr, a=a, k1=k1, k2=k2, beta=beta)
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        """
        Perform a single optimization step.
        """
        loss = closure() if closure is not None else None
        epsilon_min = 1e-5  # to avoid instability when norm is close to zero

        for group in self.param_groups:
            lr = group['lr']
            a = group['a']
            k1 = group['k1']
            k2 = group['k2']
            beta = group['beta']

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad.data  # gradient tensor

                # Get state dict for this parameter
                state = self.state[p]

                # Initialize velocity buffer if not present
                if 'v' not in state:
                    state['v'] = torch.zeros_like(p.data)

                v = state['v']

                # Compute Euclidean norm: || [grad, v] ||
                # Compute || [grad, v] ||
                norm_z = torch.sqrt(grad.pow(2).sum() + v.pow(2).sum()).clamp(min=1e-5)

                # Compute time-varying gain
                alpha = lr * norm_z.pow(a)

                # Explicit update (in-place)
                v.add_(alpha * (-k2 * grad - beta * v))  # Update v
                p.data.add_(alpha * (-k1 * grad + v))  # Update p

        return loss
