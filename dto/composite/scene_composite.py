from typing import List

from dto.composite.I_Scene import IScene


class ScenesComposite(IScene):
    def __init__(self):
        self.id = "SCENE"
        self.type = "Composite"
        self.metada = "Non Metadata"
        self._children: List[IScene] = []

    def add(self, component: IScene):
        self._children.append(component)

    def remove(self, component: IScene):
        self._children.remove(component)

    def count(self) -> int:
        return len(self._children)

    def generateSceneJSON(self):
        return {"id": self.id,
                "type": self.type,
                "metadata": self.metada,
                "children": [
                    child.generateSceneJSON() for child in self._children
                ]}

