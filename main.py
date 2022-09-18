from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.ads import Ads
from resources.articles import Article, Articles
from resources.users import User, UserArticle

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Ads, '/search/<string:key>')
api.add_resource(Article, '/article')
api.add_resource(Articles, '/articles')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserArticle, '/userarticle')

if __name__ == "__main__":
    app.run(debug=True, port=8080)


