from common.constants import OptionType
from common.utils import sqrt, ln, norm_cdf, exp


def basket_option_price(
        s1: float, s2: float, sigma1: float, sigma2: float, r: float, t: float, k: float, rho: float,
        option_name: OptionType
) -> float:
    sigma_b = sqrt(sigma1 ** 2 + sigma2 ** 2 + 2 * sigma1 * sigma2 * rho) / 2
    mu_b = r - (sigma1 ** 2 + sigma2 ** 2) / (2 * 2) + sigma_b ** 2 / 2
    geo_mean = sqrt(s1 * s2)
    d1_hat = (ln(geo_mean / k) + (mu_b + sigma_b ** 2 / 2) * t) / (sigma_b * sqrt(t))
    d2_hat = d1_hat - sigma_b * sqrt(t)
    if option_name == OptionType.Call:
        return exp(-r * t) * (geo_mean * exp(mu_b * t) * norm_cdf(d1_hat) - k * norm_cdf(d2_hat))
    if option_name == OptionType.Put:
        return exp(-r * t) * (k * norm_cdf(-d2_hat) - geo_mean * exp(mu_b * t) * norm_cdf(-d1_hat))


if __name__ == '__main__':
    p = basket_option_price(100, 100, 0.3, 0.3, 0.05, 3, 100, 0.5, OptionType.Call)
    print(p)
