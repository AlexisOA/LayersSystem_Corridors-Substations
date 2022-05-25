from dto.composite.I_Scene import IScene


class BaseMapLayer(IScene):
    id: str
    types: str
    metadata: str
    wtm_template_layers: []

    def __init__(self):
        self.id = "SCENE_MAP"
        self.types = "Map"
        self.metadata = "None"
        self.wtm_template_layers = [{
            "url_template": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "sector_epsg_3857": [-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244],
            "min_level": 0,
            "max_level": 18
        }]

    def generateSceneJSON(self):
        return {
            "id": self.id,
            "type": self.types,
            "metadata": self.metadata,
            "wtm_template_layers": self.wtm_template_layers
        }


