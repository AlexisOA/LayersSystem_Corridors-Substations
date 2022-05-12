from typing import List

from dto.composite.I_Scene import IScene


class Scene(IScene):
    def __init__(self):
        self.id = "SCENE"
        self.type = "Composite"
        self.metada = "Non Metadata"
        self.children: List[IScene] = []

    def add_scenes(self, scene: IScene):
        self.children.append(scene)

    def generateSceneJSON(self):
        return {"id": self.id,
                "type": self.type,
                "metadata": self.metada,
                "children": [
                    child.generateSceneJSON() for child in self.children
                ]}
