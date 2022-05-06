from typing import List

from dto.composite.I_Scene import IScene


class CompositeScenes(IScene):
    def __init__(self):
        self._children: List[IScene] = []

    def add(self, component: IScene):
        self._children.append(component)

    def remove(self, component: IScene):
        self._children.remove(component)

    def count(self) -> int:
        return len(self._children)

    def generateSceneJSON(self):
        for scene in self._children:
            scene.generateSceneJSON()
