from flask_restful import Resource
from flask import request

from libs.database import DBManager
from libs.strings import getText
from libs.queries import getQuery


class Article(Resource):

    def _getDataArticules(self, res: dict):
        keys = res.keys()
        author = res['authors'] if 'authors' in keys and res['authors'] != '' else None
        title = res['title'] if 'title' in keys and res['title'] != '' else None
        pub = res['pub'] if 'pub' in keys and res['pub'] != '' else None
        url = res['url'] if 'url' in keys and res['url'] != '' else None
        bibcode = res['bibcode'] if 'bibcode' in keys and res['bibcode'] != '' else None
        doi = res['doi'] if 'doi' in keys and res['doi'] != '' else None
        firstPage = res['firstpage'] if 'firstpage' in keys and res['firstpage'] != '' else None
        lastPage = res['lastpage'] if 'lastpage' in keys and res['lastpage'] != '' else None
        volume = res['volume'] if 'volume' in keys and res['volume'] != '' else None
        year = res['year'] if 'year' in keys and res['year'] != '' else None
        id_article = res['id'] if 'id' in keys and res['id'] != '' else None
        if id_article is None:
            values = (author, title, pub, bibcode, doi, firstPage, lastPage, volume, year,)
        else:
            values = (author, title, pub, bibcode, doi, firstPage, lastPage, volume, year, id_article)
        return values, title

    def post(self):
        db = DBManager()
        if db.getStatus()["status"]:
            res = request.get_json()
            values, title = self._getDataArticules(res)
            response = db.query(getQuery("INSERT_ARTICLE"), values)
            if response["status"]:
                return {"status": True, "message": getText("ARTICLE:SUCCESSFUL_POST").format(title=title)}
            else:
                return {"status": False, "error": response['error']}
        else:
            return {"status": False, "error": db.getStatus()["error"]}

    def put(self):
        db = DBManager()
        if db.getStatus()["status"]:
            res = request.get_json()
            values, title = self._getDataArticules(res)
            response = db.query(getQuery("UPDATE_ARTICLE"), values)
            if response["status"]:
                return {"status": True, "message": getText("ARTICLE:SUCCESSFUL_UPDATE").format(title=title)}
            else:
                return {"status": False, "error": response['error']}
        else:
            return {"status": False, "error": db.getStatus()["error"]}
