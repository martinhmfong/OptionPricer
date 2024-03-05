import numpy as np
from scipy.stats import norm

from common.constants import OptionType
from common.utils import ln, sqrt


def calculate_d1(s: float, k: float, t: float, sigma: float, r: float, q: float, ) -> float:
    d1 = (ln(s / k) + (r - q) * t) / (sigma * np.sqrt(t)) + 0.5 * sigma * np.sqrt(t)
    return d1


def calculate_d2(s: float, k: float, t: float, sigma: float, r: float, q: float, ) -> float:
    d2 = (ln(s / k) + (r - q) * t) / (sigma * np.sqrt(t)) - 0.5 * sigma * np.sqrt(t)
    return d2


def is_valid_european_option_price(
        option_price: float, s: float, k: float, t: float, r: float, q: float, option_type: OptionType
) -> bool:
    if option_type == OptionType.EuropeanCall:
        option_max = s * np.exp(-q * t)
        option_min = max(s * np.exp(-q * t) - k * np.exp(-r * t), 0)
    elif option_type == OptionType.EuropeanPut:
        option_min = max(k * np.exp(-r * t) - s * np.exp(-q * t), 0)
        option_max = k * np.exp(-r * t)
    else:
        raise ValueError(f"Invalid option type: {option_type}")
    return option_min < option_price <= option_max


def european_option_price(
        s: float, k: float, t: float, sigma: float, r: float, q: float, option_type: OptionType
) -> float:
    d1 = calculate_d1(s, k, t, sigma, r, q)
    d2 = calculate_d2(s, k, t, sigma, r, q)
    if option_type == OptionType.EuropeanCall:
        return s * np.exp(-q * t) * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
    if option_type == OptionType.EuropeanPut:
        return k * np.exp(-r * t) * norm.cdf(-d2) - s * np.exp(-q * t) * norm.cdf(-d1)


def european_option_vega(
        s: float, k: float, t: float, sigma: float, r: float, q: float
) -> float:
    d1 = calculate_d1(s, k, t, sigma, r, q)
    return s * np.exp(-q * t) * np.sqrt(t) * norm.pdf(d1, 0, 1)


def european_option_implied_volatility(
        option_price: float, s: float, k: float, t: float, r: float, q: float,
        option_type: OptionType, max_steps: int = 100, tolerance: float = 1e-8
) -> float:
    if not is_valid_european_option_price(option_price, s, k, t, r, q, option_type):
        return np.nan
    step = 0
    diff = float('inf')
    sigma_guess = sqrt(2 * np.abs((ln(s / k) + (r - q) * t) / t))
    while (step < max_steps) and (diff >= tolerance):
        guess_price = european_option_price(s, k, t, sigma_guess, r, q, option_type)
        guess_vega = european_option_vega(s, k, t, sigma_guess, r, q)
        increment = (guess_price - option_price) / guess_vega
        sigma_guess -= increment
        step += 1
        diff = np.abs(sigma_guess)
    if step > max_steps and diff >= tolerance:
        return np.nan
    if sigma_guess <= 0:
        return np.nan
    return sigma_guess
