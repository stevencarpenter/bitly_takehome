from flask import Flask
from flask_restful import reqparse, Api, Resource


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('bitlink')


class AverageClicksPerCountry(Resource):
    def get(self):
        return

# add route
api.add_resource(AverageClicksPerCountry, '/bitly/')

if __name__ == '__main__':
    app.run(debug=True)
