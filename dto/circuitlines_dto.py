from collections import defaultdict

from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers
import numpy as np
import re

from utils.pcutils import convert_crs, convert_crs_individual_values


class CircuitLinesDTO(ILayers):
    id: int = ""
    types: str = "CircuitLine"
    metadata: str = ""
    lines: list = []

    def __init__(self, id, lines):
        self.id = id
        self.types = "CircuitLine"
        self.metadata = "No circuit line metadata"
        self.lines = lines
        self.lines_dict = []
        for idx, i in enumerate(self.lines):
            a = np.array([float(s) for s in re.findall(r'-?\d+\.?\d*', i)])
            self.lines_dict.append(self.convert_crs_circuitlines(a).tolist())

    def convert_crs_circuitlines(self, coords) -> np.ndarray:
        for idx, coord in enumerate(coords):
            if coord == 0:
                x, y = convert_crs(coords[idx - 2],
                                   coords[idx - 1], 4326, 3857)
                coords[idx - 2] = x
                coords[idx - 1] = y

        return coords

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + str("/CircuitLine"),
            "type": self.types,
            "metadata": self.metadata,
            "lines": self.lines_dict,
            "options": {}
        }
