from typing import Tuple

import numpy as np

from common.constants import SimulationResult, MeanMethod, OptionType, z_value_95
from common.utils import norm_random, exp, sqrt, cov
from formula.basket_options import basket_option_price
from simulation.abstract_mc import AbstractSimulation


class BasketOptionSimulation(AbstractSimulation):
    def __init__(
            self, s: float, sigma: float, s2: float, sigma2: float, rho: float,
            k: float, t: float, r: float, option_type: OptionType, m: int, is_control_variate: bool, mean_method: MeanMethod.Arithmetic
    ):
        super().__init__(s, sigma, k, t, r, option_type, m, is_control_variate)
        self.s2 = s2
        self.sigma2 = sigma2
        self.rho = rho
        self.mean_method = mean_method

    def random_factors(self) -> Tuple[np.ndarray, np.ndarray]:
        r1 = norm_random(self.m)
        r2 = self.rho * r1 + np.sqrt(1 - self.rho ** 2) * norm_random(self.m)
        return r1, r2

    def generate_asset_prices(self) -> Tuple[np.ndarray, np.ndarray]:
        r1, r2 = self.random_factors()
        a1 = exp((self.r - self.sigma ** 2 / 2) * self.t + self.sigma * sqrt(self.t) * r1) * self.s
        a2 = exp((self.r - self.sigma2 ** 2 / 2) * self.t + self.sigma2 * sqrt(self.t) * r2) * self.s2
        return a1, a2

    def cal_arithmetic_payoffs(self, a1: np.ndarray, a2: np.ndarray) -> np.ndarray:
        ref_rates = (a1 + a2) / 2
        return self.discounted_payoffs(ref_rates)

    def cal_geometric_payoffs(self, a1: np.ndarray, a2: np.ndarray) -> np.ndarray:
        ref_rates = (a1 * a2) ** 0.5
        return self.discounted_payoffs(ref_rates)

    def simulate(self) -> SimulationResult:
        a1, a2 = self.generate_asset_prices()
        geometric_payoffs = self.cal_geometric_payoffs(a1, a2)
        if self.mean_method == MeanMethod.Geometric:
            return SimulationResult(geometric_payoffs.mean())
        if self.mean_method == MeanMethod.Arithmetic:
            arithmetic_payoffs = self.cal_arithmetic_payoffs(a1, a2)
            mean, std = arithmetic_payoffs.mean(), arithmetic_payoffs.std()
            if self.is_control_variate:
                covariance = cov(arithmetic_payoffs, geometric_payoffs)
                theta = covariance / geometric_payoffs.var()
                geometric_theoretical_price = basket_option_price(
                    self.s, self.s2, self.sigma, self.sigma2, self.r, self.t, self.k, self.rho, self.option_type
                )
                z = arithmetic_payoffs - theta * (geometric_theoretical_price - geometric_payoffs)
                mean, std = z.mean(), z.std()
            return SimulationResult(
                price=mean,
                confidence_interval=(
                    mean - z_value_95 * std / sqrt(self.m),
                    mean + z_value_95 * std / sqrt(self.m)
                )
            )


if __name__ == '__main__':
    param1 = dict(
        s=100, s2=100, k=100, t=3, sigma=0.3, sigma2=0.3, r=0.05, rho=0.5,
        option_type=OptionType.Call, m=100_000, is_control_variate=False,
        mean_method=MeanMethod.Arithmetic
    )
    pricer = BasketOptionSimulation(**param1)
    print(pricer.simulate())

    param2 = dict(
        s=100, s2=100, k=100, t=3, sigma=0.3, sigma2=0.3, r=0.05, rho=0.5,
        option_type=OptionType.Call, m=100_000, is_control_variate=False,
        mean_method=MeanMethod.Arithmetic
    )
    pricer = BasketOptionSimulation(**param2)
    print(pricer.simulate())
