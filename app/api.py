import functools
import operator
from collections import Counter

from bitly_api_functions import *
from flask import Flask, jsonify
from flask import request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.errorhandler(403)
def access_denied(error=None):
    message = {
        "status":  403,
        "message": "No access token supplied. Access denied: " + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp


@app.route("/bitly/clicks/average")
def get_average_clicks():
    if "access_token" in request.args:
        token = request.args["access_token"]
        default_user_group = get_default_user_group(token)
        bitlinks = get_bitlinks(token, default_user_group)
        clicks_per_bitlink = [get_country_clicks(token, bitlink) for bitlink in bitlinks]
        return jsonify(
            average_clicks_per_country(dict(functools.reduce(operator.add, map(Counter, clicks_per_bitlink))), 30))
    else:
        return access_denied()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
