from typing import List

import numpy as np

from common.constants import SimulationResult, MeanMethod, OptionType, z_value_95
from common.utils import exp, cov, sqrt
from formula.asian_options import geometric_asian_option_price
from simulation.abstract_mc import AbstractSimulation


class AsianOptionSimulation(AbstractSimulation):
    def discounted_payoffs(self, ref_rates: List[float]) -> np.ndarray:
        if self.option_type == OptionType.Call:
            return np.array([exp(-self.r * self.t) * max(i - self.k, 0) for i in ref_rates])
        if self.option_type == OptionType.Put:
            return np.array([exp(-self.r * self.t) * max(self.k - i, 0) for i in ref_rates])

    def cal_arithmetic_payoffs(self, paths: List[np.ndarray]) -> np.ndarray:
        ref_rates = [i.mean() for i in paths]
        return self.discounted_payoffs(ref_rates)

    def cal_geometric_payoffs(self, paths: List[np.ndarray]) -> np.ndarray:
        ref_rates = [i.prod() ** (1 / self.n) for i in paths]
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
