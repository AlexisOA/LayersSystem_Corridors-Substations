from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table, Numeric, Boolean
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

#SmallInteger

class LidarSource(Base):
    __tablename__ = 'lidarsources'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    path = Column(Text)
    circuitid = Column(Integer, ForeignKey('circuits.id'))
    serverid = Column(Integer, ForeignKey('servers.id'))
    yearid = Column(Integer, ForeignKey('years.id'))


class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    server = Column(Text)
    port = Column(Integer)
    lidarsource = relationship('LidarSource', backref='servers', lazy=True)

class Circuits(Base):
    __tablename__ = 'circuits'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    mnemonico = Column(Text)
    ckt = Column(Numeric)
    sseeoptoinitial = Column(Text)
    sseeoptofinal = Column(Text)
    issubstation = Column(Boolean)
    tcircuitidentificator = Column(Boolean)
    tale = Column(Text)
    direction = Column(Text)
    tension = Column(Text)
    maxtension = Column(Text)
    desigtension = Column(Text)
    circuittype = Column(Text)
    energytype = Column(Text)
    nettype = Column(Text)
    date = Column(DateTime(), default=datetime.now())
    state = Column(Text)
    longitudepercoordinate = Column(Numeric)
    projectlongitude = Column(Numeric)
    sharedlongitude = Column(Numeric)
    retributionlongitude = Column(Numeric)
    subterrainlongitude = Column(Numeric)
    submarinelongitude = Column(Numeric)
    morefrequencyconf = Column(Text)
    morerestrictiveconductorid =  Column(Integer)
    springmva = Column(Numeric)
    summermva = Column(Numeric)
    autommva = Column(Numeric)
    wintermva = Column(Numeric)
    springelement = Column(Text)
    summerelement = Column(Text)
    automelement = Column(Text)
    winterelement = Column(Text)
    directresistence = Column(Numeric)
    directreactance = Column(Numeric)
    directsubceptance = Column(Numeric)
    homopolarresistence = Column(Numeric)
    homopolarreactance = Column(Numeric)
    homopolarsubceptance = Column(Numeric)
    instalationcode = Column(Integer)
    internationalconection = Column(Boolean)
    internationalinfluence = Column(Boolean)
    ssaainfluence = Column(Boolean)
    utmcoord = Column(Text)
    pss = Column(Text)
    b1 = Column(Text)
    b2 = Column(Text)
    b3 = Column(Text)
    aditionalinfo = Column(Text)
    paasigpm = Column(Boolean)
    lastownerid = Column(Integer)
    regulationid = Column(Integer)
    stationid = Column(Integer)

    lidarsource = relationship('LidarSource', backref='lidarsources', lazy=True)
