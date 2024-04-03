import logging

from flask import Flask, request, jsonify

from common.constants import OptionType
from formula.european_options import european_option_price, european_option_implied_volatility

app = Flask(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


@app.route('/eu_price', methods=['POST'])
def eu_price():
    params = request.get_json()
    logging.info(f'Received request for eu_price: {params}')
    params['option_name'] = OptionType(params['option_name'])
    price = european_option_price(**params)
    return jsonify(price)


@app.route('/eu_implied_vol', methods=['POST'])
def eu_implied_vol():
    params = request.get_json()
    logging.info(f'Received request for eu_price: {params}')
    params['option_name'] = OptionType(params['option_name'])
    price = european_option_implied_volatility(**params)
    return jsonify(price)


if __name__ == '__main__':
    app.run(debug=True)
