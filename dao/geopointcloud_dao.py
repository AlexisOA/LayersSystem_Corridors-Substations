from connection.database import get_session
from orm.lidarsource import LidarSource, Circuits, Server


class GeoPointcloudDAO():

    def __init__(self, session):
        self.session = session

    def getPointcloudFromCircuit(self, circuits):
        return self.session.query(LidarSource.path.label('path'),
                                  Circuits.mnemonico.label('circuitename'),
                                  Server.name.label('servername')
                                  ).join(LidarSource, LidarSource.circuitid == Circuits.id
                                         ).join(Server, LidarSource.serverid == Server.id
                                                ).filter(Circuits.id == circuits.circuitid).all()

