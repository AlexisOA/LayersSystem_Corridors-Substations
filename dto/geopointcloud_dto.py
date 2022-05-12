from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers


class GeoPointcloudDTO(ILayers):
    id: int = ""
    types: str = "GeoPointcloud"
    metadata: str = ""
    url: str = ""

    def __init__(self, obj):
        self.id = obj['circuitname']
        self.types = "GeoPointcloud"
        self.metadata = "No pointcloud metadata"
        self.url = str(obj['path'])

    def generateLayersJSON(self):
        return {
            "id": str(self.id) + str("/Pointcloud"),
            "type": self.types,
            "metadata": self.metadata,
            "url": "https://d35c0y5ctcznbt.cloudfront.net" + self.url
        }