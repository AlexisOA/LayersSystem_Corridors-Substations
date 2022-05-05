from typing import List

from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Scene import IScene


class CircuitsComposite(IScene):
    def __init__(self) -> None:
        self._children: List[IScene] = []

    def add(self, component: IScene) -> None:
        self._children.append(component)

    def remove(self, component: IScene) -> None:
        self._children.remove(component)

    def generateSceneJSON(self):
        """Iterate above array of components"""
        for items in self._children:
            return items.generateSceneJSON()