from unittest import TestCase

from common.constants import OptionType
from formula.basket_options import basket_option_price


class TestBasketOption(TestCase):
    def test_basket_option_price(self):
        params = {
            's1': 100, 's2': 100, 'sigma1': 0.3, 'sigma2': 0.3,
            'r': 0.05, 't': 3, 'k': 100, 'rho': 0.5, 'option_name': OptionType.Call
        }
        call_price = basket_option_price(**params)
        expected_call_price = 22.102
        self.assertAlmostEqual(expected_call_price, call_price, places=3)
