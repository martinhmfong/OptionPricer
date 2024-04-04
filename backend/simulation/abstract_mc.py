from abc import ABC, abstractmethod
from typing import List

import numpy as np

from common.constants import OptionType, MeanMethod, SimulationResult
from common.utils import exp, sqrt, norm_random


class AbstractSimulation(ABC):
    def __init__(
            self, s: float, k: float, t: float, sigma: float, r: float, n: int,
            option_type: OptionType, m: int, is_control_variate: bool,
            mean_method: MeanMethod = MeanMethod.Arithmetic
    ):
        self.s = s
        self.k = k
        self.t = t
        self.sigma = sigma
        self.r = r
        self.n = n
        self.option_type = option_type
        self.m = m
        self.is_control_variate = is_control_variate
        self.mean_method = mean_method

    def simulate_path(self, random_factor: np.ndarray = None) -> np.ndarray:
        random_factor = random_factor if random_factor is not None else norm_random(self.n)
        delta_t = self.t / self.n
        growth_factors = exp((self.r - self.sigma ** 2 / 2) * delta_t + self.sigma * sqrt(delta_t) * random_factor)
        cumulative_rate = np.cumprod(growth_factors)
        return self.s * cumulative_rate

    def simulate_paths(self) -> List[np.ndarray]:
        return [self.simulate_path() for _ in range(self.m)]

    def path_payoffs(self, paths: List[np.ndarray], ref_rate: float) -> np.ndarray:
        ...

    @abstractmethod
    def simulate(self) -> SimulationResult:
        ...
