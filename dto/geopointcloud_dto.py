from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers


class GeoPointcloudDTO(ILayers):

    def __init__(self, obj):
        self.id = obj.mnemonico
        self.types = "GeoPointcloud"
        self.metadata = "No pointcloud metadata"
        self.url = obj.path

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + "/Pointcloud",
            "type": self.types,
            "metadata": self.metadata,
            "url": "http://80.28.134.48" + self.url
        }