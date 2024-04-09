import pandas as pd

from binomial_tree.american_options import american_option_price
from common.constants import PricerName, OptionType, MeanMethod
from formula.asian_options import geometric_asian_option_price
from formula.basket_options import basket_option_price
from formula.european_options import european_option_price, european_option_implied_volatility
from simulation.asian_options_mc import AsianOptionSimulation
from simulation.basket_options_mc import BasketOptionSimulation
from simulation.kiko_options_mc import KIKOOptionSimulation


def clear_params(pricer_name: str, **kwargs) -> dict:
    mapping = {
        'European': ["r", "t", "s", "sigma", "q", "k", "option_type"],
        'ImpliedVolatility': ["r", "t", "s", "q", "k", "option_type", "option_price"],
        'Asian': ["r", "t", "s", "sigma", "k", "option_type", "mean_method", "n", "m", "is_control_variate", "use_simulation"],
        'Basket': ["r", "t", "s", "sigma", "s2", "sigma2", "rho", "k", "option_type", "mean_method", "m", "is_control_variate", "use_simulation"],
        'American': ["r", "t", "s", "sigma", "k", "option_type", "n"],
        'KIKO': ["r", "t", "s", "sigma", "k", "option_type", "n", "m", "barrier_low", "barrier_high", "rebate"],
    }
    required = mapping[pricer_name]
    return {k: v for k, v in kwargs.items() if k in required}


def calculate(pricer_name: str, **kwargs):
    kwargs = clear_params(pricer_name, **kwargs)
    pricer = PricerName(pricer_name)
    if pricer == PricerName.European:
        return european_option_price(**kwargs)
    if pricer == PricerName.ImpliedVolatility:
        return european_option_implied_volatility(**kwargs)
    if pricer == PricerName.Asian:
        mean_method = MeanMethod(kwargs.pop('mean_method'))
        use_simulation = kwargs.pop('use_simulation', False)
        if not use_simulation:
            return geometric_asian_option_price(**kwargs)
        else:
            kwargs['mean_method'] = mean_method
            return AsianOptionSimulation(**kwargs).simulate()
    if pricer == PricerName.Basket:
        mean_method = MeanMethod(kwargs.pop('mean_method'))
        use_simulation = kwargs.pop('use_simulation', False)
        if not use_simulation:
            return basket_option_price(**kwargs)
        else:
            kwargs['mean_method'] = mean_method
            return BasketOptionSimulation(**kwargs).simulate()
    if pricer == PricerName.American:
        return american_option_price(**kwargs)
    if pricer == PricerName.KIKO:
        kwargs['is_control_variate'] = False
        return KIKOOptionSimulation(**kwargs).simulate()


def test_cases():
    df = pd.read_excel('test_cases.xlsx')
    d = []

    for _, row in df.iterrows():
        params = {k: v for k, v in row.dropna().items()}
        pricer_name = params.pop('pricer_name')
        params['option_type'] = OptionType(params.pop('option_type'))
        result = calculate(pricer_name, **params)
        print(f'{pricer_name}: {params} | result = {result}')

        d.append({**params, **{'result': result, 'pricer_name': pricer_name}})

    res = pd.DataFrame(d)[list(df.columns) + ['result']]
    res.to_excel('test_case_result_done.xlsx', index=False)


if __name__ == '__main__':
    test_cases()
