from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers
import numpy as np


class LabeledPolylineDTO(ILayers):
    id: int = ""
    types: str = "CircuitLine"
    metadata: str = ""
    coords: np.ndarray = []

    def __init__(self, id, coords):
        self.id = id
        self.types = "LabeledPolyline"
        self.metadata = "No labeled polyline metadata"
        self.coords = coords

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + str("/LabeledPolyline"),
            "type": self.types,
            "metadata": self.metadata,
            "lines": self.coords.tolist(),
            "options": {}
        }
