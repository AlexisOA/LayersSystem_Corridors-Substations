import psycopg2
import numpy as np
from connection.database import get_connection, close_connection
from orm.lidarsource import Circuits, CircuitGeoms, CircuitGeomTypes
from sqlalchemy import func

class CircuitlineDAO:

    def __init__(self, session):
        self.session = session

    def getCircuitLineById(self, circuits):
        return self.session.query(Circuits.mnemonico.label('id'),
                                    func.ST_AsText(func.ST_Transform(CircuitGeoms.geom, 3857)).label('geom_text'),
                                  # func.ST_AsText(CircuitGeoms.geom).label('geom_text'),
                                     ).join(CircuitGeoms,CircuitGeoms.circuitid == Circuits.id
                                    ).join(CircuitGeomTypes,CircuitGeomTypes.id == CircuitGeoms.geomtypeid
                                           ).filter(CircuitGeomTypes.name == "Tower_String").filter(Circuits.id == circuits).all()

    def runQueryById(self, query, id):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, (id,))
            conn.commit()
            return cur.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error: ", error)
        finally:
            if conn:
                close_connection(conn)

    def numbersOfCircuitslines(self, id):
        query = """
        select ST_NumGeometries(geom) from circuitsview 
        inner join circuitgeoms on (circuitgeoms.circuitid= circuitsview.circuitid) 
        inner join circuitgeomtypes on (circuitgeomtypes.id = circuitgeoms.geomtypeid)
        where regionname = 'CENTRO' AND name = 'Tower_String' AND circuitsview.circuitid=%s;
        """
        res = self.runQueryById(query, id)
        return res[0]

    def getCircuitlineById(self, id, numberOfCircuits):
        query = """
        with lines as(
        select ST_Astext(ST_GeometryN(geom, %s)) as geom from circuitsview 
        inner join circuitgeoms on (circuitgeoms.circuitid= circuitsview.circuitid) 
        inner join circuitgeomtypes on (circuitgeomtypes.id = circuitgeoms.geomtypeid)
        where regionname = 'CENTRO' AND name = 'Tower_String' AND circuitsview.circuitid=%s
        ),
        lines_points as(
        SELECT ST_AsText(
           ST_PointN(
              geom,
              generate_series(1, ST_NPoints(geom))
           )) as points FROM lines
    
        )
        SELECT ARRAY[ST_X(points), ST_Y(points), ST_Z(points)] from lines_points;
        """
        conn = get_connection()
        cur = conn.cursor()
        list_points = []
        for i in range(1, numberOfCircuits + 1):
            cur.execute(query, (i, id))
            points = cur.fetchall()
            list_points.append(np.array(points).flatten())
        lines = np.array(list_points, dtype=object)
        return lines

    # def getDataCircuitLineByID(self, lines, id):
    #     query = """
    #     select circuitmnemonico from circuitsview
    #         inner join circuitgeoms on (circuitgeoms.circuitid= circuitsview.circuitid)
    #         inner join circuitgeomtypes on (circuitgeomtypes.id = circuitgeoms.geomtypeid)
    #         where regionname = 'CENTRO' AND name = 'Tower_String' AND circuitsview.circuitid=%s
    #     """
    #     conn = get_connection()
    #     cur = conn.cursor()
    #     cur.execute(query, (id, ))
    #     points = cur.fetchone()

