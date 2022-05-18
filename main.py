import numpy as np
from connection.database import get_session
from dao.circuitline_dao import CircuitlineDAO
from dao.circuitview_dao import CircuitViewDao
from dao.geopointcloud_dao import GeoPointcloudDAO
from dao.hipothesis_dao import HipothesisDAO
from dao.pylon_dao import PylonDAO
from dao.towerline_dao import TowerLineDao
from dao.towerline_dao_alchemy import TowerLineDao2
from dto.circuitlines_dto import CircuitLinesDTO
from dto.circuits_dto import CircuitsDTO
from dto.composite.scene_composite import ScenesComposite
from dto.geometries.linestring_collect import LineStringCollection
from dto.geometries.point import Point
from dto.geopointcloud_dto import GeoPointcloudDTO
from dto.labeledpolyline_dto import LabeledPolylineDTO
from dto.pylon_dto import PylonDTO
from dto.pylonset_dto import PylonSetDTO
from dto.scenemap_dto import SceneMap3857
import json
import os
import time
from dto.towerline_dto import TowerLineDTO
from dto.towerlineset_dto import TowerLineSetDTO

if __name__ == '__main__':
    inicio = time.time()
    session = get_session()
    scene_json = SceneMap3857()
    composite_scene = ScenesComposite()

    circuits_view = CircuitViewDao(session).getCircuitsNewForZone('CENTRO')

    # scene_main = Scene()  NOT USE
    composite_scene.add(scene_json)
    for circuits in circuits_view:
        circ = CircuitsDTO(circuits)
        # Get all pointclouds from circuit
        print(circuits.id)
        lidar_query = GeoPointcloudDAO(session).test(circuits)
        # Iterate pointcloud and serialize to GeoPointCloudDTO
        for lidar in lidar_query:
            if lidar:
                geo = GeoPointcloudDTO(lidar)
                circ.add_layers(geo)

        # circuitline
        circuit_line = CircuitlineDAO(session).getCircuitLineById(circuits)
        linea = []
        for object_circuit in circuit_line:
            linestring_z = str(object_circuit.geom_text).replace("GEOMETRYCOLLECTION Z (LINESTRING Z (", "")
            arr_split = linestring_z.split("LINESTRING Z (")
            linea = LineStringCollection(object_circuit.geom_text).getLinestringCollectAsArrayself()
        circuiteline = CircuitLinesDTO(circuits.mnemonico, linea)
        circ.add_layers(circuiteline)

        ##LabeledPolyline De momento no se pone
        # labeled_polyline = LabeledPolylineDTO(circ.circuitmnemonico,
        #                                       np.array([-435029.019, 4925910.677, 0, -436366.272, 4922753.102, 0]))
        # circ.add_layers(labeled_polyline)

        # PylonSet
        pylons = PylonDAO(session).getPylonsFromCircuit(circuits)
        if len(pylons) > 0:
            pylonset = PylonSetDTO(circ.circuitmnemonico)
            for pylon in pylons:
                point = Point(pylon.geom_text).getPointAsArray()
                pylon_ = PylonDTO(pylon, point)
                pylonset.add_pylons(pylon_)
            circ.add_layers(pylonset)

        # Towerline

        # Get hipothesis data
        hipothesis_types = HipothesisDAO().getHipothesis()

        for hipothesis in hipothesis_types:
            # get towerline by circuitid and hipothesis
            # towerlines_data = TowerLineDao().TowerLineByCircuitAndHipothesis(circuits.id, hipothesis[0])
            towerlines_data = TowerLineDao2(session).getPylonsFromCircuit(circuits.id, hipothesis[0])
            if len(towerlines_data) > 0:
                towerline_set = TowerLineSetDTO(circ.circuitmnemonico, hipothesis)
                for towerline in towerlines_data:
                    towerline = TowerLineDTO(towerline)
                    towerline_set.add_towerlines(towerline)
                circ.add_layers(towerline_set)

        composite_scene.add(circ)
        # break

    data_json = composite_scene.generateSceneJSON()

    with open(os.getcwd() + "\layer.json", "w") as file:
        json.dump(data_json, file, indent=4)

    fin = time.time()
    print(fin - inicio)
