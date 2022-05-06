import ast

from connection.database import get_session
from dao.circuitview_dao import CircuitViewDao
from dao.geopointcloud_dao import GeoPointcloudDAO
from dto.circuits_dto import CircuitsDTO
from dto.composite.layers_composite import LayersComposite
from dto.composite.scene import Scene
from dto.composite.scene_composite import ScenesComposite
from dto.geopointcloud_dto import GeoPointcloudDTO
from dto.scenemap_dto import SceneMap3857
from orm.circuits_pylon_xref import CircuitsPylonsXref
from orm.circuitsview import CircuitView
from orm.companies import Company
from orm.companies_countries_xref import CompaniesCountriesXref
# from orm.lidarsource import LidarSource, Circuits, Server
# from orm.pylons import Pylons, Area, Country, Region
from orm.years import Year
import json


if __name__ == '__main__':
    session = get_session()

    scene_json = SceneMap3857()
    composite_scene = ScenesComposite()
    circuitsview = CircuitViewDao(session).getCircuitsForZone('CENTRO')
    scene_main = Scene()
    scene_main.add_scenes(scene_json)
    c = 0
    for circuits in circuitsview:
        circ = CircuitsDTO(circuits)
        # Get all pointclouds from circuit
        lidar_query = GeoPointcloudDAO(session).getPointcloudFromCircuit(circuits)
        #Iterate pointcloud and serialize to GeoPointCloudDTO
        for lidar in lidar_query:
            if lidar:
                geo = GeoPointcloudDTO(lidar)
                circ.add_layers(geo)

        scene_main.add_scenes(circ)

    data_string = scene_main.generateSceneJSON()
    app_json = json.dumps(data_string)
    print(app_json)