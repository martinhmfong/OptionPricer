from dataclasses import dataclass
from enum import Enum
from typing import List
from scipy.stats import norm

z_value_95 = norm.ppf(1 - (1 - 0.95) / 2)


class ExerciseStyle(Enum):
    European = 'European'
    American = 'American'
    Asian = 'Asian'


class OptionType(Enum):
    Call = 'Call'
    Put = 'Put'


class MeanStrategy(Enum):
    Arithmetic = 'Arithmetic'
    Geometric = 'Geometric'


class OptionName(Enum):
    Call = 'Call'
    Put = 'Put'

    # unique one
    KIKOPut = 'KIKOPut'


@dataclass
class SimulationResult:
    price: float
    confidence_interval: List[float]
