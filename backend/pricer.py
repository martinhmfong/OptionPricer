import pandas as pd

from binomial_tree.american_options import american_option_price
from common.constants import PricerName, OptionType, MeanMethod
from formula.asian_options import geometric_asian_option_price
from formula.basket_options import basket_option_price
from formula.european_options import european_option_price, european_option_implied_volatility
from simulation.asian_options_mc import AsianOptionSimulation
from simulation.basket_options_mc import BasketOptionSimulation
from simulation.kiko_options_mc import KIKOOptionSimulation


def calculate(pricer_name: PricerName, **kwargs):
    if pricer_name == PricerName.European:
        return european_option_price(**kwargs)
    if pricer_name == PricerName.ImpliedVolatility:
        return european_option_implied_volatility(**kwargs)
    if pricer_name == PricerName.Asian:
        mean_method = MeanMethod(kwargs.pop('mean_method'))
        use_simulation = kwargs.pop('use_simulation', False)
        if not use_simulation:
            return geometric_asian_option_price(**kwargs)
        else:
            kwargs['mean_method'] = mean_method
            return AsianOptionSimulation(**kwargs).simulate()
    if pricer_name == PricerName.Basket:
        mean_method = MeanMethod(kwargs.pop('mean_method'))
        use_simulation = kwargs.pop('use_simulation', False)
        if not use_simulation:
            return basket_option_price(**kwargs)
        else:
            kwargs['mean_method'] = mean_method
            return BasketOptionSimulation(**kwargs).simulate()
    if pricer_name == PricerName.American:
        return american_option_price(**kwargs)
    if pricer_name == PricerName.KIKO:
        kwargs['is_control_variate'] = False
        return KIKOOptionSimulation(**kwargs).simulate()


def test_cases():
    df = pd.read_excel('test_cases.xlsx')
    d = []

    for _, row in df.iterrows():
        params = {k: v for k, v in row.dropna().items()}
        pricer_name = PricerName(params.pop('pricer_name'))
        params['option_type'] = OptionType(params.pop('option_type'))
        result = calculate(pricer_name, **params)
        print(f'{pricer_name.name}: {params} | result = {result}')

        d.append({**params, **{'result': result, 'pricer_name': pricer_name.name}})

    res = pd.DataFrame(d)[list(df.columns) + ['result']]
    res.to_excel('test_case_result.xlsx', index=False)


if __name__ == '__main__':
    test_cases()
