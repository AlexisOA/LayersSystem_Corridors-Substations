from typing import List
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene
from utils.pcutils import convert_crs


class PylonDTO(ILayers):
    id: int
    code: str
    type: str
    ut: str
    plate: str
    coords: list

    def __init__(self, obj, point):
        self.id = obj.id
        self.code = obj.code
        self.type = obj.type
        self.ut = obj.ut
        self.plate = obj.plate
        self.coords = point

    def generateLayersJSON(self):
        return {
            "id": self.id,
            "coords": self.coords,
            "code": self.code,
            "type": self.type,
            "plate": self.plate}
