from typing import List
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene


class TowerLineSetDTO(ILayers):

    def __init__(self, id, hipothesis_data):
        self.id = id
        self.types = "TowerLineSet"
        self.metadata = "TowerLineSet of Hypothesis 1"
        self.hyphotesis_id = "hypothesis" + str(hipothesis_data[0])
        self.towerlineSet = []
        self.wind = hipothesis_data[3]
        self.temperature = hipothesis_data[4]
        self.year = hipothesis_data[6]

    def add_towerlines(self, towerline):
        self.towerlineSet.append(towerline)

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + str("/TowerLineSet"),
            "type": self.types,
            "metadata": self.metadata,
            "hypothesis_id": self.hyphotesis_id,
            "towerlines": [
                towerline.generateLayersJSON() for towerline in self.towerlineSet
            ],
            "wind": self.wind,
            "temperature": self.temperature,
            "year": self.year
        }
