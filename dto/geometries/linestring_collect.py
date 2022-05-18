import re
import numpy as np


# Return linestrings array
class LineStringCollection:

    def __init__(self, linestring_collect: str):
        self.linestring_collect = linestring_collect

    def getLinestringCollectAsArrayself(self) -> list:
        linestring_z = self.linestring_collect.replace("GEOMETRYCOLLECTION Z (LINESTRING Z (", "")
        lines_split = linestring_z.split("LINESTRING Z (")
        lines = []
        for idx, i in enumerate(lines_split):
            lines.append([float(s) for s in re.findall(r'-?\d+\.?\d*', i)])
        return lines
