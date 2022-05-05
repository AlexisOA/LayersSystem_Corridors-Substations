from connection.database import get_session
from dto.circuits_dto import CircuitsDTO
from dto.composite.layers_composite import LayersComposite
from dto.composite.scene_composite import ScenesComposite
from dto.geopointcloud_dto import GeoPointcloudDTO
from dto.scenemap_dto import SceneMap3857
from orm.circuits_pylon_xref import CircuitsPylonsXref
from orm.circuitsview import CircuitView
from orm.companies import Company
from orm.companies_countries_xref import CompaniesCountriesXref
from orm.lidarsource import LidarSource, Circuits, Server
from orm.pylons import Pylons, Area, Country, Region
from orm.years import Year

if __name__ == '__main__':
    session = get_session()
    # views = session.query(CircuitView).filter(CircuitView.regionname == 'CENTRO').all()

    # Return Corredores de la zona centro
    scene_json = SceneMap3857()
    composite_scene = ScenesComposite()


    circuitsview = session.query(
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
                                       ).join(CompaniesCountriesXref, CompaniesCountriesXref.countryid == Country.id,
                                              isouter=True
                                              ).join(Company, Company.id == CompaniesCountriesXref.companyid,
                                                     isouter=True
                                                     ).distinct().order_by(CircuitsPylonsXref.circuitid).filter(
        Region.name == 'CENTRO').all()

    # circuits_list = []
    # for circuits in circuitsview:
    #     circ = CircuitsDTO(circuits)
    #     circuits_list.append(circ)
    composite_scene.add(scene_json)
    composite_layer = LayersComposite()
    for circuits in circuitsview:
        #Tenemos un circuito de zona centro
        circ = CircuitsDTO(circuits)
        composite_scene.add(circ)

        lidar_query = session.query(LidarSource.path.label('path'),
                                    Circuits.mnemonico.label('circuitename'),
                                    Server.name.label('servername')
                                    ).join(LidarSource, LidarSource.circuitid == Circuits.id
                                           ).join(Server, LidarSource.serverid == Server.id
                                                  ).filter(Circuits.id == circuits.circuitid).all()
        #Get all pointclouds from circuit

        for lidar in lidar_query:
            if lidar:
                print()
                # print(GeoPointcloudDTO(lidar))

                # composite_layer.add(lidar)
                # circ.add(GeoPointcloudDTO(lidar))

        # composite_scene.add(circ)
        print(composite_scene.count())
        print(composite_scene.jsonRoot())
        # print(composite_layer.generateLayersJSON())
        break
