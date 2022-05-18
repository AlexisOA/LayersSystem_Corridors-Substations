import psycopg2
import numpy as np
from connection.database import get_connection, close_connection
from orm.lidarsource import Circuits, CircuitGeoms, CircuitGeomTypes
from sqlalchemy import func


class TowerLineDao:


    def runQueryById(self, query, circuitid, hiphotesis_id):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, (circuitid,hiphotesis_id))
            conn.commit()
            return cur.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)
        finally:
            if conn:
                close_connection(conn)

    def TowerLineByCircuitAndHipothesis(self, circuit_id, hipothesis_id):
        query = """
        select
        electricspans.id as electricspanid,
        spanhipothesisgeoms.id as spanhipothesisgeomsid,
        ST_astext(ST_Transform(spanhipothesisgeoms.geom, 3857)),
        hipothesis.wind,
        hipothesis.temperature,
        hipothesis.longname,
        hipothesis.name,
        year,
        spanhipothesisgeoms.phase
        from spanhipothesisgeoms
        inner join years on (years.id = spanhipothesisgeoms.yearid) 
        inner join hipothesis on(hipothesis.id = spanhipothesisgeoms.hipothesisid) 
        inner join electricspans on(electricspans.id = spanhipothesisgeoms.electricspanid) 
        inner join circuits on(circuits.id = electricspans.circuitid) 
        where circuits.id=%s and hipothesis.id=%s
        and spanhipothesisgeoms.geom IS NOT NULL;
        """
        res = self.runQueryById(query, circuit_id, hipothesis_id)
        return res

