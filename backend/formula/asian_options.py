from common.constants import OptionType
from common.utils import sqrt, ln, norm_cdf, exp


def geometric_asian_option_price(
        s: float, k: float, t: float, sigma: float, r: float, n: int, option_type: OptionType
) -> float:
    sigma_hat = sigma * sqrt((n + 1) * (2 * n + 1) / (6 * n ** 2))
    mu_hat = (r - sigma ** 2 / 2) * (n + 1) / (2 * n) + sigma_hat ** 2 / 2
    d1_hat = (ln(s / k) + (mu_hat + sigma_hat ** 2 / 2) * t) / (sigma_hat * sqrt(t))
    d2_hat = d1_hat - sigma_hat * sqrt(t)
    if option_type == OptionType.Put:
        return exp(-r * t) * (k * norm_cdf(-d2_hat) - s * exp(mu_hat * t) * norm_cdf(-d1_hat))
    if option_type == OptionType.Call:
        return exp(-r * t) * (s * exp(mu_hat * t) * norm_cdf(d1_hat) - k * norm_cdf(d2_hat))


if __name__ == '__main__':
    price = geometric_asian_option_price(100, 100, 3, 0.3, 0.05, 50, OptionType.Call)
    print(price)
