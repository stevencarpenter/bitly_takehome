from flask import Flask
from flask_restful import reqparse, Api, Resource

from app.bitly_api_functions import *

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('bitlink')


class Bitly(Resource):
    def get(self):
        return

# add route
api.add_resource(Bitly, '/bitly')

if __name__ == '__main__':
    app.run(debug=True)
