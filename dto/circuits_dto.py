from typing import List

from sqlalchemy.engine import Row

from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene


class CircuitsDTO(IScene):

    def __init__(self, obj):
        self.circuitid = obj.id
        self.circuitmnemonico = obj.mnemonico
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


