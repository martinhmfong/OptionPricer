from typing import List, Any

import numpy as np
from numpy import ndarray, dtype, floating

from common.constants import OptionType, SimulationResult, z_value_95
from common.utils import exp, norm_random, sqrt, simulate_prices, mean, std, norm_cdf, norm_ppf, cov
from formula.asian_options import geometric_asian_option_price


def arithmetic_asian_option_price(
        s: float, k: float, t: float, sigma: float, r: float, n: int,
        option_name: OptionType, path_number: int, is_control_variate: bool
) -> SimulationResult:
    if option_name not in (OptionType.Call, OptionType.Put):
        raise ValueError(f"{option_name} is not supported by this function")

    paths = [simulate_prices(s, r, sigma, t, n) for _ in range(path_number)]
    arithmetic_payoff = [i.mean() for i in paths]

    if option_name == OptionType.Call:
        arithmetic_price = [exp(-r * t) * max(i - k, 0) for i in arithmetic_payoff]
    else:
        arithmetic_price = [exp(-r * t) * max(k - i, 0) for i in arithmetic_payoff]

    if is_control_variate:
        geometric_payoff = [i.prod() ** (1 / n) for i in paths]
        covariance = cov(arithmetic_payoff, geometric_payoff)
        theta = covariance / std(geometric_payoff) ** 2
        arr = arithmetic_payoff + theta * (geometric_payoff - 1)
    else:
        price = mean(arithmetic_price)
        sd = std(arithmetic_price)
        return SimulationResult(
            price=price,
            confidence_interval=[
                price - sd / sqrt(path_number) * z_value_95,
                price + sd / sqrt(path_number) * z_value_95
            ]
        )


if __name__ == "__main__":
    param = dict(
        s=100, k=100, t=3, sigma=0.3, r=0.05, n=50, path_number=100_000
    )
    mc_call = arithmetic_asian_option_price(**param, option_name=OptionType.Call, is_control_variate=True)
    print(mc_call)

    # mc_put = arithmetic_asian_option_price(**param, option_name=OptionName.Put, is_control_variate=False)
    # print(mc_put)

    # cv_mc_call = arithmetic_asian_option_price(**param, option_name=OptionName.ArithmeticAsianCall, is_control_variate=True)
