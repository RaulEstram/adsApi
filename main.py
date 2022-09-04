from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.ads import Ads

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Ads, '/search/<string:key>')

if __name__ == "__main__":
    app.run()