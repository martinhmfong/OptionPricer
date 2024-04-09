import json
import logging

from flask import Flask, request, jsonify

from common.constants import SimulationResult, OptionType
from pricer import calculate

app = Flask(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


@app.route('/price/<string:pricer>', methods=['GET', 'POST'])
def get_price(pricer: str):
    params = json.loads(request.data)
    params['option_type'] = OptionType(params['option_type'])
    logging.info(f'Received request for {pricer}: {params}')
    result = calculate(pricer, **params)
    response = SimulationResult(result) if isinstance(result, float) else result
    logging.info(f'Returned response: {response}')
    return jsonify(response.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)
