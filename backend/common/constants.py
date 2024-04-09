from dataclasses import dataclass, asdict
from enum import Enum
from typing import Tuple

from scipy.stats import norm

z_value_95 = norm.ppf(1 - (1 - 0.95) / 2)


class OptionType(Enum):
    Call = 'Call'
    Put = 'Put'


class MeanMethod(Enum):
    Arithmetic = 'Arithmetic'
    Geometric = 'Geometric'


class PricerName(Enum):
    European = 'European'
    ImpliedVolatility = 'ImpliedVolatility'
    Asian = 'Asian'
    Basket = 'Basket'
    American = 'American'
    KIKO = 'KIKO'


@dataclass
class SimulationResult:
    price: float
    confidence_interval: Tuple[float, float] = None
    delta: float = None

    def to_dict(self) -> dict:
        return asdict(self)


if __name__ == '__main__':
    s = SimulationResult(100, (99, 101))
    print(s.to_dict())
