import re

class LineString:

    def __init__(self, linestring : str):
        self.linestring = linestring

    def getLinestringAsArray(self):
        return [float(s) for s in re.findall(r'-?\d+\.?\d*', self.linestring)]