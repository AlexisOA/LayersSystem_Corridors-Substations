from typing import List

from dto.composite.I_Scene import IScene


class ScenesComposite(IScene):
    def __init__(self) -> None:
        self._children: List[IScene] = []

    def add(self, component: IScene) -> None:
        self._children.append(component)

    def remove(self, component: IScene) -> None:
        self._children.remove(component)

    def count(self) -> int:
        return len(self._children)

    def jsonRoot(self):
        return {
            "id": "SCENE",
            "type": "Composite",
            "metadata": "None",
            "children": [self.generateSceneJSON()]
        }

    def generateSceneJSON(self):
        for item in self._children:
            print(item.generateSceneJSON())
