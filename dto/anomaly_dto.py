from typing import List
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene
from dto.geometries.linestring import LineString
from dto.geometries.point import Point
from utils.pcutils import convert_crs


class AnomalyDTO(ILayers):

    def __init__(self, anomaly_data):
        self.id = anomaly_data.anomalyid
        self.main_point = Point(anomaly_data.geom_main_text).getPointAsArray()
        self.secondary_points = Point(anomaly_data.geom_secondary).getPointAsArray()
        self.year = anomaly_data.yearname
        self.severity_id = anomaly_data.severityid
        self.hypothesis_id = anomaly_data.hipothesisid

    def generateLayersJSON(self):
        return {
            "id": self.id,
            "main_point": self.main_point,
            "secondary_points": self.secondary_points,
            "year": self.year,
            "severity_id": self.severity_id,
            "hypothesis_id": "hypothesis0" + str(self.hypothesis_id)}
