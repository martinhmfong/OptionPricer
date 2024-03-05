from enum import Enum


class OptionType(Enum):
    EuropeanCall = 'EuropeanCall'
    EuropeanPut = 'EuropeanPut'

    AmericanCall = 'AmericanCall'
    AmericanPut = 'AmericanPut'
