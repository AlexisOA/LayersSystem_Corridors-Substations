from dto.composite.I_Circuits import ICircuits
from dto.composite.I_Layers import ILayers


class GeoPointcloudDTO(ILayers):
    id: int = ""

    types: str = "GeoPointcloud"
    metadata: str = ""
    url: str = ""

    def __init__(self, obj):
        self.id = obj['path']
        self.types = "GeoPointcloud"
        self.metadata = None
        self.url = "https://d35c0y5ctcznbt.cloudfront.net/Models/CENTRO/101C_220LET-MOT"

    def generateLayersJSON(self):
        print({
            "id": str(self.id) + str("/Pointcloud"),
            "type": self.types,
            "metadata": self.metadata,
            "url": self.url
        })

    def __repr__(self):
        return str({
            "id": str(self.id) + str("/Pointcloud"),
            "type": self.types,
            "metadata": self.metadata,
            "url": self.url
        })


