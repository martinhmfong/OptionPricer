from abc import ABC, abstractmethod

import numpy as np

from common.constants import OptionType, SimulationResult
from common.utils import exp


class AbstractSimulation(ABC):
    def __init__(
            self, s: float, sigma: float, k: float, t: float, r: float,
            option_type: OptionType, m: int, is_control_variate: bool,
    ):
        self.s = s
        self.sigma = sigma
        self.k = k
        self.t = t
        self.r = r
        self.option_type = option_type
        self.m = int(m)
        self.is_control_variate = is_control_variate

    def discounted_payoffs(self, ref_rates: np.ndarray) -> np.ndarray:
        if self.option_type == OptionType.Call:
            return np.array([exp(-self.r * self.t) * max(i - self.k, 0) for i in ref_rates])
        if self.option_type == OptionType.Put:
            return np.array([exp(-self.r * self.t) * max(self.k - i, 0) for i in ref_rates])

    @abstractmethod
    def simulate(self) -> SimulationResult:
        ...
