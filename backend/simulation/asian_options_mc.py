import numpy as np

from common.constants import OptionName, SimulationResult, z_value_95
from common.utils import exp, norm_random, sqrt, simulate_prices, mean, std, norm_cdf, norm_ppf
from formula.asian_options import geometric_asian_option_price


def arithmetic_asian_option_price(
        s: float, k: float, t: float, sigma: float, r: float, n: int,
        option_name: OptionName, path_number: int, is_control_variate: bool
) -> SimulationResult:
    paths = [simulate_prices(s, r, sigma, t, n) for _ in range(path_number)]
    arithmetic_mean = [i.mean() for i in paths]

    if option_name == OptionName.ArithmeticAsianCall:
        arithmetic_price = [exp(-r * t) * max(i - k, 0) for i in arithmetic_mean]
    if option_name == OptionName.ArithmeticAsianPut:
        arithmetic_price = [exp(-r * t) * max(k - i, 0) for i in arithmetic_mean]
    if is_control_variate:
        geometric_mean = [i.cumprod() ** (1 / path_number) for i in paths]
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
    mc_call = arithmetic_asian_option_price(**param, option_name=OptionName.ArithmeticAsianCall, is_control_variate=False)
    print(mc_call)

    # mc_put = arithmetic_asian_option_price(**param, option_name=OptionName.ArithmeticAsianPut, is_control_variate=False)
    # print(mc_put)

    # cv_mc_call = arithmetic_asian_option_price(**param, option_name=OptionName.ArithmeticAsianCall, is_control_variate=True)
