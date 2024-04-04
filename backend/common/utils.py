from typing import Union, List, Iterable

import numpy as np
from scipy.stats import norm

from common.constants import OptionType

number_type = Union[int, float, np.ndarray, List[float]]

np.random.seed(1000)


def exp(x: number_type) -> number_type:
    return np.exp(x)


def ln(x: number_type) -> number_type:
    return np.log(x)


def sqrt(x: number_type) -> number_type:
    return np.sqrt(x)


def mean(x: number_type) -> number_type:
    return np.mean(x)


def std(x: number_type) -> number_type:
    return np.std(x)


def cov(x: number_type, y: number_type) -> float:
    return float(np.cov(x, y)[0][1])


def norm_cdf(x: float) -> float:
    return norm.cdf(x)


def norm_ppf(x: float) -> float:
    return norm.ppf(x)


def norm_random(sample_size: int) -> np.ndarray:
    return np.random.normal(loc=0, scale=1, size=sample_size)


def simulate_prices(s: float, rate: float, sigma: float, t: float, n: int) -> np.ndarray:
    delta_t = t / n
    random_factors = norm_random(n)
    growth_factors = np.exp((rate - sigma ** 2 / 2) * delta_t + sigma * sqrt(delta_t) * random_factors)
    cumulative_rate = np.cumprod(growth_factors)
    return s * cumulative_rate


def discounted_payoffs(values: Iterable[float], r: float, t: float, k: float, option_type: OptionType) -> np.ndarray:
    if option_type == OptionType.Call:
        return np.array([exp(-r * t) * max(i - k, 0) for i in values])
    if option_type == OptionType.Put:
        return np.array([exp(-r * t) * max(k - i, 0) for i in values])


if __name__ == '__main__':
    # p = simulate_prices(s=50, rate=0.05, sigma=0.3, t=3, n=50)
    # print(p)

    a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = [1, 2, 3, 1, 2, 3, 1, 2, 3]
    c = cov(a, b)
    print(c)