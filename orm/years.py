from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime

Base = declarative_base()


class Year(Base):
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)

    def __init__(self, id, year):
        self.year = year