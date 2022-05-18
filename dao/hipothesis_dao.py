import psycopg2
import numpy as np
from connection.database import get_connection, close_connection
from orm.lidarsource import Circuits, CircuitGeoms, CircuitGeomTypes
from sqlalchemy import func


class HipothesisDAO:

    def runQuery(self, query):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            return cur.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)
        finally:
            if conn:
                close_connection(conn)

    def getHipothesis(self):
        query = """
        SELECT * FROM hipothesis inner join years on (years.id = hipothesis.id);
        """
        res = self.runQuery(query)
        return res
