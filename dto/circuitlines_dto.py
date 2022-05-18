from collections import defaultdict

from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers
import numpy as np
import re

from utils.pcutils import convert_crs


class CircuitLinesDTO(ILayers):
    id: int = ""
    types: str = "CircuitLine"
    metadata: str = ""
    lines: list = []

    def __init__(self, id, lines):
        self.id = id
        self.types = "CircuitLine"
        self.metadata = "No circuit line metadata"
        self.label = id
        self.lines = lines

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + str("/CircuitLine"),
            "type": self.types,
            "metadata": self.metadata,
            "label": self.id,
            "lines": self.lines,
            "options": {}
        }
