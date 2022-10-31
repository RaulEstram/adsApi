from flask import Flask, Response, send_file
from flask_restful import Api
from flask_cors import CORS

from resources.ads import Ads
from resources.articles import Article, Articles
from resources.users import User, UserArticle
from resources.home import Home
from resources.downloads import Downloads, Queries

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/")
def hello():
    return "hola desde api"


api.add_resource(Ads, '/search/<string:key>')
api.add_resource(Article, '/article')
api.add_resource(Articles, '/articles')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserArticle, '/userarticle')
api.add_resource(Home, '/home')
api.add_resource(Downloads, "/downloads/<string:filename>")
api.add_resource(Queries, "/queries")

if __name__ == "__main__":
    app.run(debug=True)



