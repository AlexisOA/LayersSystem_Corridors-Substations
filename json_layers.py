from connection.database import get_session
from dao.circuitline_dao import CircuitlineDAO
from dao.circuitview_dao import CircuitViewDao
from dao.distanceincidence_dao import DistanceIncidenceDAO
from dao.geopointcloud_dao import GeoPointcloudDAO
from dao.hipothesis_dao import HipothesisDAO
from dao.pylon_dao import PylonDAO
from dao.towerline_dao import TowerLineDao
from dao.towerline_dao_alchemy import TowerLineDao2
from dto.anomaliesset_dto import AnomaliesSetDTO
from dto.anomaly_dto import AnomalyDTO
from dto.circuitlines_dto import CircuitLinesDTO
from dto.circuits_dto import CircuitsDTO
from dto.composite.scene_composite import ScenesComposite
from dto.geometries.linestring_collect import LineStringCollection
from dto.geometries.point import Point
from dto.geopointcloud_dto import GeoPointcloudDTO
from dto.labeledpolyline_dto import LabeledPolylineDTO
from dto.pylon_dto import PylonDTO
from dto.pylonset_dto import PylonSetDTO
from dto.basemap_layer import BaseMapLayer
import json
import os
import time
from dto.towerline_dto import TowerLineDTO
from dto.towerlineset_dto import TowerLineSetDTO


class JsonLayer():
    def __init__(self,
                 circuit_zone: str,
                 parent_directory: str = ""):

        self.circuit_zone = circuit_zone
        self.composite_scene = ScenesComposite()
        self._parent_directory = parent_directory
        self.session = get_session()
        self.circuitDTO = None
        self.circuit = None
        self._circuits_name = []
        self.data_json = None

    def get_circuits_name_array(self):
        return self._circuits_name

    def generate_all_json(self, labelel_polilyne: bool = False):
        self.composite_scene.add(BaseMapLayer())
        circuits = self.get_circuits_by_zone(self.circuit_zone)
        self.set_layer_to_circuits(circuits)

    def generate_json_by_circuitid(self, tuples):
        self.composite_scene.add(BaseMapLayer())
        circuits = self.get_circuits_by_id(self.circuit_zone, tuples)
        self.set_layer_to_circuits(circuits)

    def set_layer_to_circuits(self, circuits):
        inicio = time.time()
        for c in circuits:
            print("Generating layers from circuit ", c.mnemonico)
            circuit_id_ = c.id
            self._circuits_name.append(c.mnemonico)
            self.circuit = c
            self.circuitDTO = CircuitsDTO(self.circuit)
            self.get_pointclouds_from_circuit(circuit_id_)
            self.get_circuitline_from_circuit(circuit_id_)
            self.get_pylon_from_circuit(circuit_id_)
            self.get_towerline_from_circuit(circuit_id_)
            self.get_anomalies_from_circuit(circuit_id_)
            self.composite_scene.add(self.circuitDTO)

        self.create_json()
        fin = time.time()
        print("Json generated in seconds: ", fin - inicio)

    def create_json(self):
        self.data_json = self.composite_scene.generateSceneJSON()

        with open(self._parent_directory + "\layer.json", "w") as file:
            print("Generating json...")
            json.dump(self.data_json, file, indent=4)
            print("Json generated succesfully")

    def get_pointclouds_from_circuit(self, circuit_id):
        lidar_query = GeoPointcloudDAO(self.session).test(circuit_id)
        for lidar in lidar_query:
            if lidar:
                geo = GeoPointcloudDTO(lidar)
                self.circuitDTO.add_layers(geo)

    def get_circuitline_from_circuit(self, circuit_id):
        circuit_line = CircuitlineDAO(self.session).getCircuitLineById(circuit_id)
        linea = []
        for object_circuit in circuit_line:
            linea = LineStringCollection(object_circuit.geom_text).getLinestringCollectAsArrayself()
        circuiteline = CircuitLinesDTO(self.circuitDTO.circuitmnemonico, linea)
        self.circuitDTO.add_layers(circuiteline)

    def get_circuits_by_zone(self, circuit_zone):
        circuits_view = CircuitViewDao(self.session).getCircuitsNewForZone(circuit_zone)
        for circuits in circuits_view:
            yield circuits

    def get_circuits_by_id(self, circuit_zone, tuple_ids):
        circuits_view = CircuitViewDao(self.session).getCircuitsNewForZoneandId(circuit_zone, tuple_ids)
        for circuits in circuits_view:
            yield circuits

    def get_pylon_from_circuit(self, circuit_id):
        pylons = PylonDAO(self.session).getPylonsFromCircuit(circuit_id)
        if len(pylons) > 0:
            pylonset = PylonSetDTO(self.circuitDTO.circuitmnemonico)
            for pylon in pylons:
                point = Point(pylon.geom_text).getPointAsArray()
                pylon_ = PylonDTO(pylon, point)
                pylonset.add_pylons(pylon_)
            self.circuitDTO.add_layers(pylonset)

    def get_towerline_from_circuit(self, circuit_id):
        hipothesis_types = HipothesisDAO().getHipothesis()

        for hipothesis in hipothesis_types:
            ## get towerline by circuitid and hipothesis
            #  towerlines_data = TowerLineDao().TowerLineByCircuitAndHipothesis(circuits.id, hipothesis[0])
            towerlines_data = TowerLineDao2(self.session).getPylonsFromCircuit(circuit_id, hipothesis[0])
            towerline_set = TowerLineSetDTO(self.circuitDTO.circuitmnemonico, hipothesis)
            if len(towerlines_data) > 0:
                for towerline in towerlines_data:
                    towerline = TowerLineDTO(towerline)
                    towerline_set.add_towerlines(towerline)
            self.circuitDTO.add_layers(towerline_set)

    def get_anomalies_from_circuit(self, circuit_id):
        anomalies = DistanceIncidenceDAO(self.session).getAnomalysByCircuitID(circuit_id)
        anomalies_set = AnomaliesSetDTO(self.circuit.mnemonico)
        if len(anomalies):
            for anomaly in anomalies:
                anomalie = AnomalyDTO(anomaly)
                anomalies_set.add_anomalies(anomalie)
        self.circuitDTO.add_layers(anomalies_set)

    def update_json_labeled_polyline(self, name, dict_data):
        # open json for read
        with open(self._parent_directory + "\layer.json") as fp:
            listObj = json.load(fp)
            for idx, child in enumerate(listObj['children']):
                if child['id'] == name:
                    child['children'].append(dict_data)
            self.data_json = listObj
        # open json for update
        with open(self._parent_directory + "\layer.json", "w") as file:
            print("updating json...")
            json.dump(self.data_json, file, indent=4)
            print("Json update succesfully")

    def update_json_add_circuits(self, tuples):
        pass

