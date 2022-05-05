from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table
from datetime import datetime

from sqlalchemy.future import engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import ClauseElement, Executable

Base = declarative_base()


class CircuitView(Base):
    __tablename__ = 'circuitsview'
    companyid = Column(Integer)
    companyname = Column(Text)
    countryid = Column(Integer)
    countryname = Column(Text)
    regionid = Column(Integer)
    regionname = Column(Text)
    areaid = Column(Integer)
    areaname = Column(Text)
    circuitid = Column(Integer, primary_key=True)
    circuitmnemonico = Column(Text)


