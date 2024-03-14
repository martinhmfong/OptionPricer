import numpy as np
from scipy.stats import norm


def exp(x: float) -> float:
    return np.exp(x)


def ln(x: float) -> float:
    return np.log(x)


def sqrt(x: float) -> float:
    return np.sqrt(x)


def norm_cdf(x: float) -> float:
    return norm.cdf(x)
