import numpy as np
import pandas as pd
from scipy.stats import qmc, norm

from common.constants import OptionType, SimulationResult, z_value_95
from common.utils import sqrt, exp
from simulation.abstract_mc import AbstractSimulation


class KIKOOptionSimulation(AbstractSimulation):
    def __init__(
            self, s: float, sigma: float, k: float, t: float, r: float, option_type: OptionType, m: int, is_control_variate: bool,
            barrier_low: float, barrier_high: float, n: int, rebate: float
    ):
        super().__init__(s, sigma, k, t, r, option_type, m, is_control_variate)
        if self.option_type == OptionType.Call:
            raise ValueError('Call Options are not supported')
        self.barrier_low = barrier_low
        self.barrier_high = barrier_high
        self.n = n
        self.rebate = rebate
        self.delta_t = self.t / self.n

    def simulate(self) -> SimulationResult:
        sequencer = qmc.Sobol(d=self.n, seed=1000)
        z = norm.ppf(np.array(sequencer.random(n=self.m)))
        samples = (self.r - self.sigma ** 2 / 2) * self.delta_t + self.sigma * sqrt(self.delta_t) * z
        df = pd.DataFrame(samples).cumsum(axis=1).apply(np.exp) * self.s
        df['value'] = df.apply(self.calculate_value, axis=1)
        value = df.value.mean()
        std = df.value.std()
        return SimulationResult(
            price=value,
            confidence_interval=(
                value - z_value_95 * std / sqrt(self.m),
                value + z_value_95 * std / sqrt(self.m)
            )
        )

    def calculate_value(self, row: np.array) -> float:
        price_max, price_min = row.max(), row.min()
        if price_max >= self.barrier_high:  # KO happened
            ko_time = row[row.ge(self.barrier_high)].index[0] + 1
            return self.rebate * exp(-ko_time * self.r * self.delta_t)
        if price_min <= self.barrier_low:
            return max(self.k - row.iloc[-1], 0) * exp(-self.r * self.t)
        return 0


if __name__ == '__main__':
    option = KIKOOptionSimulation(100, 0.2, 100, 2, 0.05, OptionType.Put, 100_000, False, 80, 125, 24, 1.5)
    price = option.simulate()
    print(price)
