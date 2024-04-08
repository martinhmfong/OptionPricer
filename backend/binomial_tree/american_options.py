import numpy as np

from common.constants import OptionType
from common.utils import exp, sqrt


def american_option_price(
        s: float, k: float, t: float, sigma: float, r: float, option_type: OptionType, n: int
) -> float:
    n = int(n)
    delta_t = t / n
    u = exp(sigma * sqrt(delta_t))
    d = 1 / u
    p = (exp(r * delta_t) - d) / (u - d)

    asset_tree = np.zeros((n + 1, n + 1))
    asset_tree[0, 0] = s
    for i in range(1, n + 1):
        asset_tree[i, 0] = asset_tree[i - 1, 0] * u
        for j in range(1, i + 1):
            asset_tree[i, j] = asset_tree[i - 1, j - 1] * d

    option_tree = np.zeros((n + 1, n + 1))
    if option_type == OptionType.Call:
        option_tree[n, :] = np.maximum(0, asset_tree[n, :] - k)
    else:
        option_tree[n, :] = np.maximum(0, k - asset_tree[n, :])

    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            value = asset_tree[i, j] - k if option_type == OptionType.Call else k - asset_tree[i, j]
            option_tree[i, j] = np.maximum(
                exp(-r * delta_t) * (p * option_tree[i + 1, j] + (1 - p) * option_tree[i + 1, j + 1]),
                value
            )
    return float(option_tree[0, 0])


if __name__ == '__main__':
    param = dict(s=50, r=0.1, sigma=0.4, t=2.0, n=200, option_type=OptionType.Put)
    for i in (40, 50, 70):
        param['k'] = i
        option_price = american_option_price(**param)
        print(f'Option Price: {option_price} | {param}')
