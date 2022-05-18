from connection.database import get_session
from orm.circuits_pylon_xref import CircuitsPylonsXref
from orm.companies import Company
from orm.companies_countries_xref import CompaniesCountriesXref
from orm.lidarsource import LidarSource, Circuits, Server
from orm.pylons import Country, Region, Area, Pylons


class CircuitViewDao:

    def __init__(self, session):
        self.session = session

    def getCircuitsForZone(self, zone):
        return self.session.query(
            Company.id.label('companyid'),
            Company.name.label('companyname'),
            Country.id.label('countryid'),
            Country.name.label('countryname'),
            Region.id.label('regionid'),
            Region.name.label('regionname'),
            Area.id.label('areaid'),
            Area.name.label('areaname'),
            CircuitsPylonsXref.circuitid.label('circuitid'),
            Circuits.mnemonico.label('circuitname')
        ).join(CircuitsPylonsXref,
               CircuitsPylonsXref.circuitid == Circuits.id, isouter=True
               ).join(Pylons,
                      CircuitsPylonsXref.pylonid == Pylons.id, isouter=True
                      ).join(Area, Area.id == Pylons.areaid, isouter=True
                             ).join(Region, Region.id == Area.regionid, isouter=True
                                    ).join(Country, Country.id == Region.countryid, isouter=True
                                           ).join(CompaniesCountriesXref,
                                                  CompaniesCountriesXref.countryid == Country.id,
                                                  isouter=True
                                                  ).join(Company, Company.id == CompaniesCountriesXref.companyid,
                                                         isouter=True
                                                         ).distinct().order_by(CircuitsPylonsXref.circuitid).all()

    def getCircuitsNewForZone(self, zone):
        return self.session.query(Circuits
                                  ).join(CircuitsPylonsXref,
                                         CircuitsPylonsXref.circuitid == Circuits.id
                                         ).join(Pylons,
                                                CircuitsPylonsXref.pylonid == Pylons.id
                                                ).join(Area, Area.id == Pylons.areaid, isouter=True
                                                       ).join(Region, Region.id == Area.regionid, isouter=True
                                                              ).distinct().filter(Region.name == zone).order_by(
            Circuits.id).all()
