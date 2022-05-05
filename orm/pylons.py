from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table, Numeric
from datetime import datetime

from sqlalchemy.future import engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import ClauseElement, Executable

Base = declarative_base()


class Pylons(Base):
    __tablename__ = 'pylons'
    id = Column(Integer, primary_key=True)
    code = Column(Text)
    type = Column(Text)
    ut = Column(Text)
    plate = Column(Text)
    ordernumber = Column(Integer)
    suspensionpylon = Column(Text)
    segurity = Column(Text)
    aislatormaterial = Column(Text)
    aislatortype = Column(Text)
    aislatorsubtype = Column(Text)
    longitude = Column(Numeric)
    conductorperphase = Column(Numeric)
    designtemperature = Column(Numeric)
    angle = Column(Numeric)
    x = Column(Numeric)
    y = Column(Numeric)
    z = Column(Numeric)
    corrosion = Column(Text)
    pylonphase = Column(Text)
    notes = Column(Text)
    pesdate = Column(DateTime(), default=datetime.now())
    installationdate = Column(DateTime(), default=datetime.now())
    nextspancode = Column(Integer)
    wireid = Column(Integer, ForeignKey('wires.id'))
    areaid = Column(Integer, ForeignKey('areas.id'))
    regulationid = Column(Integer, ForeignKey('regulations.id'))
    geom = Column(Geometry('POINT'))


class Area(Base):
    __tablename__ = 'areas'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    regionid = Column(Integer, ForeignKey('regions.id'))


class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    countryid = Column(Integer, ForeignKey('countries.id'))


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(Text)


