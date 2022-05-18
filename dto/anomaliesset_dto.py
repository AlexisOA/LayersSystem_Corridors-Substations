from typing import List
from dto.composite.I_Layers import ILayers
from dto.composite.I_Scene import IScene


class AnomaliesSetDTO(ILayers):

    def __init__(self, id):
        self.id = id
        self.types = "AnomalySet"
        self.metadata = "No metadata in anomalyset"
        self.anomalies = []

    def add_anomalies(self, anomalie):
        self.anomalies.append(anomalie)

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + str("/AnomalySet"),
            "type": self.types,
            "metadata": self.metadata,
            "anomalies": [
                anomaly.generateLayersJSON() for anomaly in self.anomalies
            ]
        }
