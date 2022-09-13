from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.ads import Ads
from resources.articles import Article
from resources.users import User

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Ads, '/search/<string:key>')
api.add_resource(Article, '/article')
api.add_resource(User, '/user/<string:user_id>')

if __name__ == "__main__":
    app.run(debug=True, port=8080)
