from flask_restful import Resource
from flask import request

from libs.database import DBManager
from libs.queries import getQuery
from libs.strings import getText


class User(Resource):

    def get(self, user_id):
        db = DBManager()
        if db.getStatus()["status"]:
            response = db.query(getQuery("IS_USER_EXIST"), (user_id,))
            if response["status"] and len(db.getResults()):
                return {"status": True, "message": getText("USER:USER_EXIST")}
            elif response["status"] and len(db.getResults()) == 0:
                return {"status": False, "message": getText("USER:USER_NOT_EXIST")}
            else:
                return {"status": False, "error": response['error']}
        else:
            return {"status": False, "error": db.getStatus()["error"]}


class UserArticle(Resource):

    def _getData(self, data: dict):
        keys = data.keys()
        user_id = data['user_id'] if 'user_id' in keys and data['user_id'] != '' else None
        bibcode = data['bibcode'] if 'bibcode' in keys and data['bibcode'] != '' else None
        values = (user_id, bibcode)
        if user_id and bibcode:
            return {"status": True, "values": values, "bibcode": bibcode}
        return {"status": False, "error": getText("USERARTICLE:NO_DATA")}

    def post(self):
        db = DBManager()
        if db.getStatus()["status"]:
            res = request.get_json()
            data = self._getData(res)
            if data['status']:
                response = db.query(getQuery("USER_HAVE_ARTICLE"), data['values'])
                if response["status"] and len(db.getResults()):
                    return {"status": True, "message": getText("USERARTICLE:USER_HAVE_ARTICLE")}
                elif response["status"] and len(db.getResults()) == 0:
                    return {"status": False, "message": getText("USERARTICLE:USER_HAVE_NOT_ARTICLE")}
                else:
                    return {"status": False, "error": response['error']}
            else:
                return {"status": False, "error": data['error']}
        else:
            return {"status": False, "error": db.getStatus()["error"]}
