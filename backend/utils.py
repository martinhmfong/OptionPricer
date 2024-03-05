import numpy as np


def simulate_discrete_prices(s0: float, mu: float, sigma: float, days: int) -> np.ndarray:
    delta_t = 1 / days
    sns = np.random.standard_normal(days)
    factors = 1 + mu * delta_t + sigma * np.sqrt(delta_t) * sns
    prices = np.cumprod(factors) * s0
    return prices


def simulate_continuous_prices(s0: float, mu: float, sigma: float, days: int) -> np.ndarray:
    delta_t = 1 / days
    sns = np.random.standard_normal(days)
    factors = (mu - sigma ** 2 / 2) * delta_t + sigma * np.sqrt(delta_t) * sns
    returns = np.log(s0) + np.cumsum(factors)
    prices = np.exp(returns)
    return prices


if __name__ == '__main__':
    p = simulate_discrete_prices(100, .05, .2, 250)
    from matplotlib import pyplot as plt
    plt.plot(p)
    plt.show()
