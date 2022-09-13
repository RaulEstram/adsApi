from flask_restful import Resource

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
                return {"status": False, "message": getText("USER:USER_EXIST")}
            else:
                return {"status": False, "error": response['error']}
        else:
            return {"status": False, "error": db.getStatus()["error"]}
