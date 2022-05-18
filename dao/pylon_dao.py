from orm.circuits_pylon_xref import CircuitsPylonsXref
from orm.lidarsource import LidarSource, Circuits, Server
from orm.pylons import Pylons
from sqlalchemy import func
class PylonDAO():

    def __init__(self, session):
        self.session = session

    def getPylonsFromCircuit(self, circuits):
        return self.session.query(Circuits.mnemonico.label('circuitname'),
                                  Pylons.id.label('id'),
                                  Pylons.code.label('code'),
                                  Pylons.type.label('type'),
                                  Pylons.ut.label('ut'),
                                  Pylons.plate.label('plate'),
                                  func.st_x(Pylons.geom).label('x'),
                                  func.st_y(Pylons.geom).label('y'),
                                  func.st_z(Pylons.geom).label('z'),
                                  func.ST_AsText(func.ST_Transform(Pylons.geom, 3857)).label('geom_text')
                                  ).join(CircuitsPylonsXref, CircuitsPylonsXref.circuitid == Circuits.id
                                         ).join(Pylons, CircuitsPylonsXref.pylonid == Pylons.id
                                                ).filter(Circuits.id == circuits.id).all()

