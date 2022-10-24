from flask_restful import Resource
from flask import render_template, make_response, request


class Home(Resource):

    def get(self):
        try:
            headers = {'Content-Type': 'text/html'}
            res = request.form['user_id']
            return make_response(render_template('index.html', user=res), 200, headers)
        except:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html', user=319), 200, headers)
