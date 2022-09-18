from flask_restful import Resource
from flask import request

from libs.database import DBManager
from libs.strings import getText
from libs.queries import getQuery


class DataArticles:

    @staticmethod
    def getDataArticules(res: dict):
        keys = res.keys()
        user = res['user_id'] if 'user_id' in keys and res['user_id'] != '' else None
        author = res['authors'] if 'authors' in keys and res['authors'] != '' else None
        title = res['title'] if 'title' in keys and res['title'] != '' else None
        pub = res['pub'] if 'pub' in keys and res['pub'] != '' else ''
        url = res['url'] if 'url' in keys and res['url'] != '' else ''
        bibcode = res['bibcode'] if 'bibcode' in keys and res['bibcode'] != '' else None
        doi = res['doi'] if 'doi' in keys and res['doi'] != '' else None
        fpage = res['page_range'].split("-")[0] if 'page_range' in keys and res['page_range'] != '' else ''
        lpage = res['page_range'].split("-")[1] if 'page_range' in keys and '-' in res['page_range'] else ''
        volume = res['volume'] if 'volume' in keys and res['volume'] != '' else ''
        year = res['year'] if 'year' in keys and res['year'] != '' else ''
        id = res['id_article'] if 'id_article' in keys and res['id_article'] != '' else ''
        page_count = res['page_count'] if 'page_count' in keys and res['page_count'] != '' else ''
        update = res['update'] if 'update' in keys and res['update'] != '' else None
        if user and update is None:
            values = (user, author, title, pub, url, fpage, lpage, bibcode, doi, volume, year, id, page_count)
            return {"status": True, "values": values, "title": title}
        elif user and update:
            values = (author, title, pub, url, fpage, lpage, bibcode, doi, volume, year, id, page_count, bibcode, user)
            return {"status": True, "values": values, "title": title}
        else:
            return {"status": False, "error": getText("ARTICLE:NO_DATA")}


class Article(Resource):

    def post(self):
        db = DBManager()
        if db.getStatus()["status"]:
            res = request.get_json()
            data = DataArticles.getDataArticules(res)
            if data['status']:
                response = db.query(getQuery("INSERT_ARTICLE"), data['values'])
                if response["status"]:
                    return {"status": True, "message": getText("ARTICLE:SUCCESSFUL_POST").format(title=data['title'])}
                else:
                    return {"status": False, "error": response['error']}
            else:
                return {"status": False, "error": data['error']}
        else:
            return {"status": False, "error": db.getStatus()["error"]}

    def put(self):
        db = DBManager()
        if db.getStatus()["status"]:
            res = request.get_json()
            data = DataArticles.getDataArticules(res)
            if data['status']:
                response = db.query(getQuery("UPDATE_ARTICLE"), data['values'])
                if response["status"]:
                    return {"status": True, "message": getText("ARTICLE:SUCCESSFUL_UPDATE").format(title=data['title'])}
                else:
                    return {"status": False, "error": response['error']}
            else:
                return {"status": False, "error": data['error']}
        else:
            return {"status": False, "error": db.getStatus()["error"]}


class Articles(Resource):

    def post(self):
        db = DBManager()
        res = request.get_json()
        keys = res.keys()
        info = {"status": True, "inserts": 0, "updates": 0, "errors": 0}

        if not db.getStatus()["status"]:
            return {"status": False, "error": db.getStatus()["error"]}
        if 'user_id' not in keys or 'data' not in keys:
            return {"status": False, "error": "Faltan datos"}
        if len(res['data']) == 0:
            return {"status": False, "error": "No hay articulos para guardar"}

        for value in res['data'].values():
            response = db.query(getQuery("USER_HAVE_ARTICLE"), (res['user_id'], value['bibcode']))
            if not response["status"]:
                info["errors"] += 1
                continue
            response = db.getResults()

            if len(response) == 0:
                value['user_id'] = res['user_id']
                data = DataArticles.getDataArticules(value)
                if not data['status']:
                    info["errors"] += 1
                    continue
                response = db.query(getQuery("INSERT_ARTICLE"), data['values'])
                if not response["status"]:
                    info["errors"] += 1
                    continue
                info["inserts"] += 1
            else:
                value['user_id'] = res['user_id']
                value['update'] = True
                data = DataArticles.getDataArticules(value)
                if not data['status']:
                    info["errors"] += 1
                    continue
                response = db.query(getQuery("UPDATE_ARTICLE"), data['values'])
                if not response["status"]:
                    info["errors"] += 1
                    continue
                info["updates"] += 1
        return info
