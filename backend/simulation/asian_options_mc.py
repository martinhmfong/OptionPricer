from common.constants import OptionType, SimulationResult, z_value_95
from common.utils import sqrt, simulate_prices, mean, std, cov, discounted_payoffs
from formula.asian_options import geometric_asian_option_price


def arithmetic_asian_option_price(s: float, k: float, t: float, sigma: float, r: float, n: int, option_name: OptionType, path_number: int,
                                  is_control_variate: bool) -> SimulationResult:
    if option_name not in (OptionType.Call, OptionType.Put):
        raise ValueError(f"{option_name} is not supported by this function")

    paths = [simulate_prices(s, r, sigma, t, n) for _ in range(path_number)]
    arithmetic_means = [i.mean() for i in paths]
    arithmetic_payoff = discounted_payoffs(arithmetic_means, r, t, k, option_name)

    if is_control_variate:
        geometric_means = [i.prod() ** (1 / n) for i in paths]
        geometric_payoff = discounted_payoffs(geometric_means, r, t, k, option_name)
        covariance = cov(arithmetic_payoff, geometric_payoff)
        theta = covariance / std(geometric_payoff) ** 2
        geo_asian_price = geometric_asian_option_price(s, k, t, sigma, r, n, option_name)
        arr = arithmetic_payoff + theta * (geometric_payoff - geo_asian_price)
        price = mean(arr)
        sd = std(arr)
    else:
        price = mean(arithmetic_payoff)
        sd = std(arithmetic_payoff)

    return SimulationResult(
        price=price,
        confidence_interval=[price - sd / sqrt(path_number) * z_value_95, price + sd / sqrt(path_number) * z_value_95]
    )


if __name__ == "__main__":
    param = dict(s=100, k=100, t=3, sigma=0.3, r=0.05, n=50, path_number=100_000)
    mc_call = arithmetic_asian_option_price(**param, option_name=OptionType.Put, is_control_variate=True)
    print(mc_call)
