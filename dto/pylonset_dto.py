from typing import List
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene


class PylonSetDTO(ILayers):
    id: int = ""

    types: str = "PylonSet"
    metadata: str = ""

    def __init__(self, id):
        self.id = id
        self.types = "PylonSet"
        self.metadata = "No pylons metadata"
        self.pylonSet = []

    def add_pylons(self, pylon):
        self.pylonSet.append(pylon)

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + str("/PylonSet"),
            "type": self.types,
            "metadata": self.metadata,
            "pylons": [
                pylon.generateLayersJSON() for pylon in self.pylonSet
            ]
        }
