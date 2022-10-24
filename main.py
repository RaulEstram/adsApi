from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.ads import Ads
from resources.articles import Article, Articles
from resources.users import User, UserArticle
from resources.home import Home

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/hola")
def hello():
    return "hola desde api"


api.add_resource(Ads, '/search/<string:key>')
api.add_resource(Article, '/article')
api.add_resource(Articles, '/articles')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserArticle, '/userarticle')
api.add_resource(Home, '/home')

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run()

