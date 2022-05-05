from abc import ABCMeta, abstractmethod

class ICircuits(metaclass=ABCMeta):

    @abstractmethod
    def generateCircuitsJSON(self):
        "Print information"