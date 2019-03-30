import functools
import operator
from collections import Counter

from bitly_api_functions import *
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)


@app.errorhandler(403)
def access_denied():
    message = {
        "status":  403,
        "message": "No access token supplied. Access denied: " + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp


@app.route("/bitly/clicks/average")
def get_average_clicks():
    if "access_token" not in request.args:
        return access_denied()
    else:
        token = request.args["access_token"]
        unit = request.args["unit"] if "unit" in request.args else "day"
        units = int(request.args["units"]) if "units" in request.args else 30
        default_user_group = get_default_user_group(token)
        bitlinks = get_bitlinks(token, default_user_group)
        clicks_per_bitlink = [get_country_clicks(token, bitlink, unit, units) for bitlink in bitlinks]
        summed_clicks = dict(functools.reduce(operator.add, map(Counter, clicks_per_bitlink)))
        return jsonify(average_clicks_per_country(summed_clicks, units))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
