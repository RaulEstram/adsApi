from flask_restful import Resource
from flask import request, send_file
from datetime import datetime

from libs.database import DBManager
from libs.queries import getQuery
from resources.articles import DataArticles


class Downloads(Resource):

    def get(self, filename):
        return send_file(f"files/{filename}", as_attachment=True)


class Queries(Resource):

    def post(self):
        db = DBManager()
        res = request.get_json()
        keys = res.keys()
        queries = ""
        if not db.getStatus()["status"]:
            return {"status": False, "error": db.getStatus()["error"]}
        if 'user_id' not in keys or 'data' not in keys:
            return {"status": False, "error": "Faltan datos"}
        if len(res['data']) == 0:
            return {"status": False, "error": "No hay articulos para guardar"}

        for value in res['data'].values():
            response = db.query(getQuery("USER_HAVE_ARTICLE"), (res['user_id'], value['bibcode']))
            if not response["status"]:
                continue
            response = db.getResults()

            # insert
            if len(response) == 0:
                value['user_id'] = res['user_id']
                data = DataArticles.getDataArticules(value)
                if not data['status']:
                    continue
                query = getQuery("INSERT_ARTICLE_QUERY").replace("'", '"').format(*data['values'])
                queries += query + "\n"
            else:
                value['user_id'] = res['user_id']
                value['update'] = True
                data = DataArticles.getDataArticules(value)
                if not data['status']:
                    continue
                query = getQuery("UPDATE_ARTICLE_QUERY").replace("'", '"').format(*data['values']) + "\n"
                queries += query

        try:
            time = datetime.now()
            filename = f"queries_{time.timestamp()}".replace(".", "_") + ".sql"
            with open(f"files/{filename}", 'w') as temp_file:
                temp_file.write(queries)
        except Exception as error:
            print(error)
            return {"status": False, "error": "Error al crear el archivo sql"}

        return {"status": True, "filename": filename}
