import psycopg2
import numpy as np

from connection.database import get_connection, close_connection
from dao.circuitline_dao import CircuitlineDAO

conn= None
try:
    # conn = psycopg2.connect(dbname="AeDaliaDb", user="aedaliauser", password="aedaliapassword", host="192.168.7.4")
    consulta = """
    select *, ST_Astext(geom) from circuitsview 
    inner join circuitgeoms on (circuitgeoms.circuitid= circuitsview.circuitid) 
    inner join circuitgeomtypes on (circuitgeomtypes.id = circuitgeoms.geomtypeid)
    where regionname = 'CENTRO' AND name = 'Tower_String' AND circuitsview.circuitid = 244;
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(consulta)
    conn.commit()
    res = cur.fetchall()
    for i in res:
        print(i[-1])
        linestring_z = str(i[-1]).replace("GEOMETRYCOLLECTION Z (", "")
        print(linestring_z[linestring_z.find("(") + 1: linestring_z.find(")")].split(","))
        # print(str(i[-1]).split(","))
        # print(str(i[-1]).replace("GEOMETRYCOLLECTION Z ", "").replace("LINESTRING Z ", "").replace("(", "").replace(")", "").split(","))
except (Exception, psycopg2.Error) as error:
    print("Error: " , error)
finally:
    if conn:
        close_connection(conn)
