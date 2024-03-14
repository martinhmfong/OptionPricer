import random
from unittest import TestCase

from common.constants import OptionName
from formula.european_options import european_option_price, european_option_implied_volatility


class TestBlackScholesCallPut(TestCase):
    def test_european_call_price(self):
        # use assignment 2 Q1 as test case
        params = {'s': 100, 'k': 100, 't': 0.5, 'sigma': 0.2, 'r': 0.01, 'q': 0}
        call_price = european_option_price(option_name=OptionName.EuropeanCall, **params)
        expected_call_price = 5.876024233827607
        self.assertAlmostEqual(expected_call_price, call_price)

    def test_european_put_price(self):
        # use assignment 2 Q1 as test case
        params = {'s': 100, 'k': 100, 't': 0.5, 'sigma': 0.2, 'r': 0.01, 'q': 0}
        call_price = european_option_price(option_name=OptionName.EuropeanPut, **params)
        expected_call_price = 5.377272153095845
        self.assertAlmostEqual(expected_call_price, call_price)

    def test_european_option_implied_volatility_call(self):
        expected_implied_volatility = random.random()
        params = {
            's': 100, 'k': 100,
            't': 2.5, 'sigma': expected_implied_volatility,
            'r': 0.08, 'q': 0.2
        }
        theoretical_option_price = european_option_price(option_name=OptionName.EuropeanCall, **params)
        implied_volatility = european_option_implied_volatility(
            option_price=theoretical_option_price, option_name=OptionName.EuropeanCall,
            **{k: v for k, v in params.items() if k != 'sigma'}
        )
        self.assertAlmostEqual(expected_implied_volatility, implied_volatility)

    def test_european_option_implied_volatility_put(self):
        expected_implied_volatility = random.random()
        params = {
            's': 200, 'k': 150,
            't': 2, 'sigma': expected_implied_volatility,
            'r': 0.03, 'q': 0.12
        }
        theoretical_option_price = european_option_price(option_name=OptionName.EuropeanPut, **params)
        implied_volatility = european_option_implied_volatility(
            option_price=theoretical_option_price, option_name=OptionName.EuropeanPut,
            **{k: v for k, v in params.items() if k != 'sigma'}
        )
        self.assertAlmostEqual(expected_implied_volatility, implied_volatility)
