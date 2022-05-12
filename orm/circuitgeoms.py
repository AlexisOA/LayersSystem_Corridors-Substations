from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table
from datetime import datetime

from sqlalchemy.future import engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import ClauseElement, Executable

Base = declarative_base()


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
