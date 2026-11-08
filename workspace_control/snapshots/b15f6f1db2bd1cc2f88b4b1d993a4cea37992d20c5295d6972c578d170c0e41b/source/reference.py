import numpy as np
import torch


def impl(mixes, hc_mult=4, hc_sinkhorn_iters=20, eps=1e-06):
    return_numpy = not isinstance(mixes, torch.Tensor)
    x = torch.as_tensor(mixes).float()
    H = int(hc_mult)
    iters = int(hc_sinkhorn_iters)
    eps = float(eps)
    z = x.reshape(*x.shape[:-1], (2 + H) * H)
    (z_pre, z_post, z_comb) = z.split([H, H, H * H], dim=-1)
    pre = torch.sigmoid(z_pre) + eps
    post = 2.0 * torch.sigmoid(z_post)
    comb = torch.softmax(z_comb.reshape(*x.shape[:-1], H, H), dim=-1) + eps
    comb = comb / (comb.sum(dim=-2, keepdim=True) + eps)
    for _ in range(iters - 1):
        comb = comb / (comb.sum(dim=-1, keepdim=True) + eps)
        comb = comb / (comb.sum(dim=-2, keepdim=True) + eps)
    if return_numpy:
        return (pre.numpy(), post.numpy(), comb.numpy())
    return (pre, post, comb)
