from typing import Tuple

import numpy as np

from common.constants import SimulationResult, MeanMethod, OptionType
from common.utils import norm_random, exp, sqrt
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


if __name__ == '__main__':
    params = dict(
        s=100, s2=100, k=100, t=3, sigma=0.3, sigma2=0.3, r=0.05, rho=0.5,
        option_type=OptionType.Call, m=100_000, is_control_variate=False,
        mean_method=MeanMethod.Geometric
    )
    pricer = BasketOptionSimulation(**params)
    print(pricer.simulate())
