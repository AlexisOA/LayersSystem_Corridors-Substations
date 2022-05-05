from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table
from datetime import datetime

from sqlalchemy.future import engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import ClauseElement, Executable

Base = declarative_base()


class CircuitsPylonsXref(Base):
    __tablename__ = 'circuits_pylons_xref'
    circuitid = Column(Integer, primary_key=True)
    pylonid = Column(Integer, primary_key=True)


