import psycopg2
import numpy as np
from connection.database import get_connection, close_connection
from orm.lidarsource import Circuits, CircuitGeoms, CircuitGeomTypes, ElectricSpans, SpanHipothesisGeoms, Hipothesis
from sqlalchemy import func


class TowerLineDao2:

    def __init__(self, session):
        self.session = session

    def getPylonsFromCircuit(self, circuit_id, hipothesis_id):
        return self.session.query(ElectricSpans.id.label('electricspan_id'),
                                  SpanHipothesisGeoms.id.label('spanhipothesis_id'),
                                  func.ST_AsText(func.ST_Transform(SpanHipothesisGeoms.geom, 3857)).label('geom_text'),
                                  Hipothesis.wind.label('wind'), Hipothesis.temperature.label('temperature'), Hipothesis.longname.label('longname'), Hipothesis.name.label('name'),
                                  SpanHipothesisGeoms.phase.label('phase')
                                  ).join(Hipothesis, Hipothesis.id == SpanHipothesisGeoms.hipothesisid
                                         ).join(ElectricSpans, ElectricSpans.id == SpanHipothesisGeoms.electricspanid
                                                ).join(
            Circuits, Circuits.id == ElectricSpans.circuitid
        ).filter(Circuits.id == circuit_id
                 ).filter(Hipothesis.id == hipothesis_id
                          ).filter(SpanHipothesisGeoms.geom.isnot(None)).all()

