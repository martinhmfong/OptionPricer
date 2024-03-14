from enum import Enum


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
    EuropeanCall = 'EuropeanCall'
    EuropeanPut = 'EuropeanPut'
    AmericanCall = 'AmericanCall'
    AmericanPut = 'AmericanPut'
    AsianCall = 'AsianCall'
    AsianPut = 'AsianPut'

    ArithmeticAsianCall = 'ArithmeticAsianCall'
    ArithmeticAsianPut = 'ArithmeticAsianPut'
    GeometricAsianCall = 'GeometricAsianCall'
    GeometricAsianPut = 'GeometricAsianPut'

    GeometricBasketCall = 'GeometricBasketCall'
    GeometricBasketPut = 'GeometricBasketPut'

    # unique one
    KIKOPut = 'KIKOPut'
