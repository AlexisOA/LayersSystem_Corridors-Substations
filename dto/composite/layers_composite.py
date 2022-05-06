from typing import List

from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers


class LayersComposite(ILayers):
    def __init__(self) -> None:
        self._children: List[ILayers] = []

    def remove(self, component: ILayers) -> None:
        self._children.remove(component)

    def add(self, component: ILayers) -> None:
        self._children.append(component)

    def count(self) -> int:
        return len(self._children)

    def generateLayersJSON(self):
        for item in self._children:
            item.generateLayersJSON()


