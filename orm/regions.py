from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Table
from datetime import datetime

from sqlalchemy.future import engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import ClauseElement, Executable

Base = declarative_base()


class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    countryid = Column(Integer, ForeignKey('countries.id'))


