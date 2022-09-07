from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.ads import Ads
from resources.articles import Article

from libs.strings import getText

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Ads, '/search/<string:key>')
api.add_resource(Article, '/article')

if __name__ == "__main__":
    app.run(debug=True, port=8080)
