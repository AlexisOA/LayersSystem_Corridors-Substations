from abc import ABCMeta, abstractmethod

class ILayers(metaclass=ABCMeta):

    @abstractmethod
    def generateLayersJSON(self):
        "Print information"