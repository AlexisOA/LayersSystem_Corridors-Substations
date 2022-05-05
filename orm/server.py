from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

Base = declarative_base()


class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    server = Column(Text)
    port = Column(Integer)

    lidarsource = relationship('LidarSource', backref='lidarsources', lazy=True)