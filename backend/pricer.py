import pandas as pd

from common.constants import PricerName, OptionType, MeanMethod
from formula.asian_options import geometric_asian_option_price
from formula.european_options import european_option_price, european_option_implied_volatility
from simulation.asian_options_mc import AsianOptionSimulation

df = pd.read_excel('test_cases.xlsx')


def calculate(pricer_name: PricerName, **kwargs):
    if pricer_name == PricerName.European:
        return european_option_price(**kwargs)
    if pricer_name == PricerName.ImpliedVolatility:
        return european_option_implied_volatility(**kwargs)
    if pricer_name == PricerName.Asian:
        mean_method = kwargs.pop('mean_method')
        if mean_method == 'Geometric':
            return geometric_asian_option_price(**kwargs)
        if mean_method == 'Arithmetic':
            kwargs['mean_method'] = MeanMethod.Arithmetic
            return AsianOptionSimulation(**kwargs).simulate()


if __name__ == '__main__':
    df = pd.read_excel('test_cases.xlsx')
    print(df)

    for _, row in df.iterrows():
        params = {k: v for k, v in row.dropna().items()}
        pricer_name = PricerName(params.pop('pricer_name'))
        params['option_type'] = OptionType(params.pop('option_type'))
        result = calculate(pricer_name, **params)
        print(f'{params} | result = {result}')
