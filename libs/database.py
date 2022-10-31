import mysql.connector as db
from mysql.connector import errorcode
from libs.strings import getText


class DBManager:
    config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'database': 'ads'
    }

    def __init__(self):
        try:
            self._connection = db.connect(**DBManager.config)
            self._cursor = self._connection.cursor(buffered=True)
            self._status = {"status": True}
        except db.Error as error:
            if error.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
                self._status = {"status": False, "error": getText("DBM:ERROR_CONNECTION_LOGIN")}
            elif error.errno == errorcode.CR_UNKNOWN_HOST:
                self._status = {"status": False, "error": getText("DBM:ERROR_CONNECTION_HOST")}
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                self._status = {"status": False, "error": getText("DBM:ERROR_CONNECTION_DB")}
            else:
                self._status = {"status": False, "error": getText("DBM:ERROR_CONNECTION").format(error=error.msg)}

    def getStatus(self):
        return self._status

    def getResults(self):
        return self._cursor.fetchall()

    def query(self, query: str, values=()) -> dict:
        try:
            self._cursor.execute(query, values)
            self._connection.commit()
            return {"status": True, "message": getText("DBM:SUCCESSFUL_QUERY")}
        except db.Error as error:
            if error.errno == errorcode.ER_NO_SUCH_TABLE:
                return {"status": False, "error": getText("DBM:ERROR_QUERY_TABLE")}
            elif error.errno == errorcode.ER_PARSE_ERROR:
                return {"status": False, "error": getText("DBM:ERROR_QUERY_SYNTAX")}
            elif error.errno == errorcode.ER_BAD_FIELD_ERROR:
                return {"status": False, "error": getText("DBM:ERROR_QUERY_COLUMN")}
            else:
                return {"status": False, "error": getText("DBM:ERROR_QUERY").format(error=error.msg)}
