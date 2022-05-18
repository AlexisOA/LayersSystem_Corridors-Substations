from connection.database import get_session
from orm.circuits_pylon_xref import CircuitsPylonsXref
from orm.companies import Company
from orm.companies_countries_xref import CompaniesCountriesXref
from orm.lidarsource import LidarSource, Circuits, Server, DistanceIncidences, Hipothesis, DistanceSeverities, Year, \
    ElectricSpans, DistanceIncidencesRanges, DistanceIncidenceTypes
from orm.pylons import Country, Region, Area, Pylons
from sqlalchemy import func


class DistanceIncidenceDAO:

    def __init__(self, session):
        self.session = session

    def getAnomalysByCircuitID(self, circuit_id):
        return self.session.query(
            func.ST_AsText(func.ST_Transform(func.ST_SetSrid(DistanceIncidences.grouppoints, 4326), 3857)).label('geom_secondary'),
            func.ST_AsText(func.ST_Transform(DistanceIncidences.geom, 3857)).label('geom_main_text'),
            DistanceIncidences.id.label("anomalyid"),
            Circuits.id.label('circuitid'),
            Circuits.mnemonico.label('circuitname'),
            DistanceIncidences.hipothesisid.label('hipothesisid'),
            Hipothesis.name.label('hipothesisname'),
            DistanceSeverities.id.label('severityid'),
            DistanceSeverities.name.label('severityname'),
            Year.id.label('yearid'),
            Year.year.label('yearname')
        ).join(ElectricSpans,
               DistanceIncidences.spanid == ElectricSpans.id
               ).join(Circuits,
                      ElectricSpans.circuitid == Circuits.id
                      ).join(DistanceIncidencesRanges, DistanceIncidencesRanges.id == DistanceIncidences.distanceincidencerangesid
                             ).join(DistanceIncidenceTypes, DistanceIncidencesRanges.distanceincidencetypeid == DistanceIncidenceTypes.id
                                    ).join(DistanceSeverities, DistanceIncidencesRanges.distanceseverityid == DistanceSeverities.id
                                           ).join(Hipothesis,
                                                  DistanceIncidences.hipothesisid == Hipothesis.id
                                                  ).join(Year, Year.id == DistanceIncidences.yearid
                                                         ).filter(Circuits.id == circuit_id).filter(DistanceIncidences.grouppoints.isnot(None)).all()

