from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table, Numeric, Boolean
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# SmallInteger

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
    morerestrictiveconductorid = Column(Integer)
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
    spansource = relationship('SpanHipothesisGeoms', backref='spansource', lazy=True)
    electricspan = relationship('ElectricSpans', backref='electricspan', lazy=True)


class CircuitGeoms(Base):
    __tablename__ = 'circuitgeoms'
    id = Column(Integer, primary_key=True)
    geomtypeid = Column(Integer, ForeignKey('circuitgeomtypes.id'))
    circuitid = Column(Integer, ForeignKey('circuits.id'))
    yearid = Column(Integer)
    geom = Column(Geometry('POINT'))


class CircuitGeomTypes(Base):
    __tablename__ = 'circuitgeomtypes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    circuitgeoms = relationship('CircuitGeoms', backref='circuitgeoms', lazy=True)


class SpanHipothesisGeoms(Base):
    __tablename__ = 'spanhipothesisgeoms'
    id = Column(Integer, primary_key=True)
    hipothesisid = Column(Integer, ForeignKey('hipothesis.id'))
    electricspanid = Column(Integer, ForeignKey('electricspans.id'))
    phase = Column(Integer)
    geom = Column(Geometry('LINESTRING'))
    yearid = Column(Integer, ForeignKey('years.id'))
    circuitid = Column(Integer, ForeignKey('circuits.id'))


class Year(Base):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    yearsource = relationship('SpanHipothesisGeoms', backref='yearsource', lazy=True)


class ElectricSpans(Base):
    __tablename__ = 'electricspans'
    id = Column(Integer, primary_key=True)
    circuitid = Column(Integer, ForeignKey('circuits.id'))
    beginpylonid = Column(Integer)
    endpylonid = Column(Integer)
    ut = Column(Text)


class Hipothesis(Base):
    __tablename__ = 'hipothesis'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    longname = Column(Text)
    wind = Column(Integer)
    temperature = Column(Numeric)
