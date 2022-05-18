from typing import List
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene
from dto.geometries.linestring import LineString
from utils.pcutils import convert_crs


class TowerLineDTO(ILayers):

    # def __init__(self, towerline_data):
    #     self.id = towerline_data[1]
    #     self.name = towerline_data[5]
    #     self.polyline_coords = LineString(towerline_data[2]).getLinestringAsArray()
    #     self.phase = towerline_data[8]

    def __init__(self, towerline_data):
        self.id = towerline_data.spanhipothesis_id
        self.name = towerline_data.name
        self.polyline_coords = LineString(towerline_data.geom_text).getLinestringAsArray()
        self.phase = towerline_data.phase
        self.year = towerline_data.year

    def generateLayersJSON(self):
        return {
            "id": self.id,
            "name": self.name,
            "polyline_coords": self.polyline_coords,
            "phase": self.phase,
            "year": self.year}
