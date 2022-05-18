import re

class Point:

    def __init__(self, point : str):
        self.point = point

    def getPointAsArray(self):
        return [float(s) for s in re.findall(r'-?\d+\.?\d*', self.point)]