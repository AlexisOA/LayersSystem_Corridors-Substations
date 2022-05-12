import numpy as np
from connection.database import get_session
from dao.circuitline_dao import CircuitlineDAO
from dao.circuitview_dao import CircuitViewDao
from dao.geopointcloud_dao import GeoPointcloudDAO
from dao.pylon_dao import PylonDAO
from dto.circuitlines_dto import CircuitLinesDTO
from dto.circuits_dto import CircuitsDTO
from dto.composite.scene_composite import ScenesComposite
from dto.geopointcloud_dto import GeoPointcloudDTO
from dto.labeledpolyline_dto import LabeledPolylineDTO
from dto.pylon_dto import PylonDTO
from dto.pylonset_dto import PylonSetDTO
from dto.scenemap_dto import SceneMap3857
import json
import os
import re
from orm.lidarsource import Circuits, CircuitGeoms, CircuitGeomTypes
from sqlalchemy import func
import time

if __name__ == '__main__':
    session = get_session()
    scene_json = SceneMap3857()
    composite_scene = ScenesComposite()

    circuitsview = CircuitViewDao(session).getCircuitsForZone('CENTRO')

    # scene_main = Scene()  NOT USE
    composite_scene.add(scene_json)

    for circuits in circuitsview:
        circ = CircuitsDTO(circuits)
        # Get all pointclouds from circuit
        lidar_query = GeoPointcloudDAO(session).getPointcloudFromCircuit(circuits)
        # Iterate pointcloud and serialize to GeoPointCloudDTO
        for lidar in lidar_query:
            if lidar:
                geo = GeoPointcloudDTO(lidar)
                circ.add_layers(geo)

        # Testing circuitline
        print("####### Testing circuiteline #######")
        t_init = time.time()
        circuit_line = session.query(Circuits.mnemonico.label('id'),
                                     func.ST_AsText(CircuitGeoms.geom).label('geom_text')
                                     ).join(CircuitGeoms,CircuitGeoms.circuitid == Circuits.id
                                    ).join(CircuitGeomTypes,CircuitGeomTypes.id == CircuitGeoms.geomtypeid
                                           ).filter(CircuitGeomTypes.name == "Tower_String").filter(Circuits.id == circuits.circuitid).all()
        # circuiteline_test = CircuitLinesDTO(circuit_line.circuitmnemonico, circuit_line.)
        arr_split = []
        for object_circuit in circuit_line:
            linestring_z = str(object_circuit.geom_text).replace("GEOMETRYCOLLECTION Z (LINESTRING Z (", "")
            arr_split = linestring_z.split("LINESTRING Z (")
        circuiteline = CircuitLinesDTO(circuits.circuitname, arr_split)
        circ.add_layers(circuiteline)

        ##LabeledPolyline
        labeled_polyline = LabeledPolylineDTO(circ.circuitmnemonico,
                                              np.array([-435029.019, 4925910.677, 0, -436366.272, 4922753.102, 0]))
        circ.add_layers(labeled_polyline)

        # PylonSet
        pylonset = PylonSetDTO(circ.circuitmnemonico)
        pylons = PylonDAO(session).getPylonsFromCircuit(circuits)
        for pylon in pylons:
            pylon_ = PylonDTO(pylon)
            pylonset.add_pylons(pylon_)
        circ.add_layers(pylonset)
        composite_scene.add(circ)

    # print(composite_scene.generateSceneJSON())
    data_json = composite_scene.generateSceneJSON()

    # data_string = scene_main.generateSceneJSON()
    # print(data_string)
    with open(os.getcwd() + "\layer.json", "w") as file:
        json.dump(data_json, file, indent=4)
