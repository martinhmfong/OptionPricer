from typing import List

import numpy as np

from common.constants import SimulationResult, MeanMethod, OptionType, z_value_95
from common.utils import exp, cov, sqrt, norm_random
from formula.asian_options import geometric_asian_option_price
from simulation.abstract_mc import AbstractSimulation


class AsianOptionSimulation(AbstractSimulation):
    def __init__(
            self, s: float, sigma: float, k: float, t: float, r: float, option_type: OptionType, m: int, is_control_variate: bool,
            n: int, mean_method: MeanMethod.Arithmetic
    ):
        super().__init__(s, sigma, k, t, r, option_type, m, is_control_variate)
        self.n = int(n)
        self.mean_method = mean_method

    def simulate_path(self) -> np.ndarray:
        random_factor = norm_random(self.n)
        delta_t = self.t / self.n
        growth_factors = exp((self.r - self.sigma ** 2 / 2) * delta_t + self.sigma * sqrt(delta_t) * random_factor)
        cumulative_rate = np.cumprod(growth_factors)
        return self.s * cumulative_rate

    def simulate_paths(self) -> List[np.ndarray]:
        return [self.simulate_path() for _ in range(self.m)]

    def cal_arithmetic_payoffs(self, paths: List[np.ndarray]) -> np.ndarray:
        ref_rates = np.array([i.mean() for i in paths])
        return self.discounted_payoffs(ref_rates)

    def cal_geometric_payoffs(self, paths: List[np.ndarray]) -> np.ndarray:
        ref_rates = np.array([i.prod() ** (1 / self.n) for i in paths])
        return self.discounted_payoffs(ref_rates)

    def simulate(self) -> SimulationResult:
        paths = self.simulate_paths()
        geometric_payoffs = self.cal_geometric_payoffs(paths)
        if self.mean_method == MeanMethod.Geometric:
            return SimulationResult(geometric_payoffs.mean())
        if self.mean_method == MeanMethod.Arithmetic:
            arithmetic_payoffs = self.cal_arithmetic_payoffs(paths)
            mean, std = arithmetic_payoffs.mean(), arithmetic_payoffs.std()
            if self.is_control_variate:
                covariance = cov(arithmetic_payoffs, geometric_payoffs)
                theta = covariance / geometric_payoffs.var()
                geometric_theoretical_price = geometric_asian_option_price(self.s, self.k, self.t, self.sigma, self.r, self.n, self.option_type)
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
    params = dict(
        s=100, k=100, t=3, sigma=0.3, r=0.05, n=50,
        option_type=OptionType.Call, m=100_000, is_control_variate=False,
        mean_method=MeanMethod.Arithmetic
    )
    pricer = AsianOptionSimulation(**params)
    print(pricer.simulate())
