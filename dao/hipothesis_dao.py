import psycopg2
import numpy as np
from connection.database import get_connection, close_connection
from orm.lidarsource import Circuits, CircuitGeoms, CircuitGeomTypes
from sqlalchemy import func


class HipothesisDAO:

    def runQuery(self, query, one_param):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, (one_param,))
            conn.commit()
            return cur.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)
        finally:
            if conn:
                close_connection(conn)

    def getHipothesis(self, number_towerlines):
        #Query for three types of hipothesis, change number LIMIT for show one, two or three hipothesis
        query = """
        SELECT * FROM hipothesis LIMIT %s;
        """
        res = self.runQuery(query, number_towerlines)
        return res
