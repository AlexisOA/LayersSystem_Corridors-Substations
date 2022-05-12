from typing import List

from sqlalchemy.engine import Row

from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene


class CircuitsDTO(IScene):
    compnayid: int
    companyname: str
    countryid: int
    countryname: str
    regionid: int
    regionname: str
    areaid: int
    areaname: str
    circuitid: int
    circuitmnemonico: str
    type: str
    metadata: str

    def __init__(self, obj):
        self.compnayid = obj.companyid
        self.companyname = obj.companyname
        self.countryid = obj.countryid
        self.countryname = obj.countryname
        self.regionid = obj.regionid
        self.regionname = obj.regionname
        self.areaid = obj.areaid
        self.areaname = obj.areaname
        self.circuitid = obj.circuitid
        self.circuitmnemonico = obj.circuitname
        self.type = "Composite"
        self.metadata = "No circuit Metadata"
        self.children: List[ILayers] = []

    def add_layers(self, layer: ILayers):
        self.children.append(layer)

    def generateSceneJSON(self):
        return {
            "id": self.circuitmnemonico,
            "type": self.type,
            "metadata": self.metadata,
            "children" : [
                child.generateLayersJSON() for child in self.children
            ]}


