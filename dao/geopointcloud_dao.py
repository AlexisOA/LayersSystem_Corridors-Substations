from connection.database import get_session
from orm.circuits_pylon_xref import CircuitsPylonsXref
from orm.lidarsource import LidarSource, Circuits, Server
from orm.pylons import Pylons, Area, Region


class GeoPointcloudDAO():

    def __init__(self, session):
        self.session = session

    def getPointcloudFromCircuit(self, circuits):
        return self.session.query(LidarSource.path.label('path'),
                                  Circuits.mnemonico.label('circuitname'),
                                  Server.name.label('servername')
                                  ).join(LidarSource, LidarSource.circuitid == Circuits.id
                                         ).join(Server, LidarSource.serverid == Server.id
                                                ).filter(Circuits.id == circuits.id).all()

    def test(self, circuits):
        return self.session.query(LidarSource.path.label('path'),
                                  Circuits.mnemonico.label('mnemonico'),
                                  Server.name.label('servername')
                                  ).join(CircuitsPylonsXref,
                                         CircuitsPylonsXref.circuitid == Circuits.id
                                         ).join(Pylons,
                                                CircuitsPylonsXref.pylonid == Pylons.id
                                                ).join(Area, Area.id == Pylons.areaid, isouter=True
                                                       ).join(Region, Region.id == Area.regionid, isouter=True
                                                              ).join(LidarSource, LidarSource.circuitid == Circuits.id
                                         ).join(Server, LidarSource.serverid == Server.id
                                                ).distinct().filter(Region.name == 'NOROESTE').filter(Circuits.id == circuits).order_by(Circuits.id).all()

