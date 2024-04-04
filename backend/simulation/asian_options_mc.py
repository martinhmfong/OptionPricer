from typing import List

import numpy as np

from common.constants import SimulationResult, MeanMethod, OptionType
from common.utils import exp
from simulation.abstract_mc import AbstractSimulation


class AsianOptionSimulation(AbstractSimulation):
    def discounted_payoffs(self, ref_rates: List[float]) -> np.ndarray:
        if self.option_type == OptionType.Call:
            return np.array([exp(-self.r * self.t) * max(i - self.k, 0) for i in ref_rates])
        if self.option_type == OptionType.Put:
            return np.array([exp(-self.r * self.t) * max(self.k - i, 0) for i in ref_rates])

    def cal_arithmetic_payoffs(self, paths: np.ndarray) -> np.ndarray:
        ref_rates = [i.mean() for i in paths]
        return self.discounted_payoffs(ref_rates)

    def cal_geometric_payoffs(self, paths: np.ndarray) -> np.ndarray:
        ref_rates = [i.prod() ** (1 / self.n) for i in paths]
        return self.discounted_payoffs(ref_rates)

    def simulate(self) -> SimulationResult:
        paths = self.simulate_paths()
        geometric_payoffs = self.cal_geometric_payoffs(paths)
        if self.mean_method == MeanMethod.Geometric:
            return geometric_payoffs.mean()


if __name__ == '__main__':
    params = dict(
        s=100, k=100, t=3, sigma=0.3, r=0.05, n=50,
        option_type=OptionType.Call, m=100_000, is_control_variate=False,
        mean_method=MeanMethod.Geometric
    )
    pricer = AsianOptionSimulation(**params)
    print(pricer.simulate())
