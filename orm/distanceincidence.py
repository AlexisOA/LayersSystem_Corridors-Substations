from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Numeric
from datetime import datetime

from sqlalchemy.orm import relationship

Base = declarative_base()


class DistanceIncidences(Base):
    __tablename__ = 'distanceincidences'
    id = Column(Integer, primary_key=True)
    aerolaserid = Column(Integer)
    x = Column(Numeric)
    y = Column(Numeric)
    z = Column(Numeric)
    date = Column(DateTime(), default=datetime.now())
    temperature = Column(Numeric)
    windspeed = Column(Numeric)
    winddirection = Column(Text)
    result = Column(Text)
    l1 = Column(Numeric)
    l2 = Column(Numeric)
    distance = Column(Numeric)
    notes = Column(Text)
    geom = Column(Geometry('POINT'))
    distanceincidencer = Column(Integer)
    spanid = Column(Integer, ForeignKey('spans.id'))
    hipothesisid = Column(Integer, ForeignKey('hipothesis.id'))
    grouppoints = Column(Geometry('MULTIPOINT'))
    yearid = Column(Integer, ForeignKey('years.id'))
