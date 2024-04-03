from unittest import TestCase

from common.constants import OptionType
from formula.asian_options import geometric_asian_option_price


class TestAsianOptions(TestCase):
    def test_geo_asian_call(self):
        """
        Given by test case
        """
        params = {'s': 100, 'k': 100, 't': 3, 'sigma': 0.3, 'r': 0.05, 'n': 50, 'option_name': OptionType.Call}
        call_price = geometric_asian_option_price(**params)
        expected_call_price = 13.259
        self.assertAlmostEqual(expected_call_price, call_price, places=3)
