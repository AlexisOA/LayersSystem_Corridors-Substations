from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

Base = declarative_base()


class Spanhipothesisgeoms(Base):
    __tablename__ = 'spanhipothesisgeoms'
    id = Column(Integer, primary_key=True)
    hipothesisid = Column(Integer, ForeignKey('hipothesis.id'))
    electricspanid = Column(Integer, ForeignKey('electricspans.id'))
    phase = Column(Integer)
    geom = Column(Geometry('LINESTRING'))
    yearid = Column(Integer, ForeignKey('years.id'))
    circuitid = Column(Integer, ForeignKey('circuits.id'))