# if __name__ == '__main__':
#     inicio = time.time()
#     session = get_session()
#     scene_json = BaseMapLayer()
#     composite_scene = ScenesComposite()
#
#     circuits_view = CircuitViewDao(session).getCircuitsNewForZone('NOROESTE')
#     print("Número de circuitos en la zona NOROESTE -> ", len(circuits_view))
#     ## scene_main = Scene()  NOT USE
#     composite_scene.add(scene_json)
#     for circuits in circuits_view:
#         # if circuits.id == 382:
#         circuit_id_ = circuits.id
#         circ = CircuitsDTO(circuits)
#         ## Get all pointclouds from circuit
#         print("ID: ", circuit_id_)
#         lidar_query = GeoPointcloudDAO(session).test(circuit_id_)
#         ## Iterate pointcloud and serialize to GeoPointCloudDTO
#         for lidar in lidar_query:
#             if lidar:
#                 print(lidar)
#                 geo = GeoPointcloudDTO(lidar)
#                 circ.add_layers(geo)
#
#         ## circuitline
#         circuit_line = CircuitlineDAO(session).getCircuitLineById(circuit_id_)
#         linea = []
#         for object_circuit in circuit_line:
#             # print(object_circuit.geom_text)
#             # linestring_z = str(object_circuit.geom_text).replace("GEOMETRYCOLLECTION Z (LINESTRING Z (", "")
#             # arr_split = linestring_z.split("LINESTRING Z (")
#             linea = LineStringCollection(object_circuit.geom_text).getLinestringCollectAsArrayself()
#         circuiteline = CircuitLinesDTO(circuits.mnemonico, linea)
#         circ.add_layers(circuiteline)
#
#         ## LabeledPolyline -> Lines that user draw in the scene, at that moment not
#         #  labeled_polyline = LabeledPolylineDTO(circ.circuitmnemonico,
#         #                                       np.array([-435029.019, 4925910.677, 0, -436366.272, 4922753.102, 0]))
#         #  circ.add_layers(labeled_polyline)
#
#         ## PylonSet
#         pylons = PylonDAO(session).getPylonsFromCircuit(circuit_id_)
#         if len(pylons) > 0:
#             pylonset = PylonSetDTO(circ.circuitmnemonico)
#             for pylon in pylons:
#                 point = Point(pylon.geom_text).getPointAsArray()
#                 pylon_ = PylonDTO(pylon, point)
#                 pylonset.add_pylons(pylon_)
#             circ.add_layers(pylonset)
#
#         ## Towerline
#         ## Get hipothesis data
#         hipothesis_types = HipothesisDAO().getHipothesis()
#
#         for hipothesis in hipothesis_types:
#             ## get towerline by circuitid and hipothesis
#             #  towerlines_data = TowerLineDao().TowerLineByCircuitAndHipothesis(circuits.id, hipothesis[0])
#             towerlines_data = TowerLineDao2(session).getPylonsFromCircuit(circuit_id_, hipothesis[0])
#             towerline_set = TowerLineSetDTO(circ.circuitmnemonico, hipothesis)
#             if len(towerlines_data) > 0:
#                 for towerline in towerlines_data:
#                     towerline = TowerLineDTO(towerline)
#                     towerline_set.add_towerlines(towerline)
#             circ.add_layers(towerline_set)
#
#         ##Anomalies,
#         anomalies = DistanceIncidenceDAO(session).getAnomalysByCircuitID(circuit_id_)
#         anomalies_set = AnomaliesSetDTO(circuits.mnemonico)
#         if len(anomalies):
#             for anomaly in anomalies:
#                 anomalie = AnomalyDTO(anomaly)
#                 anomalies_set.add_anomalies(anomalie)
#         circ.add_layers(anomalies_set)
#         composite_scene.add(circ)
#         # break
#
#     data_json = composite_scene.generateSceneJSON()
#
#     with open(os.getcwd() + "\layer.json", "w") as file:
#         print("Generating json...")
#         json.dump(data_json, file, indent=4)
#         print("Json generated succesfully")
#
#     fin = time.time()
#     print(fin - inicio)
# 6624.5480766 seg el ultimo sbn
