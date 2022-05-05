from abc import ABCMeta, abstractmethod

class IScene(metaclass=ABCMeta):

    @abstractmethod
    def generateSceneJSON(self):
        "Print information"